from django.contrib import admin
from .models import Expense

# Register your models here.
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'category', 'date', 'created_at')
    list_filter = ('category', 'date', 'user')
    search_fields = ('description',)