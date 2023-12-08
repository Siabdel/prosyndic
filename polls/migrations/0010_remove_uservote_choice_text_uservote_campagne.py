# Generated by Django 4.2.6 on 2023-11-30 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_rename_question_campagne_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uservote',
            name='choice_text',
        ),
        migrations.AddField(
            model_name='uservote',
            name='campagne',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.campagne'),
        ),
    ]