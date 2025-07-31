from django.urls import path
from . import views

urlpatterns = [
    path(
        "categories/",
        views.ComponentCategoryList.as_view(),
        name="component-category-list",
    ),
    path(
        "category/<str:category_name>/",
        views.ComponentListByCategory.as_view(),
        name="component-list-by-category",
    ),
    path("<int:pk>/", views.ComponentDetail.as_view(), name="component-detail"),
]
