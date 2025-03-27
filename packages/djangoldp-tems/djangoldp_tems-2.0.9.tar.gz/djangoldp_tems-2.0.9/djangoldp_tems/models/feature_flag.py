from django.utils.translation import gettext_lazy as _

from djangoldp_tems.models.__base_named_model import baseTEMSNamedModel


class FeatureFlag(baseTEMSNamedModel):
    class Meta(baseTEMSNamedModel.Meta):
        verbose_name = _("Feature Flag")
        verbose_name_plural = _("Feature Flags")
        rdf_type = "tems:FeatureFlag"
