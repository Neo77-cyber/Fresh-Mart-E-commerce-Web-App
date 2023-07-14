from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('product-detail/<int:pk>/', views.productdetail, name= 'productdetail'),
    path('search/', views.search, name='search'),
    path('cart/', views.cart, name='cart'),
    path('del/<int:pk>/', views.delete_item, name='delete_item'),
    path('update/<int:pk>/', views.update_item, name='update_item'),
    path('check-out/', views.checkout, name='checkout' ),
    path('success/', views.completed_orders, name='completedorder'),
    path ('register/', views.register, name='register'),
    path('signin/', views.signin, name= 'signin'),
    path('create-profile/', views.createprofile, name= 'createprofile'),
    path('profile/', views.profile, name= 'profile'),
    path('logout', views.logout, name = 'logout'),
    path('about-us/', views.about_us, name= 'aboutus'),
    path('contact/', views.contact, name= 'contact'),
    path('become-a-rider/', views.become_a_rider, name= 'becomearider'),
    path('subscribe/', views.subscription, name= 'subscribe'),

    
    
    


]