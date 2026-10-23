# TaskFlow Django Overdue Service

A small Django service responsible for synchronizing overdue task state for TaskFlow. It uses the same MySQL database as the Laravel API and exposes a protected synchronization endpoint plus a health check.

## Responsibilities

- Find tasks whose due date has passed and update their overdue state
- Run the synchronization through a management command or protected HTTP endpoint
- Expose a health endpoint for deployment checks
- Map Laravel's existing `tasks` table through an unmanaged Django model; Laravel remains the schema owner

## Stack

Python 3.11+, Django, Gunicorn, MySQL (`mysqlclient`)

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and export the variables in your shell (PowerShell: `$env:NAME='value'`).
4. Set the MySQL connection variables to the same database used by Laravel and configure `OVERDUE_SYNC_TOKEN` to match Laravel's token.
5. Check configuration with `python manage.py check`.
6. Run locally with `python manage.py runserver 127.0.0.1:8001`.

Django does not create or migrate the shared application tables. Run Laravel migrations first.

## Endpoints and command

| Method | Path / command | Purpose |
| --- | --- | --- |
| `GET` | `/health/` | Health response |
| `POST` | `/api/tasks/sync-overdue/` | Protected overdue synchronization |
| command | `python manage.py mark_overdue_tasks` | Run the overdue sweep |

The synchronization endpoint requires the configured shared token. Keep the token private and use HTTPS in production.

## Wasmer deployment

`app.yaml` defines the Wasmer app and its 15-minute scheduled job. Connect this repository and configure Django's production secret, allowed hosts, shared MySQL credentials, and sync token in Wasmer's secret/environment settings. The scheduled job is configured to run every 15 minutes; adjust it to fit your deployment. This service must reach the same database as Laravel. No Django migration should be run against Laravel-owned tables.

Live service URL: _To be added after deployment._

## Related repositories

- [TaskFlow Laravel API](https://github.com/zagesh7/taskflow-laravel-api)
- [TaskFlow React frontend](https://github.com/zagesh7/taskflow-react-frontend)

