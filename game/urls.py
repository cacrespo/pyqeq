from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:room_code>/', views.room_detail, name='room_detail'),
    path('room/<str:room_code>/join/', views.join_room, name='join_room'),
    path('room/<str:room_code>/start/', views.start_submitting, name='start_submitting'),
    path('room/<str:room_code>/submit/', views.submit_statements, name='submit_statements'),
    path('room/<str:room_code>/guess/<int:target_player_id>/', views.submit_guess, name='submit_guess'),
]
