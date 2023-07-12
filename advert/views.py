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
    '''все объявления'''
    model = Advert
    ordering = '-createDate'
    template_name = 'advert.html'
    context_object_name = 'advert'
    paginate_by = 5

    def get_queryset(self):
        '''возвращает список отфильтрованных объявлений'''
        queryset = super().get_queryset()
        self.filterset = AdvertFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context

class AdvertDetail(DetailView):
    model = Advert
    template_name = 'ad.html'
    context_object_name = 'ad'

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
        myresp = Response.objects.filter(advertResponse__author=self.request.user)
        #юзер должен видеть только те отклики, которые прездназначались ему, значит aвтор=юзер
        context['myresp'] = myresp
        return context


class ResponseDetail(LoginRequiredMixin, DetailView):
    model = Response
    template_name = 'response.html'
    context_object_name = 'response'

def response_accept(request, pk):
    '''Через аргументы ФП можно передать пк отклика.
    Далее следует сделать запрос к БД, найти отклик по этому пк,
    изменить его статус и сохранить'''

    resp = Response.objects.get(id=pk)
    resp.status = True
    resp.save()
    return render(request, 'accept.html')


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
        '''для  автоматического заполнения таких полей, как advertResponse и authorResponse'''
        response = form.save(commit=False)
        response.advertResponse = Advert.objects.get(pk=self.request.resolver_match.kwargs['pk'])
        response.authorResponse = self.request.user
        return super().form_valid(form)



