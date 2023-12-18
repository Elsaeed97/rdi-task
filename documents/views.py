from PIL import Image
from rest_framework import generics, status
from rest_framework.response import Response
import os
from .models import Document
from .serializers import (
    DocumentSerializer,
    ImageDetailSerializer,
    ImageRotateSerializer,
    PDFDetailSerialzer,
)
from django.conf import settings

class PDFListView(generics.ListAPIView):
    queryset = Document.objects.filter(file_type="pdf")
    serializer_class = DocumentSerializer


class ImageListView(generics.ListAPIView):
    queryset = Document.objects.filter(file_type="image")
    serializer_class = DocumentSerializer


class ImageRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Document.objects.filter(file_type="image")
    serializer_class = ImageDetailSerializer


class PDFRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Document.objects.filter(file_type="pdf")
    serializer_class = PDFDetailSerialzer


class ImageRotateView(generics.CreateAPIView):
    serializer_class = ImageRotateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image_id = serializer.validated_data["image_id"]
        rotation_angle = serializer.validated_data["rotation_angle"]

        try:
            image = Document.objects.get(id=image_id, file_type="image")
            image_path = image.file.path
            print(image_path)

            pil_image = Image.open(image_path)


            output_directory = os.path.join(settings.MEDIA_ROOT, "files")

            os.makedirs(output_directory, exist_ok=True)

            rotated_image_filename = f"rotated_{int(rotation_angle)}_{os.path.basename(image_path)}"
            rotated_image_path = os.path.join(output_directory, rotated_image_filename)

            rotated_image = pil_image.rotate(rotation_angle, expand=True)
            rotated_image.save(rotated_image_path)

            rotated_uploaded_file = Document.objects.create(
                file_type="image",
                file=os.path.relpath(rotated_image_path, settings.MEDIA_ROOT),
            )

            response_serializer = ImageDetailSerializer(rotated_uploaded_file)

            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except Document.DoesNotExist:
            return Response(
                {"error": "Image not found."}, status=status.HTTP_404_NOT_FOUND
            )