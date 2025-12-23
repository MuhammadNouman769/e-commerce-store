from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "phone", "role")  # required fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes and placeholders dynamically
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

        self.fields["email"].widget.attrs.update({"placeholder": "Enter email"})
        self.fields["phone"].widget.attrs.update({"placeholder": "Enter phone"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Enter password"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Confirm password"})
