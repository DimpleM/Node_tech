from rest_framework import serializers
from backend.core.models import ProductCatalog


class ProductCatalogSerializer(serializers.ModelSerializer):


	class Meta:
		model = ProductCatalog
		# fields = ('name','product_type')
		fields = '__all__'
		print(fields)
