from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
from .models import Advert, Response
from .filters import AdvertFilter, ResponseFilter
from .forms import AdvertForm, ResponseForm
from django.http import HttpResponse
from django.template import loader
from django.core.mail import send_mail


class AdvertList(ListView):
    model = Advert
    ordering = '-createDate'
    template_name = 'advert.html'
    context_object_name = 'advert'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdvertFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        add = Advert.objects.filter(author = self.request.user) #не нужно показывать с списке свои объявление
        context['add'] = add
        return context

class AdvertDetail(DetailView):
    model = Advert
    template_name = 'ad.html'
    context_object_name = 'ad' #в шаблоне это имя юзаем

class AdvertCreate(LoginRequiredMixin, CreateView):

    raise_exception = True
    form_class = AdvertForm
    model = Advert
    template_name = 'ad_create.html'

    def form_valid(self, form):
        advert = form.save(commit=False)
        advert.author = self.request.user
        return super().form_valid(form)

class AdvertUpdate(LoginRequiredMixin, UpdateView):

    raise_exception = True
    form_class = AdvertForm
    model = Advert
    template_name = 'ad_create.html'

class AdvertDelete(LoginRequiredMixin,  DeleteView):

    raise_exception = True
    model = Advert
    template_name = 'ad_delete.html'
    success_url = reverse_lazy('advert_list')

class MyResponses(LoginRequiredMixin, ListView):
    raise_exception = True
    model = Response
    ordering = '-createDate'
    template_name = 'my_responses.html'
    context_object_name = 'responses'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        author = Response.advertResponse.author
        myresp = Response.objects.filter(advertResponse__author=self.request.user)
        #юзер должен видеть только те отклики, которые прездназначались ему, значит aвтор=юзер
        context['myresp'] = myresp
        return context

    # Лучше сделать выборку в КП с помощью метода filter.
    # Текущего пользователя можно получить через обращение к запросу.
    # Например, для метода get_context_data: объявления = Объявление.объекты.фильтр(пользователь = self.requset.user)
    #Да, получаем в КП с помощью фильтрации выборку из БД (коллекцию)
    # и выводим её в шаблон через контекст. В шаблоне итерируемся по полученной из КП коллекции.



class ResponseDetail(LoginRequiredMixin, DetailView):
    model = Response
    template_name = 'response.html'
    context_object_name = 'response'

def response_accept(request, pk):
    #Через аргументы ФП можно передать пк отклика.
    # Далее следует сделать запрос к БД, найти отклик по этому пк, изменить его статус и сохранить.

    resp = Response.objects.get(id=pk)
    resp.status = True
    resp.save()
    return render(request, 'accept.html')

    #send_mail(
        #subject='Ваш отклик приняли!',
        #message=f'{user.username}, ваш отклик от',
        #from_email=None,  # будет использовано значение DEFAULT_FROM_EMAIL
        #recipient_list=[user.email],
    #)


def response_reject(request, pk):
  resp = Response.objects.get(id=pk)
  resp.status = False
  resp.save()
  return render(request, 'reject.html')



class ResponseDelete(LoginRequiredMixin, DeleteView):
    raise_exception = True
    model = Response
    template_name = 'response_delete.html'
    success_url = reverse_lazy('my_responses')



class ResponseCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = ResponseForm
    model = Response
    template_name = 'response_create.html'
    success_url = reverse_lazy('advert_list')
    #context_object_name = 'response'

    def form_valid(self, form):
        ''' для заполнения таких полей, как advertResponse и authorResponse,
        а также для отправки письма при создании отклика'''
        response = form.save(commit=False)
        response.advertResponse = Advert.objects.get(pk=self.request.resolver_match.kwargs['pk'])
        response.authorResponse = self.request.user
        #form.instance.post = Advert.object.get(pk=self.request.)
        #self.request.resolver_match.kwargs['pk']
        send_mail(
            subject='На ваше объявление откликнулись!',
            message=f'{response.advertResponse.author.username}, вам отклик от {response.authorResponse}! Вот он: "{response.text}" ',
            from_email=None,  # будет использовано значение DEFAULT_FROM_EMAIL
            recipient_list=[response.advertResponse.author.email],
        )
        return super().form_valid(form)



