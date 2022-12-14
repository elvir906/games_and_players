# Generated by Django 3.2.5 on 2022-09-16 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callback', '0005_rename_reated_date_game_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(blank=True, max_length=5, related_name='player_games', to='callback.Player'),
        ),
        migrations.AddConstraint(
            model_name='player',
            constraint=models.UniqueConstraint(fields=('name', 'email'), name='uniqueness_of_name_and_email'),
        ),
    ]
