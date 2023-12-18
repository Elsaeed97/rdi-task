from django.urls import path

from .views import (
    ImageListView,
    ImageRetrieveDestroyView,
    PDFListView,
    PDFRetrieveDestroyView,
    ImageRotateView,
)

urlpatterns = [
    path("images/", ImageListView.as_view(), name="image-list"),
    path("pdfs/", PDFListView.as_view(), name="pdf-list"),
    path(
        "images/<int:pk>/",
        ImageRetrieveDestroyView.as_view(),
        name="image-detail-destroy",
    ),
    path("pdfs/<int:pk>/", PDFRetrieveDestroyView.as_view(), name="pdf-detail-destroy"),
    path("rotate/", ImageRotateView.as_view(), name="rotate-image"),
]
