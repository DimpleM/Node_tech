
import os
import io
from PIL import Image

import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from backend.core.models import ProductCatalog
from backend.core.serializers import ProductCatalogSerializer
from django.core.files.uploadedfile import SimpleUploadedFile


class ProductListAPIViewTestCase(APITestCase):
	url = reverse("product_list")

	def setUp(self):
		self.username = "dimple"
		self.password = "you_know_nothing"
		self.email = "dimpledimple41@gmail.com"
		self.user = User.objects.create_user(self.username, self.password)
		self.token = Token.objects.create(user=self.user)
		self.api_authentication()

	def api_authentication(self):
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

	def generate_photo_file(self):
		file = io.BytesIO()
		image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
		image.save(file, 'png')
		file.name = 'test.png'
		file.seek(0)
		return file

	def test_create_product(self):
		self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
		photo_file = self.generate_photo_file()

		data =  {
	        "name": "a",
	        "product_type": "laptop",
	        "attribute": "{\"ram\":\"a\",\"processor\":\"a\",\"capacity\":\"a\"}",
	        "image": photo_file,
	        "description": "a"
    	}
		response = self.client.post(self.url, data,format='multipart')
		self.assertEqual(201, response.status_code)


	def test_user_product(self):
		response = self.client.get(self.url)
		self.assertEqual(200, response.status_code)

class ProductDetailAPIViewTestCase(APITestCase):

    def setUp(self):
        self.username = "john"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.product = ProductCatalog.objects.create(name="Call Mom!")
        self.url = reverse("product_detail", kwargs={"id": self.product.id})
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_product_object_bundle(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        product_serializer_data = ProductCatalogSerializer(instance=self.product).data
        response_data = json.loads(response.content)
        self.assertEqual(product_serializer_data, response_data)

    def generate_photo_file(self):
    	file = io.BytesIO()
    	image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    	image.save(file, 'png')
    	file.name = 'test.png'
    	file.seek(0)
    	return file

    def test_product_object_update_authorization(self):
        new_user = User.objects.create_user("newuser", "new@user.com", "newpass")
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        photo_file = self.generate_photo_file()
        data =  {
	        "name": "a",
	        "product_type": "mobile",
	        "attribute": "{\"ram\":\"a\",\"processor\":\"a\",\"capacity\":\"a\"}",
	        "image": photo_file,
	        "description": "a"
    	}
    	
        response = self.client.put(self.url, data)
        self.assertEqual(201, response.status_code)
   

    def test_product_object_update(self):
    	photo_file = self.generate_photo_file()
    	data =  {
	        "name": "a",
	        "product_type": "mobile",
	        "attribute": "{\"ram\":\"a\",\"processor\":\"a\",\"capacity\":\"a\"}",
	        "image": photo_file,
	        "description": "a"
    	}

    	response = self.client.put(self.url, data)
    	response_data = json.loads(response.content)
    	print(response_data)
    	product = ProductCatalog.objects.get(id=self.product.id)
    	self.assertEqual(response_data.get("name"), product.name)
    def test_product_object_update(self):
    	photo_file = self.generate_photo_file()
    	data =  {
	        "name": "a",
	        "product_type": "mobile",
	        "attribute": "{\"ram\":\"a\",\"processor\":\"a\",\"capacity\":\"a\"}",
	        "image": photo_file,
	        "description": "a"
    	}

    	response = self.client.put(self.url, data)
    	response_data = json.loads(response.content)
    	print(response_data)
    	product = ProductCatalog.objects.get(id=self.product.id)
    	self.assertEqual(response_data.get("name"), product.name)


    def test_product_object_delete_authorization(self):
        new_user = User.objects.create_user("newuser", "new@user.com", "newpass")
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)