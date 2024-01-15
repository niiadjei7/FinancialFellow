from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.utils import timezone

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    def total_expenses(self):
        return self.expense_set.aggregate(models.Sum('amount'))['amount__sum'] or 0

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    due_day = models.PositiveIntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def ___str___(self):
        return self.name


class ExpenseLimit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class ExpenseType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class LoggedExpense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    expense_type = models.ForeignKey(ExpenseType, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    month_year = models.CharField(max_length=7, editable=False)  # Format: YYYY-MM

    
    def ___str___(self):
        return self.name
    
class MonthlySummary(models.Model):
    month_year = models.CharField(max_length=7, editable=False)

    def __str__(self):
        return self.name
    



# Create your models here.
