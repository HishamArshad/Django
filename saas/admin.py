from django.contrib import admin
from .models import Subscription, Expense, Budget, Category

admin.site.register(Subscription)
admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(Budget)
