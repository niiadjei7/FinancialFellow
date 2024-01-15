from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Sum
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Budget, Expense, Bill, ExpenseLimit, ExpenseType, LoggedExpense, MonthlySummary
from .forms import BudgetForm, ExpenseForm, BillForm, ExpenseLimitForm, LoggedExpenseForm
import json
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
import calendar
import datetime

def spending_chart(request):

    if request.user.is_authenticated:
        triallabels =[]
        data = []
        labels = []

        if timezone.now().month <= 9:
            monthyear = f'{timezone.now().year}-0{timezone.now().month}'
        else:
            monthyear = f'{timezone.now().year}-{timezone.now().month}'

        all_types=ExpenseType.objects.all()
        for type in all_types:
            triallabels.append(f'{type.name}')
        for i in range(len(triallabels)):
            total_amount = LoggedExpense.objects.filter(user=request.user, expense_type__name__exact=triallabels[i], month_year=monthyear).aggregate(total=Sum('amount'))
            if total_amount['total'] is not None:
                total = float(total_amount['total'])
                data.append(round(total,2))
                labels.append(triallabels[i])

        chartdata = {
            'labels': labels,
            'data' : data
        }
        return chartdata

    else:
        print(1)
        return JsonResponse({'error': 'User not authenticated'})
    


def budget_visualization(request):
    # Call your function to generate chart data
    chart_data = spending_chart(request)
    print(chart_data)
    # Pass the chart data to the template
    return render(request, 'budget_visualization.html', {'chart_data' : chart_data})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print('success')
            next_url = request.GET.get('next', '/tracker/profile/')
            return redirect(next_url)    
        else:
            form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def log_out(request):
    if request.method == 'POST':    
        logout(request)
        return redirect('/tracker/')
    else:
        # If the view receives a GET request, you can handle it as needed
        return render(request, 'tracker/logout.html')  # Replace 'home' with the name of your home or login view

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

@login_required
def profile(request):
    user = request.user
    now = timezone.now()
    closest_bill = Bill.objects.filter(user=user, due_day__gte=now.day).order_by('due_day').first()
    if closest_bill is not None:
        reminder_day = closest_bill.due_day
        reminder_month = calendar.month_name[now.month]
    if closest_bill is None:
        # Fetch the closest bill reminder for the next month
        closest_bill_next_month = Bill.objects.filter(user=user, due_day__gte=1).order_by('due_day').first()
        closest_bill = closest_bill_next_month
        reminder_day = closest_bill.due_day if closest_bill else None
        if now.month < 12:
            reminder_month = calendar.month_name[(now.month) + 1]
        else:
            reminder_month = calendar.month_name[1]
    return render(request, 'tracker/profile.html', {'closest_bill': closest_bill, 'reminder_day': reminder_day, 'reminder_month': reminder_month, 'bill' : closest_bill})

@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user).exclude(user=None)
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

def edit_budget(request, budget_id):
    budget = get_object_or_404(Budget, pk=budget_id)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
        return redirect('budget_list')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'tracker/edit_budget.html', {'form': form, 'budget': budget})


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

@login_required
def bill_list(request):
    bills = Bill.objects.filter(user=request.user).exclude(user=None)
    return render(request, 'tracker/bill_list.html', {'bills': bills})

@login_required
def add_bill(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.user=request.user
            form.save()
            return redirect('bill_list')
    else:
        form = BillForm()
    return render(request, 'tracker/add_bill.html', {'form': form})

def edit_bill(request, bill_id):
    bill = get_object_or_404(Bill, pk=bill_id)
    if request.method == 'POST':
        form = BillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
        return redirect('bill_list')
    else:
        form = BillForm(instance=bill)
    return render(request, 'tracker/edit_bill.html', {'form': form, 'bill': bill})

def delete_bill(request, bill_id):
    bill = get_object_or_404(Bill, pk=bill_id)
    if request.method == 'POST':
        bill.delete()
        return redirect('bill_list')
    return render(request, 'tracker/delete_bill.html', {'bill': bill})


@login_required
def set_expense_limit(request):
    if request.method == 'POST':
        form = ExpenseLimitForm(request.POST)
        if form.is_valid():
            limit = form.save(commit=False)
            limit.user = request.user
            limit.save()
            return redirect('logged_expenses')  # Redirect to a dashboard or another page
    else:
        form = ExpenseLimitForm()

    return render(request, 'tracker/set_expense_limit.html', {'form': form})

def monthly_report(request):
    monthly_total=0.0
    monthyear = []
    totals = []
    logs = LoggedExpense.objects.filter(user=request.user).exclude(user=None)
    for log in logs:
        log.month_year = log.date.strftime('%Y-%m')
        if log.month_year not in monthyear:
            monthyear.append(log.month_year)
    print(monthyear)

    monthly_objects = []
    for i in range(len(monthyear)):
        monthly_total=0
        for log in logs:
            if log.month_year == monthyear[i]:
                monthly_total += float(log.amount)
        totals.append(round(float(monthly_total),2))
    chartdata = {
        'labels': monthyear,
        'data': totals
    }

    return render(request, 'monthly_report.html', {'labels' : monthyear, 'data': totals})

@login_required
def logged_expenses(request):
    if timezone.now().month <= 9:
        monthyear = f'{timezone.now().year}-0{timezone.now().month}'
    else:
        monthyear = f'{timezone.now().year}-{timezone.now().month}'
    print(monthyear)
    user=request.user
    limit = ExpenseLimit.objects.filter(user=user).first()
    logs = LoggedExpense.objects.filter(user=user, month_year=monthyear).exclude(user=None)

    
    data = spending_chart(request)
    labels = data.get('labels')
    amounts = data.get('data')

    monthly_data = monthly_report(request)
    monthly_labels = monthly_data.get('labels')
    monthly_amounts = monthly_data.get('data')
    total_expenses = 0
    if limit:
        for log in logs:
            total_expenses += log.amount
        remainder = limit.limit - total_expenses
    else:
        remainder = 0
    return render(request, 'tracker/logged_expenses.html', {'logs': logs, 'monthly_labels': monthly_labels, 'monthly_amounts': monthly_amounts,'limit': limit, 'total': total_expenses, 'remainder': remainder, 'labels': labels, 'amounts': amounts})
    


@login_required
def add_log(request):
    if request.method == 'POST':
        form = LoggedExpenseForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.month_year = log.date.strftime('%Y-%m')
            log.save()
            return redirect('logged_expenses')  # Redirect to a dashboard or another page
            
    else:
        form = LoggedExpenseForm()

    return render(request, 'tracker/new_log.html', {'form': form})

def delete_log(request, log_id):
    log = get_object_or_404(LoggedExpense, pk=log_id)
    if request.method == 'POST':
        log.delete()
        return redirect('logged_expenses')
    return render(request, 'tracker/delete_log.html', {'log': log})

def edit_log(request, log_id):
    log = get_object_or_404(LoggedExpense, pk=log_id)
    if request.method == 'POST':
        form = LoggedExpenseForm(request.POST, instance=log)
        if form.is_valid():
            log = form.save()
            log.month_year = log.date.strftime('%Y-%m')
            log.save()
        return redirect('logged_expenses')
    else:
        form = LoggedExpenseForm(instance=log)
    return render(request, 'tracker/edit_log.html', {'form': form, 'log': log})

@login_required
def create_monthly_summary(request):
    months = []
    logs = LoggedExpense.objects.filter(user=request.user).exclude(user=None)
    for log in logs:
        log.month_year = log.date.strftime('%Y-%m')
        if log.month_year not in months:
            months.append(log.month_year)

    for month in months:
        monthly_total=LoggedExpense.objects.filter(user=request.user, month_year = month).aggregate(total=Sum('amount'))
        if monthly_total['total'] is not None:
            total = round(float(monthly_total['total']),2)
        new_summary = MonthlySummary(
            month_year = month,
        )
        new_summary.save()

@login_required
def monthly_summary(request):
    create_monthly_summary(request)
    month = request.GET.get('month', '') 
    year = request.GET.get('year', '')
   
    monthyear = f'{year}-{month}'
    logs = []
    bills = []
    not_future = False
    no_history_available=True
    logs_total = 0
    month_total = 0
    bill_total=0.0
    if month and year:
        all_logs = LoggedExpense.objects.filter(user=request.user).exclude(user=None)

        for log in all_logs:
            log.month_year = log.date.strftime('%Y-%m')
            if log.month_year == monthyear:
                no_history_available = False
                logs.append(log)
                logs_total += log.amount
        print(f'logs: {logs}')
        print(f'no_history: {no_history_available}')
        bills = Bill.objects.filter(user=request.user)
        

        if (int(year) < timezone.now().year):
            not_future=True
        elif int(year) == timezone.now().year:
            if int(month) <=timezone.now().month:
                not_future=True
            else:
                not_future=False
        else:
            not_future=False
        
        month = calendar.month_name[int(month)]

        print(logs_total)
        bill_total = Bill.objects.filter(user=request.user).aggregate(total=Sum('amount'))
        if bill_total['total'] is None:
            bill_total = 0.0
        else:
            bill_total = float(bill_total['total'])
        print(bill_total)
        month_total = round((float(logs_total) + bill_total), 2)

    context = {
        'logs': logs,
        'logs_total': logs_total,
        'bills': bills,
        'bill_total': bill_total,
        'month': month,
        'year' : year,
        'total': month_total,
        'not_future': not_future,
        'no_history_available': no_history_available
    }

    return render(request, 'tracker/monthly_summary.html', context)



    













