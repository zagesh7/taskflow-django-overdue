from django.db import connection, transaction

@transaction.atomic
def mark_overdue_tasks():
    """Transition past-due tasks to OVERDUE, preserving completed tasks."""
    with connection.cursor() as cursor:
        cursor.execute("UPDATE tasks SET status = 'OVERDUE', updated_at = UTC_TIMESTAMP() WHERE due_date < UTC_DATE() AND status <> 'DONE' AND status <> 'OVERDUE'")
        return cursor.rowcount
