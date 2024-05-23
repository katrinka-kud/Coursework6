from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from blog.models import Blog
from service.forms import ClientForm, MailingSetupForm, MessagesForm, MailingSetupModeratorForm
from service.models import Client, MailingSetup, Messages, Logs


class HomeView(TemplateView):
    template_name = 'service/home.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        context_data['all'] = MailingSetup.objects.count()
        context_data['active'] = MailingSetup.objects.filter(status=MailingSetup.STATUS_START).count()
        context_data['clients_count'] = Client.objects.count()

        random_blogs = Blog.objects.order_by('?')[:3]
        blog_article_title = [blog.title for blog in random_blogs]
        blog_article_pk = [blog.pk for blog in random_blogs]
        context_data['articles'] = dict(zip(blog_article_title, blog_article_pk))

        return context_data


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    extra_context = {
        'title': 'Клиенты сервиса',
    }

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Client.objects.all()
        else:
            return Client.objects.filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    extra_context = {
        'title': 'Полная информация о клиенте',
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise Http404('Доступно только для владельца')


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('service:client_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('service:client_detail', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner == self.request.user or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404('Доступно только для владельца')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('service:home')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner == self.request.user or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404('Доступно только для владельца')


class MailingSetupListView(LoginRequiredMixin, ListView):
    model = MailingSetup
    form_class = MailingSetupForm
    extra_context = {
        'title': 'Рассылки сервиса',
    }

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset().order_by('data_begin')
        else:
            return super().get_queryset().filter(owner=self.request.user).order_by('data_begin')


class MailingSetupDetailView(LoginRequiredMixin, DetailView):
    model = MailingSetup

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise Http404('Доступно только для владельца')


class MailingSetupCreateView(LoginRequiredMixin, CreateView):
    model = MailingSetup
    form_class = MailingSetupForm
    success_url = reverse_lazy('service:mailingsetup_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessagesFormSet = inlineformset_factory(MailingSetup, Messages, extra=1, form=MessagesForm)
        if self.request.method == 'POST':
            context_data['formset'] = MessagesFormSet(self.request.POST)
        else:
            context_data['formset'] = MessagesFormSet()
        return context_data


class MailingSetupUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingSetup
    form_class = MailingSetupForm

    def get_success_url(self):
        return reverse('service:mailingsetup_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MailingSetupFormset = inlineformset_factory(MailingSetup, Messages, extra=1, form=MessagesForm)
        if self.request.method == 'POST':
            context_data['formset'] = MailingSetupFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MailingSetupFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingSetupForm
        if user.has_perm('can_disable_mailing'):
            return MailingSetupModeratorForm
        raise PermissionDenied


class MailingSetupDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingSetup
    success_url = reverse_lazy('service:home')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner == self.request.user or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404('Доступно только для владельца')


class LogsListView(LoginRequiredMixin, ListView):
    model = Logs
    extra_context = {
        'title': 'Лог рассылок',
    }

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        user = self.request.user
        send_list = MailingSetup.objects.filter(owner=user).first()
        if user.is_superuser:
            context_data['all'] = Logs.objects.count()
            context_data['success'] = Logs.objects.filter(is_done=True).count()
            context_data['error'] = Logs.objects.filter(is_done=False).count()
        else:
            user_logs = Logs.objects.filter(send_list=send_list)
            context_data['all'] = user_logs.count()
            context_data['success'] = user_logs.filter(is_done=True).count()
            context_data['error'] = user_logs.filter(is_done=False).count()
        return context_data
