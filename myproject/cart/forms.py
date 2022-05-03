from django import forms
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Booking
from django.core.validators import RegexValidator

mobile_regex = RegexValidator(
    regex=r'^\d{10,10}$', message="Phone number must be entered in the format: '999999999'. Exact 10 digits allowed."
)


class PurchaseForm(forms.Form):
    booking = forms.ModelChoiceField(queryset=Booking.objects.all(), label='Purchase Order')

    def __init__(self, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)

        self.fields["booking"] = forms.ModelChoiceField(
            queryset=Booking.objects.all(),
            to_field_name='booking_id',
            required=False,
            label='Booking ID'
        )


class AddCartForm(forms.Form):
    json = forms.CharField(widget=forms.Textarea)

    def clean_json(self):
        data = self.cleaned_data.get("json")
        import json
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise forms.ValidationError("Invalid format")
        return data


class CheckoutForm(forms.Form):
    student_name = forms.CharField(max_length=256)
    mobile_number = forms.CharField(max_length=256, validators=[mobile_regex])
    email_address = forms.EmailField()
    admission_number = forms.CharField(max_length=256)
    branch = forms.CharField(max_length=256, required=False)

    def send_mail(self, cart):
        from_email = 'rv4971254@gmail.com'
        subject = 'Your order is Packed'
        recipients = [cart.email_address]

        items = Booking.objects.filter(booking_id=cart.id)

        context = {
            'cart': cart,
            'items': items
        }

        html_content = render_to_string('order-packed.html', context)

        msg = EmailMultiAlternatives(subject=subject, from_email=from_email, to=recipients)
        msg.attach_alternative(html_content, "text/html")
        msg.send()




