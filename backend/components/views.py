from rest_framework import generics, status
from .models import ComponentCategory, Component, RetailerComponentOffer
from .serializers import (
    ComponentCategorySerializer,
    ComponentSerializer,
    RetailerComponentOfferSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q, Min, Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
import json


class ComponentCategoryList(generics.ListAPIView):
    queryset = ComponentCategory.objects.all()
    serializer_class = ComponentCategorySerializer


class ComponentListByCategory(generics.ListAPIView):
    serializer_class = ComponentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name", "brand", "model"]

    def get_queryset(self):
        category_name = self.kwargs["category_name"]
        return Component.objects.filter(category__name__iexact=category_name)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Apply filters based on query parameters
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")
        manufacturers = request.GET.getlist("manufacturer")
        search = request.GET.get("search", "")

        # Apply search filter
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(brand__icontains=search)
                | Q(model__icontains=search)
            )

        # Apply manufacturer filter
        if manufacturers:
            queryset = queryset.filter(brand__in=manufacturers)

        # Get components with their lowest prices
        components_data = []
        for component in queryset:
            component_data = ComponentSerializer(component).data

            # Get lowest price offer for this component
            lowest_offer = (
                RetailerComponentOffer.objects.filter(
                    component=component, price__isnull=False, availability=True
                )
                .order_by("price")
                .first()
            )

            if lowest_offer:
                component_data["lowest_price"] = lowest_offer.price
                component_data["lowest_price_retailer"] = lowest_offer.retailer_name
                component_data["lowest_price_url"] = lowest_offer.url
            else:
                component_data["lowest_price"] = None
                component_data["lowest_price_retailer"] = None
                component_data["lowest_price_url"] = None

            # Apply price filter if lowest price exists
            if min_price and component_data["lowest_price"]:
                if float(component_data["lowest_price"]) < float(min_price):
                    continue

            if max_price and component_data["lowest_price"]:
                if float(component_data["lowest_price"]) > float(max_price):
                    continue

            components_data.append(component_data)

        # Get filter options for the category
        category_components = Component.objects.filter(
            category__name__iexact=self.kwargs["category_name"]
        )

        # Get unique manufacturers
        manufacturers = list(
            category_components.exclude(brand__isnull=True)
            .exclude(brand="")
            .values_list("brand", flat=True)
            .distinct()
        )

        # Get price range
        offers = RetailerComponentOffer.objects.filter(
            component__in=category_components, price__isnull=False
        )
        price_range = offers.aggregate(min_price=Min("price"), max_price=Max("price"))

        # Extract specs for filtering (this will vary by category)
        specs_filters = self.extract_specs_filters(
            category_components, self.kwargs["category_name"]
        )

        return Response(
            {
                "results": components_data,
                "filters": {
                    "manufacturers": manufacturers,
                    "price_range": price_range,
                    "specs": specs_filters,
                },
            }
        )

    def extract_specs_filters(self, components, category_name):
        """Extract filterable specifications based on category"""
        specs_filters = {}

        if category_name.upper() == "CPU":
            # Extract CPU-specific filters
            core_counts = set()
            base_frequencies = set()
            max_frequencies = set()
            cache_sizes = set()
            graphics_options = set()

            for component in components:
                specs = component.specs
                if "core_count" in specs and specs["core_count"]:
                    try:
                        core_counts.add(int(specs["core_count"]))
                    except (ValueError, TypeError):
                        pass

                if "base_clock" in specs and specs["base_clock"]:
                    try:
                        # Extract numeric value from strings like "3.6 GHz"
                        base_freq = float(
                            str(specs["base_clock"])
                            .replace("GHz", "")
                            .replace("MHz", "")
                            .strip()
                        )
                        if "MHz" in str(specs["base_clock"]):
                            base_freq = base_freq / 1000  # Convert MHz to GHz
                        base_frequencies.add(base_freq)
                    except (ValueError, TypeError):
                        pass

                if "boost_clock" in specs and specs["boost_clock"]:
                    try:
                        boost_freq = float(
                            str(specs["boost_clock"])
                            .replace("GHz", "")
                            .replace("MHz", "")
                            .strip()
                        )
                        if "MHz" in str(specs["boost_clock"]):
                            boost_freq = boost_freq / 1000
                        max_frequencies.add(boost_freq)
                    except (ValueError, TypeError):
                        pass

                if "l3_cache" in specs and specs["l3_cache"]:
                    try:
                        cache = float(str(specs["l3_cache"]).replace("MB", "").strip())
                        cache_sizes.add(cache)
                    except (ValueError, TypeError):
                        pass

                if "graphics" in specs and specs["graphics"]:
                    graphics_options.add(str(specs["graphics"]))

            specs_filters = {
                "core_counts": sorted(list(core_counts)),
                "base_frequencies": sorted(list(base_frequencies)),
                "max_frequencies": sorted(list(max_frequencies)),
                "cache_sizes": sorted(list(cache_sizes)),
                "graphics_options": sorted(list(graphics_options)),
            }

        elif category_name.upper() == "MEMORY":
            # Extract Memory-specific filters
            capacities = set()
            types = set()
            frequencies = set()

            for component in components:
                specs = component.specs
                if "capacity" in specs and specs["capacity"]:
                    try:
                        capacity = int(str(specs["capacity"]).replace("GB", "").strip())
                        capacities.add(capacity)
                    except (ValueError, TypeError):
                        pass

                if "type" in specs and specs["type"]:
                    types.add(str(specs["type"]))

                if "speed" in specs and specs["speed"]:
                    try:
                        speed = int(str(specs["speed"]).replace("MHz", "").strip())
                        frequencies.add(speed)
                    except (ValueError, TypeError):
                        pass

            specs_filters = {
                "capacities": sorted(list(capacities)),
                "types": sorted(list(types)),
                "frequencies": sorted(list(frequencies)),
            }

        elif category_name.upper() == "MONITOR":
            # Extract Monitor-specific filters
            screen_sizes = set()
            resolutions = set()
            refresh_rates = set()
            panel_types = set()

            for component in components:
                specs = component.specs
                if "screen_size" in specs and specs["screen_size"]:
                    try:
                        size = float(str(specs["screen_size"]).replace('"', "").strip())
                        screen_sizes.add(size)
                    except (ValueError, TypeError):
                        pass

                if "resolution" in specs and specs["resolution"]:
                    resolutions.add(str(specs["resolution"]))

                if "refresh_rate" in specs and specs["refresh_rate"]:
                    try:
                        rate = int(str(specs["refresh_rate"]).replace("Hz", "").strip())
                        refresh_rates.add(rate)
                    except (ValueError, TypeError):
                        pass

                if "panel_type" in specs and specs["panel_type"]:
                    panel_types.add(str(specs["panel_type"]))

            specs_filters = {
                "screen_sizes": sorted(list(screen_sizes)),
                "resolutions": sorted(list(resolutions)),
                "refresh_rates": sorted(list(refresh_rates)),
                "panel_types": sorted(list(panel_types)),
            }

        return specs_filters


class ComponentDetail(generics.RetrieveAPIView):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer


class ComponentWithOffersView(APIView):
    def get(self, request, pk):
        try:
            component = Component.objects.get(pk=pk)
        except Component.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        offers = RetailerComponentOffer.objects.filter(component=component)
        return Response(
            {
                "component": ComponentSerializer(component).data,
                "offers": RetailerComponentOfferSerializer(offers, many=True).data,
            }
        )
