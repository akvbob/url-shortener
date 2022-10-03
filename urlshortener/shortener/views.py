import time

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect

from django.utils.translation import gettext as _

from django.views.generic import TemplateView
from django.views.generic import RedirectView

from .models import ShortLink

from .utils import givenURLExists, generateUniqueUrlKey, formatUserURL
# Create your views here.




class ShortURLView(TemplateView):
    template_name = 'index.html'


    def get_context_data(self, **kwargs):
        context = super(ShortURLView, self).get_context_data(**kwargs)

        context['title'] = _("URL shortener")

        return context


    def post(self, request, *args, **kwargs):
        long_url = request.POST.get("url", None)
        short_url = ""
        
        long_url = formatUserURL(long_url)
        self.validate_long_url(long_url)
        
        start = time.time()
        short_url_key = self.generate_short_url()
        end = time.time()

        algorithm = 'random_url'
        time_lapsed = end - start
        short_url_count = ShortLink.objects.count()
        print('|-----------------------------------------------------|')
        print('|    ALGORITHM     | DB ROWS |    TIME                |')
        print('|-----------------------------------------------------|')
        print('|    {algorithm}    |   {rows}    | {time} '.format(algorithm=algorithm, rows=short_url_count, time=time_lapsed))
       

        host = request.get_host()
        
        short_url = "{}/{}".format(host, short_url_key)

        ShortLink.objects.create(original_url=long_url, short_url=short_url_key)
        return render(request, "index.html" , {"title": _("URL shortener"), "short_url": short_url })


    def short_url_already_exists(self, url):
        return ShortLink.objects.filter(short_url=url).exists()


    def generate_short_url(self):
        short_url_key = ""
        while True:
            short_url_key = generateUniqueUrlKey()
            if not self.short_url_already_exists(short_url_key):
                return short_url_key
    

    def validate_long_url(self, long_url):
        if long_url is None:
            messages.error(self.request, 'Long URL is required!')
            return render(self.request, "index.html", {"title": _("URL shortener")})
        if not givenURLExists(long_url):
            messages.error(self.request, 'Website does not exist!')
            return render(self.request, "index.html", {"title": _("URL shortener")})




class LocateToLongURLView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        short_url = self.kwargs.get("short_url")
        obj = get_object_or_404(ShortLink, short_url=short_url)
        
        return obj.original_url

