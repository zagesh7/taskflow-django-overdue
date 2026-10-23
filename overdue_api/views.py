import secrets
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from .services import mark_overdue_tasks

@require_GET
def health(request):
    return JsonResponse({'data': {'status': 'ok'}})

@csrf_exempt
@require_POST
def sync_overdue(request):
    expected = settings.OVERDUE_SYNC_TOKEN
    supplied = request.headers.get('X-Internal-Token', '')
    if not expected or not secrets.compare_digest(supplied, expected):
        return JsonResponse({'error': {'message': 'Unauthorized'}}, status=401)
    updated = mark_overdue_tasks()
    return JsonResponse({'data': {'updated': updated}})
