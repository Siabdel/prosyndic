# Generated by Django 4.2.6 on 2023-10-24 16:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Etude',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Residence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('photo', models.ImageField(upload_to='media/')),
                ('adresse', models.CharField(blank=True, max_length=200, null=True)),
                ('comment', models.TextField(null=True)),
            ],
            options={
                'verbose_name': 'Residence',
                'verbose_name_plural': 'Residences',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='LigneDeCandidature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('societe', models.CharField(max_length=100)),
                ('contacte', models.CharField(max_length=100)),
                ('telephone', models.CharField(max_length=50, verbose_name='Téléphone')),
                ('recommande_par', models.CharField(max_length=100)),
                ('candidat', models.BooleanField(verbose_name='Ajouter a la liste des Candidats')),
                ('comment', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('etude', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='copro.etude')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('pj_file', models.FileField(blank=True, null=True, upload_to='upload/')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'indexes': [models.Index(fields=['content_type', 'object_id'], name='copro_docum_content_320986_idx')],
            },
        ),
    ]