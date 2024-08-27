from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('list/', views.app_list, name='app_list'),
    path('new/', views.app_add, name='app_add'),
    path('<int:pk>/edit/', views.app_update, name='app_update'),
    path('<int:pk>/delete/', views.app_delete, name='app_delete'),
    path('run/<int:app_id>/', views.app_run, name='app_run'),


]
