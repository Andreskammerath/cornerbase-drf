import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
import json

from game.models import Board, Cell, Game, Player


CONTENT_TYPE = "application/vnd.api+json; charset=utf-8"
HEADERS = {"HTTP_ACCEPT": CONTENT_TYPE}


User = get_user_model()


@pytest.fixture
def create_user():
    return User.objects.create(username="Andy")


@pytest.fixture
def create_2_users(create_user):
    return create_user, User.objects.create(username="Woody")


@pytest.mark.django_db
def test_create_game(create_user):
    user = create_user
    data = {
        "data": {
            "type": "Game",
            "attributes": {
                "name": "Game 1",
                "created_by": {"id": user.id, "type": "User"},
                "status": Game.TO_BEGIN
            },
        }
    }
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post('/api/v1/games/', data=json.dumps(data), content_type=CONTENT_TYPE, **HEADERS)
    assert response.status_code == 201
    assert response.data["created_by"]["id"] == str(user.id)
    assert response.data["name"] == "Game 1"
    assert response.data["status"] == Game.TO_BEGIN


@pytest.mark.django_db
def test_create_board(create_user):
    user = create_user
    game = Game.objects.create(name="Game 1", status=Game.TO_BEGIN, created_by=user)
    data = {
        "data": {
            "type": "Board",
            "attributes": {
                "game": {"id": game.id, "type": "Game"},
                "number_of_cells": 4,
                "number_of_players": 2
            },
        }
    }
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post('/api/v1/boards/', data=json.dumps(data), content_type=CONTENT_TYPE, **HEADERS)
    assert response.status_code == 201
    assert response.data["game"]["id"] == str(game.id)
    assert response.data["number_of_cells"] == 4
    assert response.data["number_of_players"] == 2
    assert Player.objects.first().user.id == user.id
    board = Board.objects.first()
    assert board.players.all()[0].user == user # board's creator is joined to the game by default
    assert Cell.objects.filter(board=board).count() == board.number_of_cells ** 2


@pytest.mark.django_db
def test_join_to_game_succesfully(create_2_users):
    user, user2 = create_2_users
    game = Game.objects.create(name="Game 1", status=Game.TO_BEGIN, created_by=user)
    board = Board.objects.create(game=game, turn=0, number_of_cells=4, number_of_players=2)
    Player.objects.create(user=user, board=board)
    data = {
        "data": {
            "type": "Player",
            "attributes": {
                "board": {"id": board.id, "type": "Board"},
                "user": {"id": user2.id, "type": "User"}
            },
        }
    }
    client = APIClient()
    client.force_authenticate(user=user2)
    response = client.post('/api/v1/players/', data=json.dumps(data), content_type=CONTENT_TYPE, **HEADERS)
    assert response.status_code == 201
    assert Player.objects.count() == 2
    assert Board.objects.first().players.all()[0].user == user
    assert Board.objects.first().players.all()[1].user == user2


@pytest.mark.django_db
def test_try_to_join_to_full_board(create_2_users):
    user, user2 = create_2_users
    user3 = User.objects.create(username="Buzz")
    game = Game.objects.create(name="Game 1", status=Game.TO_BEGIN, created_by=user)
    board = Board.objects.create(game=game, turn=0, number_of_cells=4, number_of_players=2)
    Player.objects.create(user=user, board=board)
    Player.objects.create(user=user2, board=board)

    data = {
        "data": {
            "type": "Player",
            "attributes": {
                "board": {"id": board.id, "type": "Board"},
                "user": {"id": user3.id, "type": "User"}
            },
        }
    }
    client = APIClient()
    client.force_authenticate(user=user2)
    response = client.post('/api/v1/players/', data=json.dumps(data), content_type=CONTENT_TYPE, **HEADERS)
    assert response.status_code == 400
    assert response["data"] == {}
