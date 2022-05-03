from .views import LoginView
from .views import LogOut
from .views import ChangePasswordView
from .views import StatusView
from .views import ContactUs


urlpatterns = [
    StatusView.url('status/', 'auth-status'),
    LoginView.url('login/', 'auth-login'),
    LogOut.url('logout/', 'auth-logout'),
    ChangePasswordView.url('change-password/', 'change-password'),
    ContactUs.url('contact-us/', 'contact-us'),

]
