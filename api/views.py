# views.py

from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from api.models import ToDo
from api.serializers import ToDoSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response


class TodoList(APIView):

    def get(self, request):  # 모든 데이터 얻기
        todo = ToDo.objects.all()
        serializer = ToDoSerializer(todo, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)

    def post(self, request):  # 새로운 데이터 등록
        data = JSONParser().parse(request)
        serializer = ToDoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class TodoDetail(APIView):

    def get_object(self, id):
        todo = get_object_or_404(ToDo, id=id)
        return todo

    def get(self, request, id):  # 특정 데이터 얻기
        todo = self.get_object(id)
        serializer = ToDoSerializer(todo)
        return JsonResponse(serializer.data, status=200, safe=False)

    def delete(self, request, id):  # 특정 데이터 삭제
        todo = self.get_object(id)
        todo.delete()
        return Response(status=204)

    def patch(self, request, id):  # 특정 데이터 업데이트
        todo = self.get_object(id)
        data = JSONParser().parse(request)
        serializer = ToDoSerializer(todo, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
