from django.db import models
from django.utils.translation import gettext_lazy as _

from djangoldp_tems.models.__base_named_model import baseTEMSNamedModel
from djangoldp_tems.models.image import TEMSImage
from djangoldp_tems.models.offer import TEMSOffer
from djangoldp_tems.models.provider import TEMSProvider
from djangoldp_tems.models.provider_category import TEMSProviderCategory
from djangoldp_tems.models.service import TEMSService


class TEMSDataOffer(baseTEMSNamedModel):
    description = models.TextField(blank=True, null=True, default="")
    provider = models.ForeignKey(
        TEMSProvider,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="data_offers",
    )
    services = models.ManyToManyField(TEMSService, blank=True)
    offers = models.ManyToManyField(TEMSOffer, blank=True)
    image = models.ForeignKey(
        TEMSImage, blank=True, null=True, on_delete=models.SET_NULL
    )
    categories = models.ManyToManyField(TEMSProviderCategory, blank=True)

    class Meta(baseTEMSNamedModel.Meta):
        container_path = "/data-offers/"
        verbose_name = _("TEMS Data Offer")
        verbose_name_plural = _("TEMS Data Offers")

        serializer_fields = [
            "@id",
            "creation_date",
            "update_date",
            "name",
            "description",
            "offers",
            "image",
            "categories",
            "provider",
        ]
        nested_fields = ["categories", "offers", "image", "provider"]
        rdf_type = "tems:DataOffer"
