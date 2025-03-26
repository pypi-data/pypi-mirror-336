from django.core.management import call_command
from django.core.management.base import BaseCommand

from marketmanager import __title__

# Eve Category IDs
MATERIAL = 4
SHIP = 6
MODULE = 7
CHARGE = 8
BLUEPRINT = 9
SKILLS = 16
COMMODITY = 17
DRONE = 18
IMPLANT = 20
ASTEROID = 25
APPAREL = 30
PLANETARY_INDUSTRY = 41
PLANETARY_COMMODITIES = 43
SPECIAL_EDITION_ASSETS = 63
STRUCTURES = 63
STRUCTURE_MODULE = 66
SKINS = 91


class Command(BaseCommand):
    help = "Preloads data required for this app from ESI"

    def handle(self, *args, **options):
        call_command(
            "eveuniverse_load_types",
            __title__,
            "--category_id",
            str(MATERIAL),
            "--category_id",
            str(SHIP),
            "--category_id",
            str(MODULE),
            "--category_id",
            str(CHARGE),
            "--category_id",
            str(BLUEPRINT),
            "--category_id",
            str(SKILLS),
            "--category_id",
            str(COMMODITY),
            "--category_id",
            str(DRONE),
            "--category_id",
            str(IMPLANT),
            "--category_id",
            str(ASTEROID),
            "--category_id",
            str(APPAREL),
            "--category_id",
            str(PLANETARY_INDUSTRY),
            "--category_id",
            str(PLANETARY_COMMODITIES),
            "--category_id",
            str(SPECIAL_EDITION_ASSETS),
            "--category_id",
            str(STRUCTURES),
            "--category_id",
            str(STRUCTURE_MODULE),
            "--category_id",
            str(SKINS),
        )
