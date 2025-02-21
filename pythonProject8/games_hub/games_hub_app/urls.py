from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'games_hub_app'


urlpatterns = [
 path("", views.teste, name="teste"),
 path('<int:image_id>', views.image_detail, name='image_detail'),
 path('<int:image_id>/new_comment', views.new_comment, name='new_comment'),
 path("new_account", views.new_account, name="new_account"),
 path("login", views.loginview, name="loginview"),
 path("perfil", views.perfil, name="perfil"),
 path("upload", views.upload, name="upload"),
 path("logout", views.logout_view, name="logout_view"),
path("favourite_games", views.favourite_games, name="favourite_games"),
path("show_all_games", views.show_all_games, name="show_all_games"),
path("add_game", views.add_game, name="add_game"),
 path("erase_comment/<int:comment_id>/<int:image_id>/", views.erase_comment, name="erase_comment")
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
 urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)