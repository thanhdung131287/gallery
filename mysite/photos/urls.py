from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('password/change_password/', auth_views.PasswordChangeView.as_view(template_name='photos/change_password.html', success_url='/password/done/'), name='change_password'),
    path('password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='photos/change_password_done.html'), name='change_password_done'),
    path('gallery/', views.gallery, name='gallery'),
    path('photo/<str:pk>/', views.viewPhoto, name='photo'),
    path('add/', views.addPhoto, name='add'),

]

