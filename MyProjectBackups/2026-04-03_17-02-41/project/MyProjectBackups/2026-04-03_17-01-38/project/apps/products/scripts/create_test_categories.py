# Run in Django shell: python manage.py shell
# or save as management command
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
from apps.products.models import Shop, Category

# ----- Step 1: Create Shops -----
shops_data = [
    {"name": "Main Shop", "domain": "mainshop.com"},
    {"name": "Test Shop", "domain": "testshop.com"},
]

shops = {}
for s in shops_data:
    shop_obj, _ = Shop.objects.get_or_create(name=s["name"], domain=s["domain"])
    shops[s["name"]] = shop_obj

# ----- Step 2: Define categories for each shop -----
categories_data = {
    "Main Shop": [
        {"name": "Electronics", "children": [
            {"name": "Mobiles", "children": [
                {"name": "Apple"},
                {"name": "Samsung"},
                {"name": "Xiaomi"}
            ]},
            {"name": "Laptops", "children": [
                {"name": "Dell"},
                {"name": "HP"},
                {"name": "Apple MacBook"}
            ]}
        ]},
        {"name": "Fashion", "children": [
            {"name": "Men", "children": [
                {"name": "Shoes"},
                {"name": "Shirts"}
            ]},
            {"name": "Women", "children": [
                {"name": "Dresses"},
                {"name": "Accessories"}
            ]}
        ]}
    ],
    "Test Shop": [
        {"name": "Books", "children": [
            {"name": "Fiction"},
            {"name": "Non-Fiction"},
            {"name": "Comics"}
        ]},
        {"name": "Toys", "children": [
            {"name": "Action Figures"},
            {"name": "Puzzles"},
            {"name": "Board Games"}
        ]}
    ]
}

# ----- Step 3: Recursive function to create categories -----
def create_categories(shop_obj, category_list, parent=None):
    for cat_data in category_list:
        cat_obj, _ = Category.objects.get_or_create(
            name=cat_data["name"],
            shop=shop_obj,
            parent=parent
        )
        children = cat_data.get("children", [])
        if children:
            create_categories(shop_obj, children, parent=cat_obj)

# ----- Step 4: Run the creation -----
for shop_name, cat_list in categories_data.items():
    if __name__ == "__main__":
        create_categories(shops[shop_name], cat_list)
print(" Test categories created successfully!")