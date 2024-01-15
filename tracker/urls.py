from django.urls import path, include
from django.conf import settings
#from .views import budget_list, expenses, add_budget, add_expense, delete_budget, delete_expense, log_out, logged_expenses, add_log, set_expense_limit, edit_log, delete_log
#from .views import welcome_screen, register_view, login_view, profile,spending_chart, edit_expense, edit_budget, add_bill, edit_bill, delete_bill, bill_list
from .views import *
urlpatterns = [
    path('', welcome_screen, name='welcome_screen'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', log_out,name='log_out'),
    path('profile/', profile, name='profile'),
    path('budgets/', budget_list, name='budget_list'),
    path('expenses/<int:budget_id>/', expenses, name='expenses'),
    path('add_budget/', add_budget, name='add_budget'),
    path('add_expense/<int:budget_id>/', add_expense, name='add_expense'),
    path('edit_expense/<int:expense_id>/', edit_expense, name='edit_expense'),
    path('edit_budget/<int:budget_id>/', edit_budget, name='edit_budget'),  
    path('delete_budget/<int:budget_id>/', delete_budget, name='delete_budget'),
    path('delete_expense/<int:budget_id>/<int:expense_id>/', delete_expense, name='delete_expense'),
    path('bill_list/', bill_list, name='bill_list'),
    path('add_bill/', add_bill, name='add_bill'),
    path('edit_bill/<int:bill_id>/', edit_bill, name='edit_bill'),
    path('delete_bill/<int:bill_id>/', delete_bill, name='delete_bill'),
    path('new_log/', add_log, name='new_log'),
    path('set_expense_limit/', set_expense_limit, name='set_expense_limit'),
    path('logged_expenses/', logged_expenses, name='logged_expenses'),
    path('edit_log/<int:log_id>/', edit_log, name='edit_log'),
    path('delete_log/<int:log_id>/', delete_log, name='delete_log'),
    path('spending_chart/', spending_chart, name='spending_chart'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('budget_visualization/', budget_visualization, name='budget_visualization'),
    path('monthly_report/', monthly_report, name='monthly_report'),
    path('monthly_summary/', monthly_summary, name='monthly_summary'),
]