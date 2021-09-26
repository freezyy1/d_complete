from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import New
from .filters import PostFilter
from .forms import NewForm, UpdateForm
from django.contrib.auth.mixins import PermissionRequiredMixin



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


class NewCreateView(CreateView):
    template_name = 'new_create.html'
    form_class = NewForm
    success_url = '/news/'


class NewUpdateView(UpdateView):
    template_name = 'new_update.html'
    form_class = UpdateForm
    success_url = '/news/'


    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return New.objects.get(pk=id)


class NewDeleteView(DeleteView):
    template_name = 'new_delete.html'
    queryset = New.objects.all()
    success_url = '/news/'

class blockcreate(PermissionRequiredMixin, NewCreateView):
    permission_required = ('shop.add_product', )
    # здесь должно быть ограничение на использование создания


class blockupdate(PermissionRequiredMixin, NewUpdateView):
    permission_required = ('shop.add_product', )
    # здесь должно быть ограничение на использование редактирования


class blockdelete(PermissionRequiredMixin, NewDeleteView):
    permission_required = ('shop.add_product', )
    # здесь должно быть ограничение на использование удаления
