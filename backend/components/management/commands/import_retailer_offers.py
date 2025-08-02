import json
from django.core.management.base import BaseCommand
from components.models import RetailerComponentOffer


def parse_availability(val):
    """Convert 'Out of Stock' and similar to boolean False, otherwise True."""
    if isinstance(val, bool):
        return val
    if val is None:
        return True  # Default to True if not specified
    val = str(val).strip().lower()
    return val in ["true", "1", "in stock", "available", "yes"]


class Command(BaseCommand):
    help = "Import scraped retailer offers from JSON"

    def add_arguments(self, parser):
        parser.add_argument(
            "json_path", type=str, help="Path to scraped_components.json"
        )

    def handle(self, *args, **options):
        json_path = options["json_path"]
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        count_created = 0
        count_updated = 0

        for item in data:
            obj, created = RetailerComponentOffer.objects.update_or_create(
                retailer=item["retailer"],
                retailer_name=item["retailer_name"],
                url=item["url"],
                defaults={
                    "price": item.get("price"),
                    "image_url": item.get("image_url"),
                    "availability": parse_availability(item.get("availability")),
                    "category": item.get("category", "Unknown"),
                    "model_name": item.get("model"),
                },
            )
            if created:
                count_created += 1
            else:
                count_updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import finished. {count_created} new offers imported, {count_updated} offers updated."
            )
        )
