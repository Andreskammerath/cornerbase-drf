from rest_framework.routers import SimpleRouter
from game.views import BoardViewSet, GameViewSet, PlayerViewSet

router = SimpleRouter()
router.register('^games', GameViewSet, basename='games')
router.register('^boards', BoardViewSet, basename='boards')
router.register('^players', PlayerViewSet, basename='players')
urlpatterns = router.urls