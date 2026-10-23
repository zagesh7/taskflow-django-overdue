from django.db import connection, transaction

def mark_overdue_tasks():
    """Transition past-due tasks to OVERDUE, preserving completed tasks."""
    with transaction.atomic():
        with connection.cursor() as cursor:
            cursor.execute("UPDATE tasks SET status = 'OVERDUE', updated_at = UTC_TIMESTAMP() WHERE due_date < UTC_DATE() AND status <> 'DONE' AND status <> 'OVERDUE'")
            return cursor.rowcount
