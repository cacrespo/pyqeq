from django.db import models
import random
import string

def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class Room(models.Model):
    STATUS_CHOICES = [
        ('WAITING', 'Waiting for players'),
        ('SUBMITTING', 'Submitting statements'),
        ('GUESSING', 'Guessing'),
        ('RESULTS', 'Results'),
    ]
    code = models.CharField(max_length=6, unique=True, default=generate_room_code)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='WAITING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.code} ({self.status})"

class Player(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='players')
    name = models.CharField(max_length=50)  # Este será el Pseudónimo
    real_name = models.CharField(max_length=100, default="") # Nombre real para la revelación
    is_bot = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    session_key = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} in {self.room.code}"

class Statement(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='statements')
    text = models.TextField()
    is_truth = models.BooleanField(default=False)
    # index 1, 2, 3 to identify them in the UI
    order = models.IntegerField(default=0)

    def __str__(self):
        type_str = "Truth" if self.is_truth else "Lie"
        return f"{self.player.name}: {self.text[:30]} ({type_str})"

class Guess(models.Model):
    voter = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='guesses_made')
    # The player whose statements are being guessed
    target_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='guesses_received')
    
    # The index (1, 2, or 3) of the statement the voter thinks is the truth
    truth_guess_index = models.IntegerField()
    # The player the voter thinks is the author of these statements
    author_guess = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='author_identifications')

    created_at = models.DateTimeField(auto_now_add=True)
