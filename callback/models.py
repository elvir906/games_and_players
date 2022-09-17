from django.db import models
from django.db.models import constraints


class Player(models.Model):
    name = models.CharField(
        verbose_name='Имя игрока',
        max_length=54,
        default=""
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=54
    )
    created_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    update_date = models.DateTimeField(
        verbose_name='Дата изменения',
        auto_now=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'
        constraints = (constraints.UniqueConstraint(
            fields=['name', 'email'], name='uniqueness_of_name_and_email'
        ),)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=254, default="")
    players = models.ManyToManyField(
        Player, blank=True, related_name='player_games'
    )
    created_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    update_date = models.DateTimeField(
        verbose_name='Дата изменения',
        auto_now=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    def __str__(self):
        return self.name
