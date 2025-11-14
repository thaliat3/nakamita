from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0007_actividadproyecto_unique"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ActividadProyecto",
        ),
    ]
