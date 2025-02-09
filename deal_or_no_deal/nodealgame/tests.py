from django.test import TestCase
from django.utils.timezone import now
from rest_framework.test import APIClient
from rest_framework import status
from nodealgame.models import Game, Round
from users.models import User  # Ensure you import from the correct app

class GameAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='test.user1',
            date_of_birth=now().date()  # Add this line
        )
        self.client.force_authenticate(user=self.user)
        self.game = Game.objects.create(user=self.user, level=1, selected_box=5)

    def test_create_game(self):
        response = self.client.post('/games/', {'level': 1, 'selected_box': 3})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reveal_numbers(self):
        response = self.client.post(f'/games/{self.game.id}/reveal_number/', {'numbers': [1, 2, 3]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_accept_offer(self):
        Round.objects.create(game=self.game, round_number=1, offer=500, accepted=False)
        response = self.client.post(f'/games/{self.game.id}/accept_offer/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
