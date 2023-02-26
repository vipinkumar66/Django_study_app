from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('room/<int:pk>', views.room, name='room'),
    path('create_room/', views.create_room, name='create_room'),
    path('update_room/<int:pk>/', views.update_room, name='update_room'),
    path('delete_room/<int:pk>', views.delete_room, name='delete_room'),
    path('login_reg/', views.loginfunc, name='login_reg'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutfunc, name='logout'),
    # path('delete_message/<int:pk>', views.delete_message, name='delete_message'),
    path('profile/<str:username>', views.profilepage, name='profile'),

]