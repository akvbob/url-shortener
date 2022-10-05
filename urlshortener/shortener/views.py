import time

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib import messages

from django.utils.translation import gettext as _

from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.http import HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect

from .models import ShortLink

from .utils import given_url_exists, format_user_url, print_timelapse_table, get_algorithm, create_shortURL_statistics
from .utils import APP_TITLE
# Create your views here.



class ShortURLView(TemplateView):
    template_name = 'index.html'
    model = ShortLink

    def get_context_data(self, **kwargs):
        context = super(ShortURLView, self).get_context_data(**kwargs)

        context['title'] = APP_TITLE

        return context


    def post(self, request, *args, **kwargs):
        long_url = request.POST.get("url", None)
        short_url = ""
        
        self.validate_long_url(long_url)
        
        algorithm = get_algorithm()
        start = time.time()
        short_url_key = algorithm.get_short_url(long_url)
        end = time.time()

        print_timelapse_table(algorithm, end, start)

        host = request.get_host()
        short_url = "{}/redirect/{}".format(host, short_url_key)

        self.model.objects.create(original_url=long_url, short_url=short_url_key)
        return render(request, self.template_name , {"title": APP_TITLE, "short_url": short_url })


    def validate_long_url(self, long_url):
        if long_url is None or long_url == '':
            messages.error(self.request, _('Long URL is required!'))
            return render(self.request, self.template_name, {"title": APP_TITLE })
        
        long_url = format_user_url(long_url)
        if not given_url_exists(long_url):
            messages.error(self.request, _('Website does not exist!'))
            return render(self.request, self.template_name, {"title": APP_TITLE})




class RedirectToLongURLView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        short_url = self.kwargs.get("short_url")
        obj = get_object_or_404(ShortLink, short_url=short_url)
        
        if obj.can_be_opened:
            create_shortURL_statistics(self.request, obj)
            return obj.original_url

        messages.error(self.request, _('URL is not active at the moment!'))
        return None

    
    def get(self, request, *args, **kwargs):
        url = self.get_redirect_url(*args, **kwargs)
        
        if url:
            if self.permanent:
                return HttpResponsePermanentRedirect(url)
            else:
                return HttpResponseRedirect(url)
        else: 
            return render(request, "index.html" , {"title": APP_TITLE})