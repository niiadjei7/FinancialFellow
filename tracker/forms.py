# tracker/forms.py

from django import forms
from .models import Budget, Expense, Bill, ExpenseLimit, ExpenseType, LoggedExpense

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'amount']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'amount']

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['name', 'due_day', 'amount']

class ExpenseLimitForm(forms.ModelForm):
    class Meta:
        model = ExpenseLimit
        fields = ['limit']

class LoggedExpenseForm(forms.ModelForm):
    expense_type = forms.ModelChoiceField(
        queryset=ExpenseType.objects.all(),
        empty_label="Select Expense Type",
        to_field_name="name",  # Use the 'name' field of ExpenseType as the display field
    )

    class Meta:
        model = LoggedExpense  # Specify the model for the form
        fields = ['name', 'expense_type', 'amount', 'date']
