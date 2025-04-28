from django.urls import path, include
from .views import budget_list, expenses, add_budget, add_expense, delete_budget, delete_expense
from .views import welcome_screen, register_view, login_view, profile,budget_data_api, edit_expense

urlpatterns = [
    path('', welcome_screen, name='welcome_screen'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
    path('budgets/', budget_list, name='budget_list'),
    path('api/budget_data/', budget_data_api, name='budget_data_api'),  # New API endpoint
    path('expenses/<int:budget_id>/', expenses, name='expenses'),
    path('add_budget/', add_budget, name='add_budget'),
    path('add_expense/<int:budget_id>/', add_expense, name='add_expense'),
    path('edit_expense/<int:expense_id>/', edit_expense, name='edit_expense'),

    path('delete_budget/<int:budget_id>/', delete_budget, name='delete_budget'),
    path('delete_expense/<int:budget_id>/<int:expense_id>/', delete_expense, name='delete_expense'),
    path('accounts/', include('django.contrib.auth.urls')),
]