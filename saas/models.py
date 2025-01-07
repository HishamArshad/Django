from django.db import models
from django.conf import settings
# Create your models here.
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta, date
class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    name = models.CharField(max_length=255)  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()  # Next payment/renewal date
    is_recurring = models.BooleanField(default=True)  
    status = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def needs_notification(self):
        # Check if today is two days before the payment date
        return date.today() == (self.payment_date - timedelta(days=2))

    def update_payment_date(self):
        # Update the payment date to the next month if the subscription is recurring
        if self.is_recurring and self.payment_date <= date.today():
            # Increment the payment_date by one month
            next_month = self.payment_date + timedelta(days=30)
            self.payment_date = next_month
            self.save()

    def __str__(self):
        return f"{self.name} - {self.user.email}"
 

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, null=True, blank=True)  # Optional: Icon for the category
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(default=now)
    payment_method = models.CharField(max_length=255, blank=True, null=True)
    recurring = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Override save method to update the related budget when an expense is added or updated.
        """
        super().save(*args, **kwargs)

        # Find and update the associated budget
        budgets = Budget.objects.filter(
            user=self.user,
            category=self.category,
            start_date__lte=self.date,
            end_date__gte=self.date
        )
        for budget in budgets:
            budget.update_budget()

    def delete(self, *args, **kwargs):
        """
        Override delete method to update the related budget when an expense is removed.
        """
        related_budgets = Budget.objects.filter(
            user=self.user,
            category=self.category,
            start_date__lte=self.date,
            end_date__gte=self.date
        )
        super().delete(*args, **kwargs)

        # Update budgets after deletion
        for budget in related_budgets:
            budget.update_budget()

    def __str__(self):
        return f"{self.name}: ${self.amount} on {self.date}"

class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Total budget amount
    start_date = models.DateField()
    end_date = models.DateField()
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Total expenses so far
    remaining_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Remaining budget
    exceeded_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Exceeded amount if over budget

    def update_budget(self):
        """
        Automatically update total_expenses, remaining_budget, and exceeded_amount based on associated expenses.
        """
        # Get all expenses linked to this budget's category and within its date range
        total = Expense.objects.filter(
            user=self.user,
            category=self.category,
            date__range=(self.start_date, self.end_date)
        ).aggregate(Sum('amount'))['amount__sum'] or 0.0  # Default to 0.0 if no expenses

        self.total_expenses = total
        self.remaining_budget = self.amount - self.total_expenses

        # Calculate exceeded amount (if total_expenses exceeds the budget amount)
        if self.total_expenses > self.amount:
            self.exceeded_amount = self.total_expenses - self.amount
        else:
            self.exceeded_amount = 0.0

        self.save()

    def __str__(self):
        if self.exceeded_amount > 0:
            return f"{self.category} Budget: ${self.amount} (Exceeded by: ${self.exceeded_amount})"
        return f"{self.category} Budget: ${self.amount} (Remaining: ${self.remaining_budget})"
