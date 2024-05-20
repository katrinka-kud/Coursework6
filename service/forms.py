from django.forms import ModelForm, BooleanField

from service.models import Client, Messages, MailingSetup, Logs


class StyleFormMixin():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        exclude = ('owner',)


class MessagesForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Messages
        exclude = ('owner',)


class MailingSetupForm(StyleFormMixin, ModelForm):
    class Meta:
        model = MailingSetup
        fields = ('data_begin', 'data_end', 'period', 'clients')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        if self.request:
            user = self.request.user
            super().__init__(*args, **kwargs)
            self.fields['clients'].queryset = Client.objects.filter(owner=user)
        else:
            super().__init__(*args, **kwargs)


class MailingSetupModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = MailingSetup
        fields = ('is_active',)


class LogsForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Logs
        fields = '__all__'
