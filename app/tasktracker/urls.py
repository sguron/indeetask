from django.conf.urls import url, include
from rest_framework import routers

from .views import CategoryViewSet, TasksViewSet

router = routers.SimpleRouter()
router.register(r'categories', CategoryViewSet, base_name="category")
router.register(r'tasks', TasksViewSet, base_name="task")

urlpatterns = [
    url(r'^', include(router.urls)),
]
