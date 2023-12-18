import fitz
from PIL import Image
from rest_framework import serializers

from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"


class ImageDetailSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    width = serializers.SerializerMethodField()
    height = serializers.SerializerMethodField()
    channels = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ("file_type", "location", "width", "height", "channels")

    def get_location(self, obj):
        return obj.file.url

    def get_width(self, obj):
        img = Image.open(obj.file)
        return img.width

    def get_height(self, obj):
        img = Image.open(obj.file)
        return img.height

    def get_channels(self, obj):
        img = Image.open(obj.file)
        return len(img.mode)


class PDFDetailSerialzer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    number_of_pages = serializers.SerializerMethodField()
    page_width = serializers.SerializerMethodField()
    page_height = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = (
            "file_type",
            "location",
            "number_of_pages",
            "page_width",
            "page_height",
        )

    def get_location(self, obj):
        return obj.file.url

    def get_number_of_pages(self, obj):
        file = fitz.open(obj.file.path)
        return file.page_count

    def get_page_width(self, obj):
        file = fitz.open(obj.file.path)
        page_width = file[0].rect.width
        return page_width

    def get_page_height(self, obj):
        file = fitz.open(obj.file.path)
        page_height = file[0].rect.height
        return page_height


class ImageRotateSerializer(serializers.Serializer):
    image_id = serializers.IntegerField(required=True)
    rotation_angle = serializers.FloatField(required=True)