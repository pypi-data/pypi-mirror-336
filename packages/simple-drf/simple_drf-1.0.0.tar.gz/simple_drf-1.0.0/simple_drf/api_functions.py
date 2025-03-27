from rest_framework.response import Response
from rest_framework import status


def get_all(Model, ModelSerializer):
    objs = Model.objects.all()
    serializer = ModelSerializer(objs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def post(ModelSerializer, request):
    serializer = ModelSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_one(Model, ModelSerializer, pk):
    try:
        obj = Model.objects.get(pk=pk)
    except Model.DoesNotExist:
        return Response({'error': 'Object not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ModelSerializer(obj)
    return Response(serializer.data, status=status.HTTP_200_OK)


def put(Model, ModelSerializer, request, pk):
    try:
        obj = Model.objects.get(pk=pk)
    except Model.DoesNotExist:
        return Response({'error': 'Object not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ModelSerializer(obj, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete(Model, pk):
    try:
        obj = Model.objects.get(pk=pk)
    except Model.DoesNotExist:
        return Response({'error': 'Object not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    obj.delete()

    return Response(status=status.HTTP_200_OK)
