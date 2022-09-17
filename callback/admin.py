from django.contrib import admin

from . models import Game, Player


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_date', 'update_date')
    search_fields = ('name', 'email')


class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_players', 'created_date', 'update_date')
    search_fields = ('name',)

    def get_players(self, obj):
        return ", ".join([player.name for player in obj.players.all()])

    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 5:
            return False
        else:
            return True


admin.site.register(Player, PlayerAdmin)
admin.site.register(Game, GameAdmin)
