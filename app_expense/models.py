from django.db import models
from django.conf import settings


class Expense(models.Model):
    CATEGORY_CHOICES = [
    ('food', 'Food'),
    ('travel', 'Travel'),
    ('shopping', 'Shopping'),
    ('bills', 'Bills'),
    ('other', 'Other'),
    ]


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-date', '-id']


    def __str__(self):
        return f"{self.user} — {self.category} — {self.amount} on {self.date}"
