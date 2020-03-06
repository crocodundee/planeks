from django.conf import settings
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string

from users.models import User
from users.tokens import account_activation_token
from posts.models import Comment
from planeks.celery import app


@app.task
def send_confirm_email(domain, user_pk):
    user = User.objects.get(pk=user_pk)
    context = {
        'user': user.email,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user_pk)),
        'token': account_activation_token.make_token(user)
    }
    confirm_message = render_to_string('users/account_confirm_email.html', context=context)
    send_mail(
        subject='CONFIRM YOUR ACCOUNT',
        message=confirm_message,
        html_message=confirm_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True
    )


@app.task
def send_comment_info_mail(comment_id):
    comment = Comment.objects.get(id=comment_id)
    recipient_email = comment.post.author.email
    context = {
        'post_author': recipient_email,
        'comment': comment,
    }
    comment_message = render_to_string('posts/comment_email.html', context=context)
    send_mail(
        subject='Комментарии к публикации',
        message=comment_message,
        html_message=comment_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient_email],
        fail_silently=True
    )
