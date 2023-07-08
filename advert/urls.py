from django.urls import path

from . import views

urlpatterns = [
    path('', views.AdvertList.as_view(), name='advert_list'),
    path('<int:pk>', views.AdvertDetail.as_view(), name='advert_detail'), #в шаблоне при указании пути
    path('create/', views.AdvertCreate.as_view(), name='ad_create'),  #по этой ссылке работает создание объявления
    path('<int:pk>/update/', views.AdvertUpdate.as_view(), name='ad_update'),  #по этой ссылке работает редактирование объявления
    path('<int:pk>/delete/', views.AdvertDelete.as_view(), name='ad_delete'),  #по этой ссылке работает удаление объявления
    path('response/', views.MyResponses.as_view(), name='my_responses'),  #по этой ссылке работает просмотр всех откликов
    path('response/<int:pk>', views.ResponseDetail.as_view(), name='response'), #по этой ссылке работает просмотр отклика
    path('response/<int:pk>/accept', views.response_accept, name='response_accept'),#по этой ссылке работает принятие отклика
    path('response/<int:pk>/reject', views.response_reject, name='response_reject'), #по этой ссылке работает отклонение отклика
    path('response/<int:pk>/delete', views.ResponseDelete.as_view(),  name='response_delete'),  #по этой ссылке работает удаление отклика
    path('<int:pk>/response_create', views.ResponseCreate.as_view(), name='response_create'),  #по этой ссылке работает создание отклика

]