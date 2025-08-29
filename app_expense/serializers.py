from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Expense


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)


    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')


    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ('id', 'amount', 'category', 'description', 'date', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be positive.')
        return value