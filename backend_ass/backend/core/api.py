from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend.core.serializers import *
from rest_framework.authtoken.views import ObtainAuthToken  # <-- Here
from rest_framework.authtoken.models import Token  # <-- Here


class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class UserAuthentication(ObtainAuthToken):
	def post(self,request,*args,**kwargs):
		serializer = self.serializer_class(data=request.data,context={'request':request})
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		token, created = Token.objects.get_or_create(user = user)
		return Response(token.key)


class ProductList(APIView):
	def get(self, request,  format=None):
		model = ProductCatalog.objects.all()
		serializer = ProductCatalogSerializer(model, many=True)
		return Response(serializer.data) 


	def post(self, request):
		serializer = ProductCatalogSerializer(data=request.data)
		print(serializer)
		if serializer.is_valid(): 
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


class ProductDetails(APIView):
	def get_product(self,product_id):
		try:
			model = ProductCatalog.objects.get(id=product_id)
			return model
		except ProductCatalog.DoesNotExist:
			return 

	def get(self, request, id):
		if not self.get_product(id):
			return Response('Product Does Not Exist', status= status.HTTP_404_NOT_FOUND)
		serializer = ProductCatalogSerializer(self.get_product(id))
		return Response(serializer.data) 


	def put(self, request, id):
		if not self.get_product(id):
			return Response('Product Does Not Exist', status= status.HTTP_404_NOT_FOUND)
		serializer = ProductCatalogSerializer(self.get_product(id), request.data)
		if serializer.is_valid(): 
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


	def delete(self, request, id):
		if not self.get_product(id):
			return Response('Product Does Not Exist', status= status.HTTP_404_NOT_FOUND)
		model = self.get_product(id)
		model.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)