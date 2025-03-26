from django.utils.translation import gettext_lazy as _

from djangoldp_tems.models.__base_named_model import baseTEMSNamedModel


class TEMSOffer(baseTEMSNamedModel):
    class Meta(baseTEMSNamedModel.Meta):
        container_path = "/offers/"
        verbose_name = _("TEMS Offer")
        verbose_name_plural = _("TEMS Offers")
        rdf_type = "tems:Offer"
