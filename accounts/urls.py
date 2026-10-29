from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('preferences/', views.preferences_view, name='preferences'),
    path('delete/', views.delete_account_view, name='delete_account'),
]
