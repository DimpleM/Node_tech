from django.urls import path
from backend.core import views
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here
from rest_framework.authtoken.models import Token  # <-- Here
from backend.core.api import ProductList, ProductDetails, UserAuthentication,Logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url


urlpatterns = [
    path('api/product_list/', ProductList.as_view(), name='product_list'),
    path('api/product_list/<int:id>/', ProductDetails.as_view(), name='product_detail'),
    path('admin/', admin.site.urls),
    path('api/auth/', UserAuthentication.as_view(), name='UserAuthenticationAPI'),
    path('api/logout/', Logout.as_view()),
]




urlpatterns += staticfiles_urlpatterns()