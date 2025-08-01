from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter
from .views import ContactViewSet, TaskViewSet
from .views import (
    TaskListView, TaskDetailView,
    TaskCreateView, TaskUpdateView, TaskDeleteView
)
router = DefaultRouter()
router.register(r'contact', ContactViewSet)
router.register(r'task', TaskViewSet)
 
urlpatterns = [

    path('api/', include(router.urls)),
    path('asd/', TaskListView.as_view(), name='task-list'),
    path('',views.home , name="home"),
    path('about/',views.about, name="about"),
    path('contact/',views.contact, name="contact"),
    path('register/',views.register, name="register"),
    path('login/',views.login, name="login"),
    path('logout/',views.logout, name="logout"),
    path('add_task/',views.add_task, name="add_task"),
    path('buy_now/',views.buy_now, name="buy_now"),

    path('delete_task/<int:task_id>/',views.delete_task, name="delete_task"),

    path('update_task/<int:task_id>/',views.update_task, name="update_task"),
    path('send_otp/',views.send_otp, name="send_otp"),
    path('course_form/',views.course_form, name="course_form"),
    path('course_list/',views.course_list, name="course_list"),

    path('blog/<slug:slug>/',views.blog_details, name="blog_details"),

    path('update_cart/<int:course_id>/', views.update_cart, name='update_cart'),

    path('add_to_cart/<int:course_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:course_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('create_checkout_session/<int:course_id>/',views.create_checkout_session,name='create_checkout_session'),
        path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('task/create/', TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
  path('auth/', include('social_django.urls', namespace='social')),
    path('google-login-success/', views.google_login_success, name='google_login_success'),
]

 