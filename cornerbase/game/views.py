from django.shortcuts import render
from rest_framework_json_api import views
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


from game.models import Board, Cell, Game, Player
from game.serializer import BoardSerializer, GameSerializer, PlayerSerializer

class GameViewSet(views.ModelViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.all()
    # filterset_class = AssetSourceFilter
    # filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    # permission_classes = (IsAdminOrIsAuthenticatedAndReadOnly,)
    ordering = ("-created_at",)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, status=Game.TO_BEGIN)


class BoardViewSet(views.ModelViewSet):
    serializer_class = BoardSerializer
    queryset = Board.objects.all()
    # filterset_class = AssetSourceFilter
    # filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    # permission_classes = (IsAdminOrIsAuthenticatedAndReadOnly,)
    ordering = ("-game_id",)

    def perform_create(self, serializer): #validator that game's owner is the same that board's creator
        serializer.save(turn=0)
        board = serializer.instance
        Player.objects.create(user=self.request.user, board=board)
        cells = []
        for row in range(1, board.number_of_cells + 1):
            for column in range(1, board.number_of_cells + 1):
                cells.append(Cell(row=row, column=column, player=None, value=None, board=board))
        Cell.objects.bulk_create(cells)

class PlayerViewSet(views.AutoPrefetchMixin,
                    views.PreloadIncludesMixin,
                    views.RelatedMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):

    serializer_class = PlayerSerializer
    queryset = Player.objects.all()
    # filterset_class = AssetSourceFilter
    # filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    # permission_classes = (IsAdminOrIsAuthenticatedAndReadOnly,)
    ordering = ("-board_id",)

    def perform_create(self, serializer): #validator that game's owner is the same that board's creator
        serializer.save(user=self.request.user)
        player = serializer.instance
        board = player.board
        if board.players.count() == 2:
            cells = []
            cell = Cell.objects.get(row=1,column=2,board=board)
            cell.player = player
            cells.append(cell)
            cell = Cell.objects.get(row=2,column=1,board=board)
            cell.player = player
            cells.append(cell)
            Cell.objects.bulk_update(cells, ['player'])
            
            
