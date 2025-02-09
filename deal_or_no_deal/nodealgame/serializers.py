from rest_framework import serializers
from .models import Game, Round, Box

class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ['number', 'is_revealed']

class RoundSerializer(serializers.ModelSerializer):
    revealed_boxes = BoxSerializer(many=True, read_only=True)
    
    class Meta:
        model = Round
        fields = ['round_number', 'revealed_boxes', 'offer', 'accepted']

class GameSerializer(serializers.ModelSerializer):
    rounds = RoundSerializer(many=True, read_only=True)
    
    class Meta:
        model = Game
        fields = ['game_id', 'level', 'selected_box', 'is_active', 'rounds']