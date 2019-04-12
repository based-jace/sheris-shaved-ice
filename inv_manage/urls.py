"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from . import views

app_name = 'inv_manage'

urlpatterns = [
    path('orders/additem',views.add_item,name='additem'),
    path('orders/neworder/', views.neworder, name='neworder'),
    path('orders/', views.previous_orders, name='orders'),
    path('inventory/add/', views.add_item, name="add_item"),
    path('inventory/', views.inv_manage, name='inventory'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.home, name='home'),
]

from django.conf import settings
from django.conf.urls.static import static

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)