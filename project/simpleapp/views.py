from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import New, Category
from .filters import PostFilter
from .forms import NewForm, UpdateForm
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.mail import send_mail

class NewList(ListView):
    model = New
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = New.objects.order_by('-created')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())
        return context


class NewDetailView(DetailView):
    template_name = 'new.html'
    queryset = New.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscribe'] = not Category.objects.filter(subscribers=self.request.user.pk)
        return context

    def get_object(self, queryset=None):
        obj = cache.get(f'news-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=queryset)
            cache.set(f'news-{self.kwargs["pk"]}', obj)
        return obj


class Search(ListView):
    model = New
    template_name = 'search.html'
    context_object_name = 'news'
    ordering = ['-created']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())
        return context


def mail_subscr(name, text, categ):
    cats = Category.objects.filter(category=categ)
    for cat in cats:
        subscs = Category.subscribers.all()
        for subsc in subscs:
            send_mail(
                subject=name,
                # имя клиента и дата записи будут в теме для удобства
                message=text,  # сообщение с кратким описанием проблемы
                from_email='Freezyyyyy@yandex.ru',
                # здесь указываете почту, с которой будете отправлять (об этом попозже)
                recipient_list=[subsc.user.email, ]
                # здесь список получателей. Например, секретарь, сам врач и т. д.
            )


class NewCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'new_create.html'
    form_class = NewForm
    success_url = '/news/'


class NewUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'new_update.html'
    form_class = UpdateForm
    success_url = '/news/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return New.objects.get(pk=id)


class NewDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    template_name = 'new_delete.html'
    queryset = New.objects.all()
    success_url = '/news/'


def subscribe_to_category(request, category_pk):
    category = Category.objects.get(pk=category_pk)
    category.subscribers.add(request.user)
    category.save()
    return redirect('/news/')


@login_required
def subscribe_me(request):
    new_id = int(request.path.split('/')[-3])
    post_categories = New.objects.get(id=new_id).category_set.all()

    for post_category in post_categories:
        category_pk = post_category.id
        subscribe_to_category(request, category_pk)
