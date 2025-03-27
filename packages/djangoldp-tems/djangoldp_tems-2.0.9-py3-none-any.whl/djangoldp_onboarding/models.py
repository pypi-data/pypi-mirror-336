from django.db import models

from djangoldp_tems.models.__base_model import baseTEMSModel


class RegisterOrganisation(baseTEMSModel):
    firstname = models.TextField(verbose_name="first name")
    lastname = models.TextField(verbose_name="last name")
    email = models.EmailField(verbose_name="email")
    organisation = models.TextField(verbose_name="organisation name")
    organisationAddress = models.TextField(
        verbose_name="organisation Address", null=True, blank=True
    )
    organisationRegistrationNumber = models.TextField(
        verbose_name="organisation Registration Number", null=True, blank=True
    )
    optin_register = models.BooleanField(
        verbose_name="Accepts Terms and Conditions",
        default=False,
    )

    class Meta:
        serializer_fields = [
            "@id",
            "created_at",
            "firstname",
            "lastname",
            "email",
            "organisation",
            "organisationAddress",
            "organisationRegistrationNumber",
            "optin_register",
        ]

    def __str__(self):
        return self.organisation
