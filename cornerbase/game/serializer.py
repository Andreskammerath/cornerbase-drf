from rest_framework_json_api import serializers
from game.models import Board, Game, Player


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'name', 'created_by', 'status',)


class BoardSerializer(serializers.ModelSerializer):
    turn = serializers.IntegerField(read_only=True)
    class Meta:
        model = Board
        fields = ('id', 'number_of_cells', 'number_of_players', 'game', 'turn')


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'user', 'board')

    def validate_board_is_not_full(self, board):
        if board.players.count() > 1:
            return serializers.ValidationError(Board.BOARD_FULL_MSG)
        return board