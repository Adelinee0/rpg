from .views import SignUp
from django.urls import path, include

urlpatterns = [
    path('signup', SignUp.as_view(), name='signup'),
    path('', include('allauth.urls'), name='login'),
    #path('upgrade/', upgrade_user, name='account_upgrade'),
]