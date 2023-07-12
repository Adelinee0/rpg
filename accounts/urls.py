from .views import SignUp, ConfirmUser, user_login
from django.urls import path, include

urlpatterns = [
    #path('', include('allauth.urls'), name='login'),
    path('signup', SignUp.as_view(), name='signup'),
    path('confirm/', ConfirmUser.as_view(), name='confirm'), #страница, где вводишь код
    path('login/', user_login, name='code_login')

    #path('upgrade/', upgrade_user, name='account_upgrade'),
]