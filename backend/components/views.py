from rest_framework import generics, status
from .models import ComponentCategory, Component, RetailerComponentOffer
from .serializers import (
    ComponentCategorySerializer,
    ComponentSerializer,
    RetailerComponentOfferSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ComponentCategoryList(generics.ListAPIView):
    queryset = ComponentCategory.objects.all()
    serializer_class = ComponentCategorySerializer


class ComponentListByCategory(generics.ListAPIView):
    serializer_class = ComponentSerializer

    def get_queryset(self):
        category_name = self.kwargs["category_name"]
        return Component.objects.filter(category__name__iexact=category_name)


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
