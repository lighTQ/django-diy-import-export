from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response

# Create your views here.

from rest_framework.viewsets import ModelViewSet
from api.serializer import PublishSerializer, BooksSerializer
from goods.models import Books


class BookView(ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer



