# Generated by Django 4.2.6 on 2023-11-30 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_qualifiedchoice_questionnaire_alter_choice_votes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qualifiedchoice',
            old_name='choice',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='qualifiedchoice',
            old_name='valeur',
            new_name='s_valeur',
        ),
        migrations.RenameField(
            model_name='questionnaire',
            old_name='type',
            new_name='q_type',
        ),
        migrations.AlterField(
            model_name='choice',
            name='votes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.qualifiedchoice', verbose_name='Votez '),
        ),
    ]