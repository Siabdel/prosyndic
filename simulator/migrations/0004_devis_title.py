# Generated by Django 4.2.6 on 2023-12-06 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0003_remove_devis_titre'),
    ]

    operations = [
        migrations.AddField(
            model_name='devis',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
