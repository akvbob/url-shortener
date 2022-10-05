from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from .models import ShortLink
from .utils import Base62Conversion


def create_short_url():
    long_url = "https://www.google.com/"
    algorithm = Base62Conversion()
    short_url = algorithm.get_short_url(long_url)
    return ShortLink.objects.create(original_url=long_url, short_url=short_url)

def get_path(obj):
    return "/redirect/{}".format(obj.short_url)

def assert_error_message(self, response, message):
    messages = list(response.context['messages'])
    self.assertEqual(len(messages), 1)
    self.assertEqual(str(messages[0]), message)



class ShortURLViewTest(TestCase):

    def setUp(self):
        self.long_url_exists = {"url": "https://www.google.com/"}
        self.long_url_not_exists = {"url": "abcd"}
        self.long_url_not_entered = {"url": ""}
        

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('shortener:index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('shortener:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_long_url_is_none(self):
        response = self.client.post(path=reverse('shortener:index'), data=self.long_url_not_entered)
        assert_error_message(self, response, _('Long URL is required!'))

    def test_long_url_not_exist(self):
        response = self.client.post(path=reverse('shortener:index'), data= self.long_url_not_exists)
        assert_error_message(self, response, _('Website does not exist!'))
    
    def test_shorten_url_success(self):
        response = self.client.post(path=reverse('shortener:index'), data= self.long_url_exists)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 0)
        self.assertIsNotNone(response.context["short_url"])

    def test_same_long_url_different_short_url_random(self):
        response1 = self.client.post(path=reverse('shortener:index'), data=self.long_url_exists)
        response2 = self.client.post(path=reverse('shortener:index'), data=self.long_url_exists)
        
        self.assertNotEqual(response1.context["short_url"], response2.context["short_url"])



class RedirectToLongURLViewTest(TestCase):

    def tearDown(self):
        ShortLink.objects.all().delete()

    def test_redirect_success(self):
        obj = create_short_url()
        path = get_path(obj)
        response = self.client.get(path=path)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, obj.original_url)

    def test_redirect_not_active_url(self):
        obj = create_short_url()
        obj.is_active = False
        obj.save()
        path = get_path(obj)
        response = self.client.get(path=path)
        self.assertEqual(response.status_code, 200)
        assert_error_message(self, response,  _('URL is not active at the moment!'))