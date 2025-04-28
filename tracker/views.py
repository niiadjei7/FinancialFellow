from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Budget, Expense
from .forms import BudgetForm, ExpenseForm
import json

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', '/tracker/profile/')
            return redirect(next_url)    
        else:
            form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('welcome_screen')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def welcome_screen(request):
    return render(request, 'tracker/welcome_screen.html')

def profile(request):
    return render(request, 'tracker/profile.html', {'user': request.user})

@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user).exclude(user=None)
    print(f"User: {request.user}, Budgets: {budgets}")
    all_budgets =  Budget.objects.all()
    print(f"All Budgets: {all_budgets}")
    return render(request, 'tracker/budget_list.html', {'budgets': budgets})

def budget_data_api(request):
    budgets = Budget.objects.filter(user=request.user)
    data = {
        'labels': [budget.name for budget in budgets],
        'amounts': [budget.amount for budget in budgets],
    }
    return JsonResponse(data)

def expenses(request, budget_id):
    budget = Budget.objects.get(pk=budget_id)
    expenses = Expense.objects.filter(budget=budget)
    total_expenses = budget.total_expenses()
    remaining_budget = budget.amount - total_expenses

    return render(request, 'tracker/expenses.html', {
        'budget': budget,
        'expenses': expenses,
        'total_expenses': total_expenses,
        'remaining_budget': remaining_budget,
    })

@login_required
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user=request.user
            form.save()
            return redirect('budget_list')
    else:
        form = BudgetForm()
    return render(request, 'tracker/add_budget.html', {'form': form})

@login_required
def add_expense(request, budget_id):
    budget = Budget.objects.get(id=budget_id)  # Assuming you have a Budget model
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user=request.user
            expense.budget=budget
            expense.save()
            return redirect('expenses', budget_id=budget_id)
    else:
        form = ExpenseForm()

    return render(request, 'tracker/add_expense.html', {'form': form, 'budget_id': budget_id})

def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expenses', budget_id=expense.budget.id)
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'tracker/edit_expense.html', {'form': form, 'expense': expense})

def delete_budget(request, budget_id):
    budget = get_object_or_404(Budget, pk=budget_id)
    if request.method == 'POST':
        budget.delete()
        return redirect('budget_list')
    return render(request, 'tracker/delete_budget.html', {'budget': budget})

def delete_expense(request, budget_id, expense_id):
    budget = get_object_or_404(Budget, pk=budget_id)
    expense = get_object_or_404(Expense, pk=expense_id)
    if request.method == 'POST':
        expense.delete()
        return redirect('expenses', budget_id=budget_id)
    return render(request, 'tracker/delete_expense.html', {'budget' : budget, 'expense': expense})