from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from .serializers import *
from .models import *
from rest_framework import status
from django.http import Http404


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
      #   print(data,"post request data ****************************")
        serializer = ProductNameserializers(data=data)

        if serializer.is_valid():
            try:
                new_obj = FactoryName.objects.get(pk=pk)
                new_obj_ag = FactoryName.objects.get(pk=FactoryNameserializers(
                    serializer.validated_data["factoryName"]).data["id"])
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
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, id):
        try:
            new_obj = FactoryName.objects.get(pk=pk)
            serialzernew = FactoryNameserializers(new_obj, many=False)
            # print(serialzernew.data["id"])

            data = self.get_object(id)
            productserializer = ProductNameserializers(data, many=False)
            # print(productserializer.data["factoryName"])
            if serialzernew.data["id"] == productserializer.data["factoryName"]:
                data.delete()
                return Response({"message": "deleted"})
            else:
                return Response({"message": "id requested not in factory"})
        except:
            return Response({"message": "something went wrongnn"})
