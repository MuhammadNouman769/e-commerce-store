from django.db import migrations


def add_shop_owner_id_column(apps, schema_editor):
    """
    Fix for a previous fake-initial mismatch where `products_shop.owner_id`
    column did not exist in SQLite.
    """
    if schema_editor.connection.vendor != "sqlite":
        # This project uses SQLite in development. For other DBs, rely on normal migrations.
        return

    with schema_editor.connection.cursor() as cursor:
        cursor.execute("PRAGMA table_info(products_shop)")
        columns = [row[1] for row in cursor.fetchall()]

        if "owner_id" not in columns:
            schema_editor.execute("ALTER TABLE products_shop ADD COLUMN owner_id integer")

        # Keep OneToOneField semantics (best-effort) using a unique index.
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='index' AND name='products_shop_owner_id_unique'"
        )
        idx = cursor.fetchone()
        if not idx:
            schema_editor.execute(
                "CREATE UNIQUE INDEX products_shop_owner_id_unique ON products_shop (owner_id)"
            )


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_shop_owner_id_column, migrations.RunPython.noop),
    ]

