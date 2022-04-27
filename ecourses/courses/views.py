from typing import Union

from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.views import View
from .models import *
from django.http import Http404
from .serializers import *
from .paginator import BasePagination
from django.db.models import F


class CategoryViewSet(viewsets.ViewSet,
                      generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UserViewSet(viewsets.ViewSet,
                  generics.CreateAPIView,
                  generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'get_current_user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False, url_path='current-user')
    def get_current_user(self, request):
        return Response(self.serializer_class(request.user).data,
                        status=status.HTTP_200_OK)


class CourseViewSet(viewsets.ModelViewSet):
    # queryset = Course.objects.filter(active=True)
    serializer_class = CourseSerializer

    # parser_classes = BasePagination
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        courses = Course.objects.filter(active=True)
        q = self.request.query_params.get('q')
        if q is not None:
            courses = courses.filter(subject__icontains=q)

        cate_id = self.request.query_params.get('category_id')

        if cate_id is not None:
            courses = courses.filter(category_id=cate_id)

        return courses

    @action(detail=True, methods=['get'], url_path='lessons')
    def get_lessons(self, request, pk):
        lessons = Course.objects.get(pk=pk).lessons.filter(active=True)
        # lessons = self.get_object().lessons.filter(active=True)

        q = request.query_params.get('q')
        if q is not None:
            lessons = lessons.filter(subject__icontains=q)

        return Response(LessonSerializer(lessons, many=True).data,
                        status=status.HTTP_200_OK)
    # def get_permissions(self):
    #     if self.action == 'list':
    #         return [permissions.AllowAny()]
    #     else:
    #         return [permissions.IsAuthenticated()]
    #


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.filter(active=True)
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action in ['add_comment', 'take_aciton', 'rate']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['post'], detail=True, url_path='hide-lesson', url_name='hide-lesson')
    # /lessons/{pk}/hide-lesson
    def hide_lesson(self, request, pk):
        try:
            l = Lesson.objects.get(pk=pk)
            l.active = False
            l.save()
        except Lesson.DoseNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=LessonSerializer(l, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='tags')
    def add_tag(self, request, pk):
        try:
            lesson = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            tags = request.data.get('tags')
            if tags is not None:
                for tag in tags:
                    t, _ = Tag.objects.get_or_create(name=tag)
                    lesson.tags.add(t)

                lesson.save()
                return Response(self.serializer_class(lesson).data,
                                status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True, url_path='add-comment')
    def add_comment(self, request, pk):
        content = request.data.get('content')
        if content is not None:
            c = Comment.objects.create(content=content,
                                       lesson=self.get_object(),
                                       creator=request.user)
            return Response(CommentSerializer(c).data,
                            status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True, url_path='like')
    def take_aciton(self, request, pk):
        try:
            action_type = int(request.data['type'])
        except Union[IndexError, ValueError]:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            action = Action.objects.create(type=action_type,
                                           lesson=self.get_object(),
                                           creator=request.user)

            return Response(AcitonSerializer(action).data,
                            status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='rating')
    def rate(self, request, pk):
        try:
            rating = int(request.data['rating'])
        except Union[IndexError, ValueError]:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            r = Rating.objects.create(rate=rating,
                                      lesson=self.get_object(),
                                      creator=request.user)

            return Response(AcitonSerializer(r).data,
                            status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='views')
    def inc_view(self, request, pk):
        v, created = LessonView.objects.get_or_create(lesson=self.get_object())
        v.views = F('views') + 1
        v.save()

        v.refresh_from_db()
        return Response(LessonViewSerializer(v).data,
                        status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ViewSet,
                     generics.DestroyAPIView,
                     generics.UpdateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer

    def delete(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            return super().partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)


def index(request):
    return render(request, template_name='index.html', context={
        "name": "LongHD"
    })


def welcome(request, year):
    return HttpResponse('Hello ' + str(year))


def welcome2(request, year):
    return HttpResponse('Hello ' + str(year))


class TestView(View):
    def get(self, request):
        return HttpResponse("test get method")

    def post(self, request):
        pass
