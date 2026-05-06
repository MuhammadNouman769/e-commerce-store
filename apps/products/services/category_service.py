from django.core.exceptions import ValidationError
from django.db import transaction

from apps.products.models import Category


class CategoryService:

    # ================= CREATE =================
    @staticmethod
    @transaction.atomic
    def create(validated_data):
        parent = validated_data.get("parent")

        #  Prevent self-parent (extra safety)
        if parent and parent.pk == validated_data.get("id"):
            raise ValidationError("Category cannot be its own parent")

        category = Category.objects.create(**validated_data)

        return category

    # ================= UPDATE =================
    @staticmethod
    @transaction.atomic
    def update(instance, validated_data):
        parent = validated_data.get("parent", instance.parent)

        #  Prevent self-parent
        if parent and parent == instance:
            raise ValidationError("Category cannot be parent of itself")

        #  Prevent circular hierarchy
        CategoryService._validate_no_cycle(instance, parent)

        #  Safe update
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    # ================= DELETE =================
    @staticmethod
    @transaction.atomic
    def delete(instance):
        #  Optional: block delete if children exist
        if instance.children.exists():
            raise ValidationError("Cannot delete category with subcategories")

        instance.delete()

    # ================= VALIDATION =================
    @staticmethod
    def _validate_no_cycle(instance, parent):
        """
        Prevent circular category structure
        """
        current = parent
        while current:
            if current == instance:
                raise ValidationError("Circular category structure detected")
            current = current.parent