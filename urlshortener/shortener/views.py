from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.translation import gettext as _
# Create your views here.



class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context['title'] = _("URL shortener"),

        return context