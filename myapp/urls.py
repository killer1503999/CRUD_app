from django.urls import path,include
from .views import *

urlpatterns = [
    path('', factoryList.as_view()),
    path('<pk>/delete/', factoryDelete.as_view()),
    path('<pk>/', productList.as_view()),
    path('<pk>/<id>/', productDetails.as_view()),
    

]