from .models import MyUser
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name']

 

    def create(self, validated_data):
        user = MyUser.objects.create_user(
         
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
  
        user.save()
        return user
 
 
 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'first_name', 'last_name', 'is_verified', 'date_of_birth', 'profile_picture']
    read_only_fields = ['id', 'email', 'is_verified']

    def update(self, instance, validated_data):
        # Simply update the user instance with the validated data
        return super().update(instance, validated_data)