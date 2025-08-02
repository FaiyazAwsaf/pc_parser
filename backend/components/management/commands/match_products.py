from django.core.management.base import BaseCommand
from components.models import Component, RetailerComponentOffer
from rapidfuzz import fuzz, process
import re


def normalize_model_string(model):
    # Remove spaces and convert to uppercase for comparison
    if model:
        return re.sub(r"\s+", "", model).upper()
    return ""


class Command(BaseCommand):
    help = "Fuzzy match RetailerComponentOffer entries to Component DB, with exact model match first"

    def add_arguments(self, parser):
        parser.add_argument(
            "--category",
            type=str,
            help="Component category to match (e.g. CPU, GPU, Memory). If not set, matches all.",
        )
        parser.add_argument(
            "--threshold",
            type=int,
            default=85,
            help="Minimum fuzzy match score (0-100, default=85)",
        )

    def handle(self, *args, **options):
        threshold = options["threshold"]
        category = options["category"]

        qs = RetailerComponentOffer.objects.filter(component__isnull=True)
        if category:
            qs = qs.filter(category__iexact=category)
        offers = list(qs)
        if not offers:
            self.stdout.write(self.style.WARNING("No unmatched retailer offers found."))
            return

        if category:
            components = Component.objects.filter(category__name__iexact=category)
        else:
            components = Component.objects.all()
        component_lookup = [
            (comp.id, comp.name, (comp.brand or "")) for comp in components
        ]

        matched, unmatched = 0, 0

        for offer in offers:
            # -- MODEL NAME EXACT MATCH --
            model = offer.model_name
            matched_id = None
            if model:
                norm_model = normalize_model_string(model)
                for cid, name, brand in component_lookup:
                    # Normalize each word in the component name for comparison
                    name_words = re.findall(r"\w+", name)
                    for word in name_words:
                        if norm_model and norm_model == normalize_model_string(word):
                            matched_id = cid
                            offer.component_id = matched_id
                            offer.save()
                            matched += 1
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"EXACT MODEL MATCH: {offer.retailer_name} ({model}) --> {name} [EXACT]"
                                )
                            )
                            break
                    if matched_id:
                        break
            # -- FALLBACK TO FUZZY MATCH --
            if not matched_id:
                # Try to filter candidates by brand if present
                candidates = [
                    (cid, name)
                    for cid, name, brand in component_lookup
                    if not offer.retailer_name
                    or (brand and brand.lower() in offer.retailer_name.lower())
                ]
                if not candidates:
                    candidates = [(cid, name) for cid, name, _ in component_lookup]

                results = process.extractOne(
                    offer.retailer_name,
                    [name for cid, name in candidates],
                    scorer=fuzz.token_set_ratio,
                )
                if results and results[1] >= threshold:
                    idx = results[2]
                    matched_id = candidates[idx][0]
                    offer.component_id = matched_id
                    offer.save()
                    matched += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"FUZZY MATCH: {offer.retailer_name} --> {components.get(id=matched_id).name} [{results[1]}]"
                        )
                    )
                else:
                    unmatched += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"Unmatched: {offer.retailer_name} [Score: {results[1] if results else 'N/A'}]"
                        )
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"Done! Matched: {matched}, Unmatched: {unmatched} (Threshold={threshold})"
            )
        )
