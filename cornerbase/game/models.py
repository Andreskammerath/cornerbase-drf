from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Game(models.Model):
    TO_BEGIN = 'TB'
    IN_DEVELOPMENT = 'InD'
    FINISHED = 'FI'

    GAME_STATUS_CHOICES = [
        (TO_BEGIN, 'To Begin'),
        (IN_DEVELOPMENT, 'In Development'),
        (FINISHED, 'Finished'),
    ]
    name = models.CharField(unique=True, max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="games_created", blank=True, null=True)
    # chats = models.ManyToManyField('Message') -> lo pongo en el message
    status = models.CharField(max_length=255, choices=GAME_STATUS_CHOICES, blank=False, null=False)


class Board(models.Model):
    "Board of the game"
    BOARD_FULL_MSG = "This board is full."
    number_of_cells = models.IntegerField(default=4)
    number_of_players = models.IntegerField(default=2)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="board")
    turn = models.PositiveSmallIntegerField(default=0)

class Player(models.Model):
    RED = 'RED'
    BLACK = 'BLACK'

    COLOR_CHOICES = [
        (RED, 'RED'),
        (BLACK, 'BLACK'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="players", blank=True, null=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="players")
    color = models.CharField(max_length=255, choices=COLOR_CHOICES, blank=True, null=True)


class Stack:
    """ Cards that belong to a player"""
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stack")
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="stacks")
    hand = models.CharField(max_length=255, blank=True, null=True)
    deck = models.CharField(max_length=255, blank=True, null=True)


class Cell(models.Model):
    """Cell from a board"""
    JUMP = 'J'
    DIAGONAL = 'D'
    PUSH = 'P'
    SWITCH = 'S'
    GAME_CARDS_CHOICES =  [
        (JUMP, 'JUMP'),
        (DIAGONAL, 'DIAGONAL'),
        (PUSH, 'PUSH'),
        (SWITCH, 'SWITCH')
    ]
    value = models.CharField(max_length=255, choices=GAME_CARDS_CHOICES, blank=True, null=True, default=None)
    player = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    row = models.IntegerField(blank=True, null=True)
    column = models.IntegerField(blank=True, null=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)