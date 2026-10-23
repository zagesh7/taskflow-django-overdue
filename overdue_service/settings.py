import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
env_file = BASE_DIR / '.env'
if env_file.exists():
    for raw_line in env_file.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'local-only-change-this-key')
DEBUG = os.getenv('DJANGO_DEBUG', '0') == '1'
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
INSTALLED_APPS = ['django.contrib.contenttypes', 'django.contrib.staticfiles', 'overdue_api']
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware', 'django.middleware.common.CommonMiddleware']
ROOT_URLCONF = 'overdue_service.urls'
TEMPLATES = []
WSGI_APPLICATION = 'overdue_service.wsgi.application'
DATABASES = {'default': {'ENGINE':'django.db.backends.mysql','NAME':os.getenv('DB_NAME','taskflow'),'USER':os.getenv('DB_USERNAME', os.getenv('DB_USER','root')),'PASSWORD':os.getenv('DB_PASSWORD',''),'HOST':os.getenv('DB_HOST','127.0.0.1'),'PORT':os.getenv('DB_PORT','3306'),'OPTIONS':{'charset':'utf8mb4'}}}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
OVERDUE_SYNC_TOKEN = os.getenv('OVERDUE_SYNC_TOKEN', '')
