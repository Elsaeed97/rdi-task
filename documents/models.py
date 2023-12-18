from django.db import models
from model_utils import Choices
from django.utils.translation import gettext_lazy as _


class Document(models.Model):
    FILE_TYPE_CHOICES = Choices(("pdf", _("PDF")), ("image", _("Image")))

    file = models.FileField(_("File"), upload_to="files/")
    file_type = models.CharField(
        _("File Type"), max_length=10, choices=FILE_TYPE_CHOICES
    )

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")
