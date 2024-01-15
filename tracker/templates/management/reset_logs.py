from django.core.management.base import BaseCommand
from django.db.models import Sum
from tracker.models import LoggedExpense, MonthlyTotal
from django.utils import timezone


class Command(BaseCommand):
    help = 'Reset expenses on the 1st day of every month'

    def handle(self, *args, **options):
        total_spending = LoggedExpense.objects.filter(
            date__month__lte=timezone.now().month,
            date__year=timezone.now().year
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Store the total spending (you might want to save it to a model or a variable)
        monthly_total, created = MonthlyTotal.objects.get_or_create(
            month=timezone.now().month,
            year=timezone.now().year
        )
        monthly_total.total_spending = total_spending
        monthly_total.save()

        # Delete all logged spendings to reset expenses
        LoggedExpense.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Expenses reset successfully.'))