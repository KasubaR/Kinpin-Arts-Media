# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

KinpinArts is a Django 4.2 website for a creative media agency based in Zambia (timezone: Africa/Lusaka).

## Common Commands

**Local development** (defaults to `config.settings.dev`, SQLite):
```bash
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

**Run a single test:**
```bash
python manage.py test apps.core
python manage.py test apps.portfolio
python manage.py test apps.services
```

**Production server (SSH into cPanel):**
```bash
source /home/qualrijx/virtualenv/kinpinarts.com/3.9/bin/activate
cd ~/kinpinarts.com
export DJANGO_SETTINGS_MODULE=config.settings.prod
export DB_NAME=qualrijx_kinpinarts
export DB_USER=qualrijx_peter
export DB_PASSWORD=<password>
export DJANGO_SECRET_KEY=<key>
export DJANGO_ALLOWED_HOSTS=kinpinarts.com,www.kinpinarts.com
python manage.py migrate
```

## Architecture

### Settings
- `config/settings/base.py` — shared settings (SQLite, static/media paths)
- `config/settings/dev.py` — local dev; `manage.py` defaults to this
- `config/settings/prod.py` — production; requires env vars `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`. Uses MariaDB/MySQL with strict mode.

### Apps
All Django apps live under `apps/`:
- `apps/core` — contact inquiries, newsletter subscribers, testimonials, client logos
- `apps/portfolio` — projects with categories, scope items, images, and optional Behance URL
- `apps/services` — services with features; also used in global template context

### Global Template Context
`core/context_processors.py` (root-level, not inside `apps/`) injects `nav_links`, `social_links`, `services`, `behance_url`, and `nav_active_label` into every template. Templates live in `templates/` at the project root.

### Deployment
- Hosted on cPanel with Phusion Passenger
- Entry point: `passenger_wsgi.py` (sets `config.settings.prod`)
- Deploy by pushing to GitHub then pulling on the server
- Static files: `python manage.py collectstatic` (outputs to `staticfiles/`)
- Media uploads stored in `media/`
