from rest_framework import generics
from .models import ComponentCategory, Component
from .serializers import ComponentCategorySerializer, ComponentSerializer


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
