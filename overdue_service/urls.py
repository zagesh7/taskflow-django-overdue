from django.urls import path
from overdue_api.views import health, sync_overdue
urlpatterns = [path('health/', health), path('api/tasks/sync-overdue/', sync_overdue)]
