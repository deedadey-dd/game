from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Game, Box, Round
from .serializers import BoxSerializer, RoundSerializer, GameSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    
    @action(detail=True, methods=['post'])
    def reveal_number(self, request, pk=None):
        game = get_object_or_404(Game, pk=pk)
        if not game.is_active:
            return Response({"error": "Game is no longer active."}, status=400)
        
        revealed_numbers = request.data.get("numbers", [])
        if not isinstance(revealed_numbers, list) or len(revealed_numbers) == 0:
            return Response({"error": "Invalid numbers provided."}, status=400)
        
        boxes = Box.objects.filter(game=game, number__in=revealed_numbers, is_revealed=False)
        for box in boxes:
            box.is_revealed = True
            box.save()
        
        # Create a new round
        new_round = Round.objects.create(game=game, round_number=len(game.rounds.all()) + 1)
        new_round.revealed_boxes.set(boxes)
        new_round.save()
        
        return Response(GameSerializer(game).data)
    
    @action(detail=True, methods=['post'])
    def accept_offer(self, request, pk=None):
        game = get_object_or_404(Game, pk=pk)
        if not game.is_active:
            return Response({"error": "Game is no longer active."}, status=400)
        
        last_round = game.rounds.last()
        if last_round and last_round.offer:
            last_round.accepted = True
            last_round.save()
            game.is_active = False
            game.save()
            
        return Response(GameSerializer(game).data)
