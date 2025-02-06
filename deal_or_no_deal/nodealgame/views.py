from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Game, Round
from .serializers import GameSerializer, RoundSerializer
# Create your views here.



@api_view(['POST'])
def save_game_progress(request):
    user = request.user
    if not user.is_authenticated:
        return Response({"error": "Authentication required"}, status=401)
    
    # Create or Update Game
    reserved_number = request.data.get('reserved_number')
    final_offer = request.data.get('final_offer')
    accepted_offer = request.data.get('accepted_offer')
    final_outcome = request.data.get('final_outcome')

    game = Game.objects.create(
        user=user,
        reserved_number=reserved_number,
        final_offer=final_offer,
        accepted_offer=accepted_offer,
        final_outcome=final_outcome
    )
    
    # Save Round Details
    rounds_data = request.data.get('rounds', [])
    for round_data in rounds_data:
        Round.objects.create(
            game=game,
            round_number=round_data['round_number'],
            revealed_numbers=round_data['revealed_numbers'],
            offer_made=round_data['offer_made'],
            offer_accepted=round_data['offer_accepted']
        )

    return Response({"message": "Game progress saved successfully!"})

