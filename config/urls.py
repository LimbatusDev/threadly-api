"""Threadly URL Configuration
"""
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import path, include

from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=settings.DEBUG))),
]
