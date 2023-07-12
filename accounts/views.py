from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import  authenticate, login
from django.views.generic.edit import CreateView, FormView
from django.http import HttpResponse

from django.shortcuts import redirect
from django.shortcuts import render

from accounts.forms import SignUpForm, CodeForm
from accounts.models import Profile


import random


class SignUp(CreateView):
    ''' page accounts/signup -> accounts/confirm'''
    model = User
    form_class = SignUpForm
    success_url = '/accounts/confirm' #на страницу подтверждения кода
    template_name = 'registration/signup.html'



    def post(self, request, *args, **kwargs):
        """здесь отправляем ещё inactive user  письмо с  его кодом"""
        if request.method == 'POST':
            username = request.POST['username']
            #password = request.POST['password']
            email = request.POST['email']
            #user = authenticate(request, username=username, password=password)
        print('я хотя бы существую')
        code = random.randint(100, 999)
        print(code)
        user = User.objects.get(username=username)
        print(user)
        profile = Profile.objects.create(user=user, code_of_confirm=code)
        profile.save()
        #us_id = list(Profile.objects.filter(code_of_confirm=code).values_list('user', flat=True))[:1]
        #us_id = int(*us_id)
        # print(us_id)
        # user = User.objects.get(id=us_id)
        # print(user)
        if user.is_active == False:
            print('SEEEEEND')
            send_mail(
                subject='Account email confirmation',
                message=f'Hi, your confirmation code: {code}',
                from_email=None,
                recipient_list=[email],
            )

        return super().post(self, request, *args, **kwargs)

    #def form_valid(self, form):
      # """здесь мы  получаем неактивированного ещё юзера,
       # создаем для него код и заносим связь
      #  юзер-код в таблицу Profile """
        #user = form.save(commit=False)
        #user.is_active = False
        #code = random.randint(100, 999)
        #user.save()
        #profile = Profile.objects.create(user=user, code_of_confirm=code)
        #profile.save()


       # return super().form_valid(form)


class ConfirmUser(FormView):
    ''' accounts/confirm -> accounts/login'''
    model = Profile
    form_class = CodeForm
    success_url = 'accounts/login'
    template_name = 'registration/confirm.html' #страница подтверждения кода


    def form_valid(self, form):
        """здесь  проверяем верно ли юзер ввел код,
        если верно - то меняем его статус на True для дальнейшего
        успешного входа и перенаправляем на логин"""

        profile = list(Profile.objects.all().values_list('code_of_confirm', flat=True))
        code = str(form.cleaned_data['code_of_confirm'])
        # берем код, который ввел сам юзер в форме
        #us_id = str(list(Profile.objects.filter(code_of_confirm=code).values_list('user', flat=True)))
        #user = User.objects.get(id=us_id)
        #if user.is_active==False:
          # print('I SEE YOU')

           # send_mail(
           #    subject='Account email confirmation',
            #    message=f'Hi, your confirmation code: {Profile.code_of_confirm}',
         #       from_email = None,
           #     recipient_list=[user.email],
            #    )

        if code in profile:
            self.request.user.is_active = True
            self.request.user.save()
            return super().form_valid(form)
        else:
            message = 'confirmation code is incorrect'
            return HttpResponse(message)


def user_login(request):

    '''здесь мы логиним юзера, если он активирован
    иначе же направляем на страницу регистрации'''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('Authenticated successfully')
            else:
                return redirect('accounts/signup')
        else:
            return HttpResponse('Invalid login')
    return render(request, 'registration/login.html')

#сначала надо активировать пользователя, только после этого он сможет войти в систему.

#Это значит, что перед вызовом функции authenticate
# надо из БД получить пользователя и проверить его статус.
# Если пользователь найден, но статус неактиве
# н - перенаправляем на страницу ввода кода.
# Можно также сгенерировать и отправить новый код
# этому пользователю. Если не найден - перенаправляем
# на страницу регистрации. И только
#если пользователь найден и активен,
# вызываем функцию authenticate.



