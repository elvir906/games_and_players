from django.core.exceptions import ObjectDoesNotExist

from .fastapi import Game, Player


def get_user_by_name_and_email(name: str, email: str):
    queryset = Player.objects.filter(name=name)
    if queryset:
        return queryset
    return Player.objects.filter(email=email)


def get_game_by_id(id: int):
    try:
        game = Game.objects.get(id=id)
    except ObjectDoesNotExist:
        return id
    return game


def get_player_by_id(id: int):
    try:
        player = Player.objects.get(id=id)
    except ObjectDoesNotExist:
        return id
    return player
