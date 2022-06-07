from base_class.views import FormView
from base_class.views import ClassView

from .forms import LoginForm
from .forms import ChangePasswordForm
from .forms import ContactUSForm


def add_user_info(view, user):
    view.add("user", {
        "name": user.first_name if user.first_name else user.username,
        "username": user.username,
        "email": user.email,
        "superuser": user.is_superuser,
        "phone_number": user.phone_number,
    })


class LoginView(FormView):
    form_class = LoginForm

    def save(self, form):
        form.login(self.request)

    def success(self, form):
        user = form.user
        add_user_info(self, user)


class StatusView(ClassView):
    def process(self, request):
        self.add("error", False)

        if request.user.is_authenticated:
            self.add('loggedIn', True)
            add_user_info(self, request.user)
        else:
            self.add("loggedIn", False)


class LogOut(ClassView):
    def process(self, request):
        request = self.request
        from django.contrib.auth import logout

        logout(request)
        self.add("success")
        self.add("error", False)
        return self


class ChangePasswordView(FormView):
    form_class = ChangePasswordForm

    def form_params(self, kwargs):
        kwargs.update({'user': self.request.user})

    def save(self, form):
        form.save(self.request)


class ContactUs(FormView):
    form_class = ContactUSForm

    def save(self, form):
        name = form.cleaned_data.get('name')
        mobile = form.cleaned_data.get('mobile')
        subject = form.cleaned_data.get('subject')
        email = form.cleaned_data.get('email')
        message = form.cleaned_data.get('message')

        body_message = f"{message} \n\n Name: {name} \n Phone: {mobile} \n Email: {email}"
        from django.core.mail import EmailMessage
        email = EmailMessage(
            subject=subject, body=body_message,
            from_email='mission242022@gmail.com',
            to=[email],
            reply_to=[email]
        )
        email.send(fail_silently=False)

