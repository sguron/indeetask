from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CategorySerializer, TaskSerializer


class CategoryViewSet(ModelViewSet):
    # Handle authentication
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, )

    serializer_class = CategorySerializer

    def get_queryset(self):
        """
        returns a queryset for model that is locked to the loggedin user
        :return: queryset
        """
        user = self.request.user
        model = self.serializer_class.Meta.model # This is Categories model
        queryset = model.objects.filter(owner=user)
        #queryset = model.objects.all()
        return queryset


class TasksViewSet(ModelViewSet):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    serializer_class = TaskSerializer

    def get_queryset(self):
        """
        returns a queryset for model that is locked to the loggedin user
        :return: queryset
        """
        user = self.request.user
        model = self.serializer_class.Meta.model # This is Task model
        queryset = model.objects.filter(category__owner=user)
        #queryset = model.objects.all()
        return queryset

    def filter_queryset(self, queryset):
        """
        Incase one wants to filter results by category

        :param queryset:
        :return: queryset
        """
        category_id = self.request.query_params.get('category', None)

        queryset = queryset.order_by("sort_weight") # for good measure

        if category_id:
            queryset = queryset.filter(category__id=category_id)

        return queryset


class TasksAppView(LoginRequiredMixin, TemplateView):
    login_url = "account/login/"
    template_name = "tasktracker/dashboard.html"
