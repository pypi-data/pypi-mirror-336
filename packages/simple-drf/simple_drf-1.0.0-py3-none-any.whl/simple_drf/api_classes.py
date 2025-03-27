from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class ListAPIView(APIView):
    model = None
    model_serializer = None

    def get(self, request):
        objs = self.model.objects.all()
        serializer = self.model_serializer(objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.model_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailAPIView(APIView):
    model = None
    model_serializer = None

    def get(self, request, pk):
        try:
            obj = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response({'error': 'Object not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.model_serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            obj = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response({'error': 'Object not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.model_serializer(obj, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            obj = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response({'error': 'Object not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        obj.delete()

        return Response(status=status.HTTP_200_OK)
    

class FullAPIView(APIView):
    model = None
    model_serializer = None

    def get(self, request, pk=None):
        if pk is not None:
            obj = get_object_or_404(self.model, pk=pk)
            serializer = self.model_serializer(obj)
        else:
            objs = self.model.objects.all()
            serializer = self.model_serializer(objs, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.model_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            obj = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response({'error': 'Object not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.model_serializer(obj, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            obj = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return Response({'error': 'Object not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        obj.delete()

        return Response(status=status.HTTP_200_OK)
