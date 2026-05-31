import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.core.models import ClientLogo

LOGOS = [
    ('Africast',    'Client Logos_Africast.svg'),
    ('Amiran',      'Client Logos_Amiran.svg'),
    ('Bwacha MSS',  'Client Logos_Bwacha MSS.svg'),
    ('FC',          'Client Logos_FC.svg'),
    ('FF',          'Client Logos_FF.svg'),
    ('Frasmac',     'Client Logos_Frasmac.svg'),
    ('Lukanda',     'Client Logos_Lukanda.svg'),
    ('Mannock',     'Client Logos_Mannock.svg'),
    ('Metalock',    'Client Logos_Metalock.svg'),
    ('Mirai Media', 'Client Logos_Mirai Media.svg'),
    ('Ntumai',      'Client Logos_Ntumai.svg'),
    ('Qualitick',   'Client Logos_Qualitick.svg'),
    ('Skin Zm',     'Client Logos_Skin Zm.svg'),
    ('ZDA',         'Client Logos_ZDA.svg'),
    ('ZITHS',       'Client Logos_ZITHS.svg'),
    ('Zenith',      'Client Logos_Zenith.svg'),
]

SOURCE_DIR = settings.BASE_DIR / 'static' / 'images' / 'client-logos'
DEST_DIR = settings.MEDIA_ROOT / 'clients'


class Command(BaseCommand):
    help = 'Seed ClientLogo records from the existing static SVG files.'

    def handle(self, *args, **options):
        DEST_DIR.mkdir(parents=True, exist_ok=True)
        created = 0
        skipped = 0

        for order, (name, filename) in enumerate(LOGOS, start=1):
            if ClientLogo.objects.filter(name=name).exists():
                self.stdout.write(f'  skip  {name} (already exists)')
                skipped += 1
                continue

            src = SOURCE_DIR / filename
            if not src.exists():
                self.stdout.write(self.style.WARNING(f'  miss  {filename} not found in static dir'))
                continue

            dest_filename = filename
            dest = DEST_DIR / dest_filename
            shutil.copy2(src, dest)

            ClientLogo.objects.create(
                name=name,
                logo=f'clients/{dest_filename}',
                order=order,
            )
            self.stdout.write(self.style.SUCCESS(f'  add   {name}'))
            created += 1

        self.stdout.write(f'\nDone. {created} created, {skipped} skipped.')
