from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('client/', views.client, name='client'),
    path('why/', views.why, name='why'),
    path('pricing/', views.pricing, name='pricing'),
    path('all_parking/', views.all_parking, name='all_parking'),
    path('all_parking/<str:parking_id>', views.parking_detail, name='parking_detail'),
    path('all_parking/book_form/<int:slot_id>/', views.book_form, name='book_form'),
    path('all_parking/book_form/create', views.place_booking, name='place_booking'),
    path('booked', views.PaymentPageView.as_view(), name='booked'),
    path('charge/', views.charge, name='charge'),
    path('payment/', views.payment_home, name='payment_home'),
    
]


