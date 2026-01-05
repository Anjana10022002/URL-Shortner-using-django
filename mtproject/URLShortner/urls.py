from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_page, name='signup'),  
    path('', views.login_page, name='login'),
    path('home/', views.home_page, name='home'),
    path('add/', views.add_url, name='add'),
    path('urls/', views.url_list, name='url_list'),
    path('edit/<int:id>/', views.edit_url, name='edit_url'),
    path('delete/<int:id>/', views.delete_url, name='delete_url'),  
    path('logout/', views.logout_page, name='logout'),
    path('urls/<str:code>/', views.redirect_url, name='redirect_url'),  
]

