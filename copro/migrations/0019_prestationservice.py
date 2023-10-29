# Generated by Django 4.2.6 on 2023-10-28 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copro', '0018_delete_prestationservice'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrestationService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Prestation de service')),
                ('description', models.TextField(blank=True, null=True)),
                ('code', models.CharField(max_length=10)),
            ],
        ),
    ]
