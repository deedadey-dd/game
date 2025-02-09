from django.db import models
from django.contrib.auth import get_user_model
import random

User = get_user_model()

class Game(models.Model):
    LEVEL_CHOICES = (
        (1, 'Level 1'),
        (2, 'Level 2'),
        (3, 'Level 3'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')
    game_id = models.CharField(max_length=10, unique=True, editable=False)
    level = models.IntegerField(choices=LEVEL_CHOICES)
    selected_box = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.game_id:
            self.game_id = f"G-{random.randint(10000, 99999)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Game {self.game_id} - {self.user.username}"


class Box(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='boxes')
    number = models.IntegerField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_revealed = models.BooleanField(default=False)

    def __str__(self):
        return f"Box {self.number} - {'Revealed' if self.is_revealed else 'Hidden'}"


class Round(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='rounds')
    round_number = models.IntegerField()
    revealed_boxes = models.ManyToManyField(Box, blank=True)
    offer = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Game {self.game.game_id} - Round {self.round_number}"
