import os
import json
from django.core.management.base import BaseCommand
from components.models import Component, ComponentCategory

COMPONENT_MAP = {
    "cpu.json": "CPU",
    "gpu.json": "GPU",
    "memory.json": "Memory",
    "monitor.json": "Monitor",
    "motherboard.json": "Motherboard",
}


class Command(BaseCommand):
    help = "Import multiple component types from separate JSON files"

    def add_arguments(self, parser):
        parser.add_argument(
            "folder",
            type=str,
            help="Folder containing all component json files (e.g., data/)",
        )

    def handle(self, *args, **options):
        folder = options["folder"]
        added, updated = 0, 0
        for filename, category_name in COMPONENT_MAP.items():
            path = os.path.join(folder, filename)
            if not os.path.exists(path):
                self.stdout.write(
                    self.style.WARNING(f"File not found: {filename}, skipping")
                )
                continue

            with open(path, "r", encoding="utf-8") as f:
                items = json.load(f)
            cat_obj, _ = ComponentCategory.objects.get_or_create(name=category_name)

            for item in items:
                name = item.get("name")
                if name:
                    brand = name.split()[0]
                else:
                    brand = ""
                model = item.get("model", "")

                # Remove these from specs
                specs = {
                    k: v for k, v in item.items() if k not in ("name", "brand", "model")
                }

                obj, created = Component.objects.update_or_create(
                    name=name,
                    brand=brand,
                    model=model,
                    category=cat_obj,
                    defaults={"specs": specs},
                )
                if created:
                    added += 1
                else:
                    updated += 1
        self.stdout.write(
            self.style.SUCCESS(f"Import complete: {added} new, {updated} updated.")
        )
