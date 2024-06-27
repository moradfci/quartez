from rest_framework import serializers
from .models import BusinessOwner, Employee, Company, Review, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password',]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class BusinessOwnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = BusinessOwner
        fields = ['user',]
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        business_owner = BusinessOwner.objects.create(
            user=user, **validated_data)
        return business_owner
    
    


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Employee
        fields = ['id', 'user', 'company','owner']
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        employee = Employee.objects.create(user=user, **validated_data)
        return employee

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ['created_at','updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = '__all__'