from django.db import models
class Task(models.Model):
    id = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=20)
    due_date = models.DateField()
    class Meta:
        managed = False
        db_table = 'tasks'
