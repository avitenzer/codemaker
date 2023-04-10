from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('suggest', views.suggest, name='suggest'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('signup', views.signup_user, name='signup'),
    path('history', views.history, name='history'),
    path('delete_snippet/<question_id>', views.delete_snippet, name='delete_snippet'),
    path('images', views.images, name='images'),

]
