from django.contrib import admin
from .models import Game, Box, Round


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('game_id', 'user', 'level', 'is_active', 'created_at')
    search_fields = ('game_id', 'user__username')


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('game', 'number', 'amount', 'is_revealed')
    search_fields = ('game__game_id',)


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ('game', 'round_number', 'offer', 'accepted')
