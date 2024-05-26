from django.forms import BooleanField
from django import forms

from email_newsletter.models import Newsletter, Client, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class NewsletterForm(StyleFormMixin, forms.Form, forms.ModelForm):

    start_data = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"],
        label="Время начала рассылки",
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control datetimepicker-input",
                "data-target": "#datetimepicker1",
                "label": "Время начала рассылки",
            }
        ),
    )

    end_data = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"],
        label="Время завершения рассылки",
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control datetimepicker-input",
                "data-target": "#datetimepicker1",
                "label": "Время завершения рассылки",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        # print(self.user)
        super(NewsletterForm, self).__init__(*args, **kwargs)

        if not self.user.is_superuser:
            self.fields['message'].queryset = Message.objects.filter(owner=self.user)
            self.fields['client'].queryset = Client.objects.filter(owner=self.user)

    class Meta:
        model = Newsletter
        exclude = (
            "status",
            "owner",
            "is_active",
        )


class NewsletterModeratorForm(StyleFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(NewsletterModeratorForm, self).__init__(*args, **kwargs)

        if not self.user.is_superuser:
            self.fields['message'].queryset = Message.objects.filter(owner=self.user)
            self.fields['client'].queryset = Client.objects.filter(owner=self.user)

    class Meta:
        model = Newsletter
        fields = ("is_active",)


class NewsletterModeratorOwnerForm(StyleFormMixin, forms.ModelForm):
    start_data = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"],
        label="Время начала рассылки",
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control datetimepicker-input",
                "data-target": "#datetimepicker1",
                "label": "Время начала рассылки",
            }
        ),
    )

    end_data = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"],
        label="Время завершения рассылки",
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control datetimepicker-input",
                "data-target": "#datetimepicker1",
                "label": "Время завершения рассылки",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(NewsletterModeratorOwnerForm, self).__init__(*args, **kwargs)

        if not self.user.is_superuser:
            self.fields['message'].queryset = Message.objects.filter(owner=self.user)
            self.fields['client'].queryset = Client.objects.filter(owner=self.user)

    class Meta:
        model = Newsletter
        exclude = (
            "status",
            "owner",
        )


class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        fields = (
            "name",
            "email",
            "message"
        )


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        fields = (
            "subject",
            "body"
        )
