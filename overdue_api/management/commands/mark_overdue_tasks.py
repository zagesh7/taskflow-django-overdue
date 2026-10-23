from django.core.management.base import BaseCommand
from overdue_api.services import mark_overdue_tasks

class Command(BaseCommand):
    help = 'Mark past-due, unfinished tasks as OVERDUE.'
    def handle(self, *args, **options):
        count = mark_overdue_tasks()
        self.stdout.write(self.style.SUCCESS(f'Marked {count} task(s) as OVERDUE.'))
