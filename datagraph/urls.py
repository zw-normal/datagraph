"""datagraph URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView
from datagraph.schema import schema

from viewer import urls as viewer_url
from viewer.forms import DataGraphAuthenticationForm
from engine import urls as engine_url


urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(
        authentication_form=DataGraphAuthenticationForm), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin', admin.site.urls),
    path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    path('engine/', include(engine_url)),
    path('', include(viewer_url)),
]
