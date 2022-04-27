from django.contrib import admin
from django.urls import path, re_path, include
from . import views
# from .admin import admin_site
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('courses', views.CourseViewSet, 'course')
router.register('lessons', views.LessonViewSet)
router.register('users', views.UserViewSet)
router.register('categories', views.CategoryViewSet, 'category')
router.register('comments', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls), name="index"),
    path('welcome/<int:year>/', views.welcome, name='welcome'),
    path('test/', views.TestView.as_view()),
    re_path(r'^welcome2/(?P<year>[0-9]{1,2})/$', views.welcome2, name='welcome2'),
    # path('admin/', admin_site.urls)
]

