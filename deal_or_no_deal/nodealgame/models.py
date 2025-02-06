from django.db import models
import uuid
from users.models import User
# Create your models here.


class GameSession(models.Model):
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    level = models.IntegerField(choices=[(1, "Level 1"), (2, "Level 2"), (3, "Level 3")])
    reserved_case = models.IntegerField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Case(models.Model):
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE)
    case_number = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    revealed = models.BooleanField(default=False)


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games")
    created_at = models.DateTimeField(auto_now_add=True)
    reserved_number = models.PositiveIntegerField()
    final_offer = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    accepted_offer = models.BooleanField(default=False)
    final_outcome = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Game for {self.user.username} on {self.created_at}"


class Round(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="rounds")
    round_number = models.PositiveIntegerField()
    revealed_numbers = models.JSONField()  # List of numbers revealed in this round
    offer_made = models.DecimalField(max_digits=12, decimal_places=2)
    offer_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Round {self.round_number} of Game {self.game.id}"

