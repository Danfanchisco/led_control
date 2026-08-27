from django.contrib.auth.views import LogoutView
from django.urls import path
from led_control import views

urlpatterns = [
    path('', views.index, name='index'),
    path('members/', views.members, name='members'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/led/<str:state>/', views.set_led, name='set_led'),
    path('api/led/', views.get_led_status, name='led_status'),
    path('dashboard/', views.dashboard, name='dashboard')
]