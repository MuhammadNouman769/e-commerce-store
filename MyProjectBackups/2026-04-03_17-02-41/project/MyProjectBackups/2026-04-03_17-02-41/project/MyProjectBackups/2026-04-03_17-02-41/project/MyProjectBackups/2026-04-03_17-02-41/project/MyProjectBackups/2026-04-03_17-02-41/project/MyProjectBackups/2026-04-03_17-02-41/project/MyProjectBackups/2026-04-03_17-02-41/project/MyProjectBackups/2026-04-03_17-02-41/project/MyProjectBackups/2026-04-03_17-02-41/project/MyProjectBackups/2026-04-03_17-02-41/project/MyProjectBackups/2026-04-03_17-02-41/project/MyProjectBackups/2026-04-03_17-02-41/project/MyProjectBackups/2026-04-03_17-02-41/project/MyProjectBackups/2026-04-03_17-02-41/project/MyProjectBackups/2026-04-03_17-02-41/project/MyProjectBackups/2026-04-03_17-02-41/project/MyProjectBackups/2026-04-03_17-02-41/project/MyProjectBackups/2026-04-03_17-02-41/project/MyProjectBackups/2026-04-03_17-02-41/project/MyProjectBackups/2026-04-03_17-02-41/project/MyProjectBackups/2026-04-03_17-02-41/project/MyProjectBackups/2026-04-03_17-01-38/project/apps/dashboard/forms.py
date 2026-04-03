# from decimal import Decimal

# from django import forms
# from django.utils import timezone

# from apps.products.models import Category, Product, ProductVariant, Shop


# class ShopForm(forms.ModelForm):
#     class Meta:
#         model = Shop
#         fields = ["name", "domain", "description"]

#     def clean_domain(self):
#         domain = (self.cleaned_data.get("domain") or "").strip().lower()
#         if not domain:
#             raise forms.ValidationError("Domain is required.")
#         return domain


# class SellerProductForm(forms.Form):
#     title = forms.CharField(max_length=255)
#     description_html = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 4}))
#     vendor = forms.CharField(max_length=255, required=False)
#     product_type = forms.CharField(max_length=255, required=False)

#     status = forms.ChoiceField(choices=Product.ProductStatus.choices, initial=Product.ProductStatus.DRAFT)

#     categories = forms.ModelMultipleChoiceField(queryset=Category.objects.none(), required=False)

#     price = forms.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal("0.00"))
#     sku = forms.CharField(max_length=100, required=False)

#     def __init__(self, *args, **kwargs):
#         shop = kwargs.pop("shop", None)
#         super().__init__(*args, **kwargs)
#         if shop is not None:
#             self.fields["categories"].queryset = Category.objects.filter(shop=shop).order_by("name")

