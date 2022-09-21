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
      #   print(1)
      #   print(var.data)
        data = var.data["id"]
        data_delete = self.get_object(data)

        # data = FactoryName.objects.get(serializer.initial_data["id"])
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
      #   print(1)
        data_delete = self.get_object(int(pk))

        # data = FactoryName.objects.get(serializer.initial_data["id"])
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
      #   print(username)

        try:

            # serializers=ProductNameserializers(ProductName.objects.get(pk=pk))
            # print(serializers.data)
            a = []

            for keys in serializer.data:
                if keys["factoryName"] == int(pk):
                    a.append(keys)
            # print(a)

            return Response({'message': a})
        except:
            return Response({"message": "not found"})

    def post(self, request, pk):

        data = request.data
      #   data['image'].name = "nilesh.jpeg"
      #   print(data['image'].name)
      #   print(data,"post request data ****************************")
        serializer = ProductNameserializers(data=data)

        if serializer.is_valid():
            try:
                new_obj = FactoryName.objects.get(pk=pk)
            #     print(1)
            #     print(serializer.data)
                file = request.FILES['image']
                ext = Path(file.name).suffix
            #     print(data['id'])
            #     print()

                new_file = upload_file_to_blob(
                    file)
                data['image'].name = new_file

            #     print(request.data)
            #     print(file.name)

            #     new_file.file_name = file.name
            #     new_file.file_extention = ext
            #     new_file.save()

            #     new_obj_ag = FactoryName.objects.get(pk=FactoryNameserializers(
            #         serializer.validated_data["factoryName"]).data["id"])
                serialzernew = FactoryNameserializers(new_obj, many=False)
                # print(FactoryNameserializers(serializer.validated_data["factoryName"]).data["id"])
                keys = serialzernew.data
                if keys["id"] == int(pk):
                    serializer.save()
                    return Response({'message': 'succesful'})
            except:
                return Response({"message": "factory not present"})
            # return Response({"message":"factory not present first create an factory"})
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
            # print(keys["factoryName"],keys["id"])
            if keys["factoryName"] == int(pk) and keys["id"] == int(id):
                #     print(keys["factoryName"],keys["id"])
                a.append(keys)
        if a != []:
            return Response({'message': a})
        return Response({"message": "Product not found"})

    def put(self, request, pk, id):
        data = self.get_object(id)
        serializer = ProductNameserializers(data, data=request.data)
      #   print(serializer.is_valid(), serializer)
        print(data.image)

      #   print(serializer)
        if serializer.is_valid():
            print(serializer.is_valid())
            print("put request*******************")
            if request.data['image']:
                file = request.FILES['image']
            #     print(file)
                # print(type(file))
            #       ext = Path(file.name).suffix
            #       #     print(data['id'])
            #       #     print()

                new_file = upload_file_to_blob(file)
                print(new_file)
                # print(new_file)
                data.image.name = new_file
                request.data['image'].name = new_file
                print(request.data['image'], "request", data.image,
                      type(request.data['image']), type(data.image))

            # print(serializer.is_valid(), serializer, "serializer")

            # serializer = ProductNameserializers(data, data=request.data)
            reg = ProductName(id=id, productsName=request.data['productsName'], quantity=request.data['quantity'],
                              description=request.data['description'], image=request.data['image'], factoryName=FactoryName(
                                  pk))
            reg.save()

            # serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, id):
        try:
            new_obj = FactoryName.objects.get(pk=pk)
            serialzernew = FactoryNameserializers(new_obj, many=False)
            # # print(serialzernew.data["id"])

            data = self.get_object(id)
            productserializer = ProductNameserializers(data, many=False)
            # print(type(productserializer.data["factoryName"]),
            #       type(serialzernew.data["id"]))
            if serialzernew.data["id"] == productserializer.data["factoryName"]:
                #     print(data.image.name)
                check = delete_blob_client(str(data.image.name))
                data.delete()
                print(str(data.image.name))
                return Response({"message": "deleted"})
            return Response({"message": "id requested not in factory"})
        except:
            return Response({"message": "id requested not in factory12"})
