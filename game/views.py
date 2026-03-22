from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Room, Player, Statement, Guess
from django.http import HttpResponse

def get_current_player(request, room):
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key
    return Player.objects.filter(room=room, session_key=session_key).first()

def home(request):
    if not request.session.session_key:
        request.session.save()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            room = Room.objects.create()
            return redirect('room_detail', room_code=room.code)
    return render(request, 'game/home.html')
def join_room(request, room_code):
    room = get_object_or_404(Room, code=room_code.upper())
    if not request.session.session_key:
        request.session.save()
    
    if request.method == 'POST':
        player_name = request.POST.get('player_name')
        real_name = request.POST.get('real_name')
        if not player_name or not real_name:
            return render(request, 'game/join.html', {'room': room, 'error': 'Faltan campos'})
        
        session_key = request.session.session_key
        
        player, created = Player.objects.get_or_create(
            room=room,
            session_key=session_key,
            defaults={'name': player_name, 'real_name': real_name}
        )
        if not created:
            player.name = player_name
            player.real_name = real_name
            player.save()
            
        return redirect('room_detail', room_code=room.code)
    
    return render(request, 'game/join.html', {'room': room})

def room_detail(request, room_code):
    room = get_object_or_404(Room, code=room_code.upper())
    player = get_current_player(request, room)
    
    if not player and room.status == 'WAITING':
        return redirect('join_room', room_code=room.code)
    
    context = {
        'room': room,
        'player': player,
        'players': room.players.all(),
    }
    
    if room.status == 'WAITING':
        return render(request, 'game/lobby.html', context)
    elif room.status == 'SUBMITTING':
        players_submitted = Player.objects.filter(room=room, statements__isnull=False).distinct().count()
        total_players = room.players.count()
        
        # Auto-transition to guessing if everyone is ready
        if players_submitted >= total_players and total_players >= 2:
            room.status = 'GUESSING'
            room.save()
            return redirect('room_detail', room_code=room.code)
            
        has_submitted = Statement.objects.filter(player=player).exists()
        context.update({
            'has_submitted': has_submitted,
            'players_submitted': players_submitted,
            'total_players': total_players,
        })
        return render(request, 'game/submitting.html', context)
    
    elif room.status == 'GUESSING':
        guesses_done_ids = Guess.objects.filter(voter=player).values_list('target_player_id', flat=True)
        players_to_guess = room.players.exclude(id=player.id)
        
        # Check if everyone finished guessing
        total_players = room.players.count()
        total_guesses_expected = total_players * (total_players - 1)
        total_guesses_made = Guess.objects.filter(voter__room=room).count()
        
        if total_guesses_made >= total_guesses_expected and total_guesses_expected > 0:
            calculate_results(room)
            room.status = 'RESULTS'
            room.save()
            return redirect('room_detail', room_code=room.code)

        context.update({
            'players_to_guess': players_to_guess,
            'guesses_done': list(guesses_done_ids),
        })
        return render(request, 'game/guessing.html', context)
    
    elif room.status == 'RESULTS':
        context['results'] = room.players.order_by('-points')
        return render(request, 'game/results.html', context)
    
    return HttpResponse(f"Estado {room.status} no contemplado")

def calculate_results(room):
    # Reset points
    room.players.update(points=0)
    
    for guess in Guess.objects.filter(voter__room=room):
        actual_truth = guess.target_player.statements.get(is_truth=True)
        if guess.truth_guess_index == actual_truth.order:
            guess.voter.points += 10
        else:
            guess.target_player.points += 5
            
        if guess.author_guess == guess.target_player:
            guess.voter.points += 15
            
        guess.voter.save()
        guess.target_player.save()

def start_submitting(request, room_code):
    room = get_object_or_404(Room, code=room_code.upper())
    if room.status == 'WAITING':
        room.status = 'SUBMITTING'
        room.save()
    return redirect('room_detail', room_code=room.code)

def submit_statements(request, room_code):
    room = get_object_or_404(Room, code=room_code.upper())
    player = get_current_player(request, room)
    
    if request.method == 'POST':
        t1 = request.POST.get('t1')
        t2 = request.POST.get('t2')
        t3 = request.POST.get('t3')
        truth_index = int(request.POST.get('truth_index'))
        
        # Clear existing
        Statement.objects.filter(player=player).delete()
        
        texts = [t1, t2, t3]
        for i, text in enumerate(texts, 1):
            Statement.objects.create(
                player=player,
                text=text,
                is_truth=(i == truth_index),
                order=i
            )
        
        return redirect('room_detail', room_code=room.code)
    
    return redirect('room_detail', room_code=room.code)

def submit_guess(request, room_code, target_player_id):
    room = get_object_or_404(Room, code=room_code.upper())
    player = get_current_player(request, room)
    target_player = get_object_or_404(Player, id=target_player_id)
    
    if request.method == 'POST':
        truth_guess_index = int(request.POST.get('truth_guess_index'))
        author_guess_id = int(request.POST.get('author_guess_id'))
        author_guess = get_object_or_404(Player, id=author_guess_id)
        
        Guess.objects.update_or_create(
            voter=player,
            target_player=target_player,
            defaults={
                'truth_guess_index': truth_guess_index,
                'author_guess': author_guess
            }
        )
        
    return redirect('room_detail', room_code=room.code)
