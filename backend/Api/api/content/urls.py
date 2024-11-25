from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register(r'genre', GenreViewSet)
router.register(r'song', SongViewSet)
router.register(r'album', AlbumViewSet)
router.register(r'artist', ArtistViewSet)
router.register(r'playlist', PlaylistViewSet)
urlpatterns = []
urlpatterns += router.urls