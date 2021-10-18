from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import New, Category
from .filters import PostFilter
from .forms import NewForm, UpdateForm
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
import logging
from django.core.mail import send_mail


logger = logging.getLogger(__name__)

logger.debug("Hello! I'm debug in your app. Enjoy:)")
logger.info("Hello! I'm info in your app. Enjoy:)")
logger.warning("Hello! I'm warning in your app. Enjoy:)")
logger.error("Hello! I'm error in your app. Enjoy:)")
logger.critical("Hello! I'm critical in your app. Enjoy:)")



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


def mail_post(name, text, category):
    catygorys = Category.objects.filter(name=category)
    for category_ in catygorys:
        subscs = Category.subscribers.all()
        for subsc in subscs:
            send_mail(
                subject=name,
                message=text,
                from_email='Freezyyyyy@yandex.ru',
                recipient_list=[subsc.user.email, ]
            )


class NewCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_new',)
    template_name = 'new_create.html'
    form_class = NewForm
    success_url = '/news/'

    mail_post(New.post_name,
              New.content,
              New.category)


class NewUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('simpleapp.change_new',)
    template_name = 'new_update.html'
    form_class = UpdateForm
    success_url = '/news/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return New.objects.get(pk=id)


class NewDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.delete_new',)
    template_name = 'new_delete.html'
    queryset = New.objects.all()
    success_url = '/news/'



def subscribe_to_category(request, category_pk):
    category = Category.objects.get(pk=category_pk)
    category.subscribers.add(request.user)
    category.save()
    return redirect('/news/')


@login_required
def subscribe_me(request, pk):
    post = New.objects.get(id=pk)
    post_categories = post.category.all()
    for post_category in post_categories:
        category_pk = post_category.id
        category = Category.objects.get(pk=category_pk)
        category.subscribers.add(request.user)
        category.save()
    return redirect('/news/')



