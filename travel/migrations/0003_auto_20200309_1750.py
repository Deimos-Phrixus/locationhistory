# Generated by Django 3.0.4 on 2020-03-09 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0002_auto_20200309_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travel',
            name='end_lat',
            field=models.DecimalField(decimal_places=20, max_digits=20),
        ),
        migrations.AlterField(
            model_name='travel',
            name='end_lng',
            field=models.DecimalField(decimal_places=20, max_digits=20),
        ),
        migrations.AlterField(
            model_name='travel',
            name='start_lat',
            field=models.DecimalField(decimal_places=20, max_digits=20),
        ),
        migrations.AlterField(
            model_name='travel',
            name='start_lng',
            field=models.DecimalField(decimal_places=20, max_digits=20),
        ),
        migrations.AlterField(
            model_name='traveltransit',
            name='lat',
            field=models.DecimalField(decimal_places=20, max_digits=20),
        ),
        migrations.AlterField(
            model_name='traveltransit',
            name='lng',
            field=models.DecimalField(decimal_places=20, max_digits=20),
        ),
        migrations.AlterField(
            model_name='travelwaypoints',
            name='lat',
            field=models.DecimalField(decimal_places=20, max_digits=20),
        ),
        migrations.AlterField(
            model_name='travelwaypoints',
            name='lng',
            field=models.DecimalField(decimal_places=20, max_digits=20),
        ),
    ]
