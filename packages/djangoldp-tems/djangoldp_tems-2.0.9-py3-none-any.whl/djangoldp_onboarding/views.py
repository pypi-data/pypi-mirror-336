from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import OrganisationRegistrationForm
from .models import RegisterOrganisation


class OrganisationCreateView(CreateView):
    model = RegisterOrganisation
    form_class = OrganisationRegistrationForm
    template_name = "onboarding_form.html"
    success_url = reverse_lazy("onboarding-success")

    def form_valid(self, form):
        return super().form_valid(form)
