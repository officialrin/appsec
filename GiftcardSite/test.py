from django.test import TestCase, Client
from django.urls import reverse
from LegacySite.models import *
from LegacySite.views import *
from django.http import HttpRequest
import io
import json


class XSSTest(TestCase):
    def setUp(self):
         self.client = Client()

    def XSSTest(self):
         product = Product.objects.create(product_name = 'test', product_image_path= 'test', recommended_price = 1, description = 'test')
          response = self.client.get('/gift', {'director' : '<script>alert("Message")</script>'})
          self.assertContains(
          	response, "&lt;script&gt;alert(&quot;Message!&quot;)&lt;/script&gt;")


class CSRFTest(TestCase):
     def setUp(self):
          self.client = Client()


     def CSRFTest(self):
    <form action="http://127.0.0.1:8000/gift.html" method="POST">
        <input type="hidden" name="username" id="username" value="attacker" />
        <input type="hidden" name="amount" id="amount" value="1000" />
    </form>
          product = Product.objects.create(product_name = 'test', product_image_path= 'test', recommended_price = 1, description = 'test')
          response = self.client.get('/buy' , {'director' : 'form action="http://127.0.0.1:8000/gift/0" method="POST"><input type="hidden" name="amount" value="2000"/><input type="hidden" name="username" value="test"/><input type="submit" value="test"/></form>'})
          self.assertContains(response, "form action=&quot;http://127.0.0.1:8000/gift/0&quot; method=&quot;POST&quot;&gt;&lt;input type=&quot;hidden&quot; name=&quot;amount&quot; value=&quot;2000&quot;/&gt;&lt;input type=&quot;hidden&quot; name=&quot;username&quot; value=&quot;hacker&quot;/&gt;&lt;input type=&quot;submit&quot; value=&quot;More Info&quot;/&gt;&lt;/form&gt;", status_code=200)
          
