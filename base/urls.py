from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('', views.home, name='home'),
    path('new-game/', views.newGame, name='new-game'),
    path('win/', views.win, name='win'),
    path('lose/', views.lose, name='lose'),
    path('leaderboard/', views.leaderboard, name='leaderboard')
]