from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "0001_initial"),
        ("cities_light", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("street", models.TextField()),
                (
                    "city",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="cities_light.city"),
                ),
                (
                    "country",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="cities_light.country"),
                ),
                (
                    "province",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="cities_light.region"),
                ),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="users.user"),
                ),
            ],
            options={
                "abstract": False,
                "ordering": ["-created_at"],
            },
        ),
    ]

