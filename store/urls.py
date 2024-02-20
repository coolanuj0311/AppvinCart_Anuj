from django.urls import path
from .import views
from store.views import StoreView
urlpatterns=[ 
    path("",views.store,name="store"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('update_item/',views.updateItem,name="update_item"),
    path('process_order/',views.processOrder,name="process_order"),
    path('StoreView/',StoreView.as_view(),name="StoreView"),
    path('new_arrivals/',views.new_arrivals,name="new_arrivals"),
]
