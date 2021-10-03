from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns=[

    path('',views.home,name="home"),
    
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('customer/<str:pk_test>/',views.customer,name="customer"),
    path('products/',views.products,name="products"),
    path('create_order/<int:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/',views.updateOrder,name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
]


