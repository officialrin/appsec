from django.test import TestCase, Client
from django.urls import reverse
from LegacySite.models import *
from LegacySite.views import *
from django.http import HttpRequest
import io
import json


class SaltTest(TestCase):
	def test_salt(self):
		self.client.post(reverse('Register'), {
		                 'uname': 'user', 'pword': 'password1', 'pword2': 'password1'})
		self.client.post(reverse('Register'), {
		                 'uname': 'admin', 'pword': 'password1', 'pword2': 'password1'})
		data = io.StringIO(
			'{"merchant_id": "Gift Card", "customer_id": "test", "total_value": "1000", "records": [{"record_type": "amount_change", "amount_added": 2000, "signature": " \' union SELECT password from LegacySite_user where username = \'user"}]}')
		filename = "salt.gftcrd"
		response = self.client.post(reverse('Input'), {
		                            'card_data': data, 'filename': filename, 'card_supplied': True, 'card_fname': 'test'},)
		pw1 = response.context.get('card_found', None)
		print(pw1)
		self.client.post(reverse('Register'), {'uname': 'admin', 'pword': 'password1'})
		data = io.StringIO(
			'{"merchant_id": "Gift Card", "customer_id": "test", "total_value": "1000", "records": [{"record_type": "amount_change", "amount_added": 2000, "signature": " \' union SELECT password from LegacySite_user where username = \'admin"}]}')
		filename = "salt.gftcrd"
		response = self.client.post(reverse('Input'), {
		                            'card_data': data, 'filename': filename, 'card_supplied': True, 'card_fname': 'test'},)
		pw2 = response.context.get('card_found', None)
		assert (pw1 != pw2)


class XSSTest(TestCase):
    def setUp(self):
         self.client = Client()

    def Test(self):
         product = Product.objects.create(product_name = 'test', product_image_path= 'test', recommended_price = 1, description = 'test')
          response = self.client.get('/gift', {'director' : '<script>alert("Message")</script>'})
          self.assertContains(
          	response, "&lt;script&gt;alert(&quot;Message!&quot;)&lt;/script&gt;")


class CSRFTest(TestCase):
     def setUp(self):
          self.client = Client()


     def csrf_attack(self):
    <form action="http://127.0.0.1:8000/gift.html" method="POST">
        <input type="hidden" name="username" id="username" value="attacker" />
        <input type="hidden" name="amount" id="amount" value="1000" />
    </form>
          product = Product.objects.create(product_name = 'test', product_image_path= 'test', recommended_price = 1, description = 'test')
          response = self.client.get('/buy' , {'director' : 'form action="http://127.0.0.1:8000/gift/0" method="POST"><input type="hidden" name="amount" value="2000"/><input type="hidden" name="username" value="test"/><input type="submit" value="test"/></form>'})
          self.assertContains(response, "form action=&quot;http://127.0.0.1:8000/gift/0&quot; method=&quot;POST&quot;&gt;&lt;input type=&quot;hidden&quot; name=&quot;amount&quot; value=&quot;2000&quot;/&gt;&lt;input type=&quot;hidden&quot; name=&quot;username&quot; value=&quot;hacker&quot;/&gt;&lt;input type=&quot;submit&quot; value=&quot;More Info&quot;/&gt;&lt;/form&gt;", status_code=200)
          
