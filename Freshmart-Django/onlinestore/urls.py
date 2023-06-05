from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('del/<int:pk>/', views.delete_item, name='delete_item'),
    path('update/<int:pk>/', views.update_item, name='update_item'),
    path('checkout/', views.checkout, name='checkout' ),
    path ('register/', views.register, name='register'),
    path('signin/', views.signin, name= 'signin'),
    path('logout', views.logout, name = 'logout'),

]