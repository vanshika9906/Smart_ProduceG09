
from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
   # url(r'^order/(?P<order_id>\d+)/$',  views.statusdisplay, name='displaystatus'),
    path('order/<int:order_id>/', views.statusdisplay),
    path('', views.indexPage, name="index"),

    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('contact/', views.contactPage, name="contact"),
    path('generateQr/', views.generateQR, name="generateQR"),
    path('generateqr/', views.generateQR, name="generateqr"),
   # path('statusdisplay/<int:order_id>', views.statusdisplay, name="displaystatus"),

    path('home/', views.home, name="home"),
    path('products/', views.products, name='products'),
    path('customer/<str:pk_test>/', views.customer, name="customer"),

    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

]
