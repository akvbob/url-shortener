import time

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect

from django.utils.translation import gettext as _

from django.views.generic import TemplateView
from django.views.generic import RedirectView

from .models import ShortLink

from .utils import given_url_exists, format_user_url, print_timelapse_table, get_algorithm
# Create your views here.




class ShortURLView(TemplateView):
    template_name = 'index.html'
    model = ShortLink

    def get_context_data(self, **kwargs):
        context = super(ShortURLView, self).get_context_data(**kwargs)

        context['title'] = _("URL shortener")

        return context


    def post(self, request, *args, **kwargs):
        long_url = request.POST.get("url", None)
        short_url = ""
        
        long_url = format_user_url(long_url)
        self.validate_long_url(long_url)
        

        algorithm = get_algorithm()
        start = time.time()
        short_url_key = algorithm.get_short_url()
        end = time.time()


        print_timelapse_table(algorithm, end, start)

        host = request.get_host()
        short_url = "{}/{}".format(host, short_url_key)

        self.model.objects.create(original_url=long_url, short_url=short_url_key)
        return render(request, "index.html" , {"title": _("URL shortener"), "short_url": short_url })


    def validate_long_url(self, long_url):

        if long_url is None:
            messages.error(self.request, 'Long URL is required!')
            return render(self.request, "index.html", {"title": _("URL shortener")})

        if not given_url_exists(long_url):
            messages.error(self.request, 'Website does not exist!')
            return render(self.request, "index.html", {"title": _("URL shortener")})




class RedirectToLongURLView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        short_url = self.kwargs.get("short_url")
        obj = get_object_or_404(ShortLink, short_url=short_url)
        
        return obj.original_url

