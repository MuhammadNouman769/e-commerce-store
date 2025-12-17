from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib import messages
from .forms import SignUpForm

class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("login")  # redirect after successful signup

    def form_valid(self, form):
        # Save the user
        form.save()
        messages.success(self.request, "Account created successfully. Please login.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Optional: handle invalid form
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
