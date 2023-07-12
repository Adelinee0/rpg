from django.core.mail import send_mail

def mail_response_created(instanse, **kwargs):
    send_mail(
        subject='На ваше объявление откликнулись!',
        message=f'{instanse.advertResponse.author.username}, вам отклик от {instanse.authorResponse}!',
        from_email=None,
        recipient_list=[instanse.advertResponse.author.email]
    )

def mail_response_accept(instanse, **kwargs):
    send_mail(
        subject='Ваш отклик приняли!',
        message=f'{instanse.authorResponse.username}, ваш отклик к "{instanse.advertResponse.title}" приняли',
        from_email=None,
        recipient_list=[instanse.authorResponse.email]
    )

