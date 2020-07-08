from django.db import models



class ProductCatalog(models.Model):
	def upload_dir(self,fileName):
		path = 'static/images/{}'.format(fileName)
		return path
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	product_type =  models.CharField(max_length=10)
	attribute = models.CharField(max_length=100)
	image =  models.ImageField(upload_to=upload_dir, null=True, blank=True)
	description = models.CharField(max_length=100, null=True)
	def __str__(self):
		return f"{self.product_type} - {self.name}"
