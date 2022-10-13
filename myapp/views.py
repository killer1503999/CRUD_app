from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from .serializers import *
from .models import *
from rest_framework import status
from django.http import Http404

from hashlib import new
from pathlib import Path
import mimetypes


from django.contrib import messages


from .azure_file_controller import ALLOWED_EXTENTIONS, download_blob, upload_file_to_blob, delete_blob_client

from . import models


class factoryList(APIView):
    def get(self, request):

        new_obj = FactoryName.objects.all()
        serialzer = FactoryNameserializers(new_obj, many=True)
        return Response(serialzer.data)

    def get_object(self, pk):
        try:
            return FactoryName.objects.get(pk=pk)
        except FactoryName.DoesNotExist:
            raise Http404

    def delete(self, var):

        data = var.data["id"]
        data_delete = self.get_object(data)

        try:
            data_delete.delete()
            return Response({"message": "deleted"})
        except:
            return Response({"message": "no"})

    def post(self, request):

        data = request.data
        serializer = FactoryNameserializers(data=data)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response({'message': 'succesful'})
            except:
                return Response({"message": "factory not present"})

        return Response(serializer._errors)


class factoryDelete(APIView):

    def get_object(self, pk):
        try:
            return FactoryName.objects.get(pk=pk)
        except FactoryName.DoesNotExist:
            raise Http404

    def delete(self, request, pk):

        data_delete = self.get_object(int(pk))

        try:
            data_delete.delete()
            return Response({"message": "deleted"})
        except:
            return Response({"message": "no"})


class productList(APIView):
    def get(self, request, pk):
        new_obj = ProductName.objects.all()
        serializer = ProductNameserializers(new_obj, many=True)

        username = self.request.query_params.get('factoryName')

        try:
            a = []
            for keys in serializer.data:
                if keys["factoryName"] == int(pk):
                    a.append(keys)
            return Response({'message': a})
        except:
            return Response({"message": "not found"})

    def post(self, request, pk):

        data = request.data
        serializer = ProductNameserializers(data=data)

        if serializer.is_valid():
            try:
                new_obj = FactoryName.objects.get(pk=pk)

                file = request.FILES['image']
                ext = Path(file.name).suffix
                new_file = upload_file_to_blob(
                    file)
                data['image'].name = new_file
                serialzernew = FactoryNameserializers(new_obj, many=False)
                keys = serialzernew.data
                if keys["id"] == int(pk):
                    serializer.save()
                    return Response({'message': 'succesful'})
            except:
                return Response({"message": "factory not present"})

        return Response(serializer._errors)


class productDetails(APIView):
    def get_object(self, pk):
        try:
            return ProductName.objects.get(pk=pk)
        except ProductName.DoesNotExist:
            raise Http404

    def get(self, request, pk, id):
        new_obj = ProductName.objects.all()
        serializer = ProductNameserializers(new_obj, many=True)

        a = []
        for keys in serializer.data:
            if keys["factoryName"] == int(pk) and keys["id"] == int(id):
                a.append(keys)
        if a != []:
            return Response({'message': a})
        return Response({"message": "Product not found"})

    def put(self, request, pk, id):

        data = self.get_object(id)
        serializer = ProductNameserializers(data, data=request.data)

        if serializer.is_valid():

            if request.data['image']:
                file = request.FILES['image']

                new_file = upload_file_to_blob(file)

                data.image.name = new_file
                request.data['image'].name = new_file
            reg = ProductName(id=id, productsName=request.data['productsName'], quantity=request.data['quantity'],
                              description=request.data['description'], image=request.data['image'], factoryName=FactoryName(
                                  pk))
            reg.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, id):
        try:
            new_obj = FactoryName.objects.get(pk=pk)
            serialzernew = FactoryNameserializers(new_obj, many=False)

            data = self.get_object(id)
            productserializer = ProductNameserializers(data, many=False)

            if serialzernew.data["id"] == productserializer.data["factoryName"]:

                data.delete()
                check = delete_blob_client(str(data.image.name))
                return Response({"message": "deleted"})
            return Response({"message": "id requested not in factory"})
        except:
            return Response({"message": "id requested not in factory12"})
