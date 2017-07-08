from django.db.models import Max
from django.db.models import F
from rest_framework import serializers
from .models import Category, Task

__author__ = 'TheArchitect'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'owner', 'name', 'date_created', 'date_updated')
        read_only_fields = ('id', 'owner', 'date_created', 'date_updated')
        depth = 0

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user
        instance = self.Meta.model.objects.create(**validated_data)
        return instance


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'category', 'description', 'sort_weight', 'completed', 'date_created', 'date_updated',)
        read_only_fields = ('id', 'date_created', 'date_updated')


    def validate_category(self, category):
        # Just check if category assigned is also owned by the loggedin user
        user = self.context['request'].user
        if category.owner != user:
            raise serializers.ValidationError("You dont own this category")

        return category

    def create(self, validated_data):
        # Get the last sorted item in this category and then add this task after it
        model = self.Meta.model

        bottom_task = model.objects.filter(category=validated_data['category']).aggregate(max= Max('sort_weight'))
        bottom_weight = bottom_task['max']

        # if bottom weight is None then this is the first task in this category
        if bottom_weight is None:
            bottom_weight = 0

        # Add one to bottom task weight for this new task
        new_task_sort_weight = bottom_weight + 1

        validated_data['sort_weight'] = new_task_sort_weight
        instance = model.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        """


         Check if the category or sort weight has changed
         If category is not changed then just resort records in db


        :param instance: Task instance
        :param validated_data: dict of validated data
        :return:
        """
        model = self.Meta.model

        sort_weight = validated_data['sort_weight']
        if 'category' in validated_data:
            category = validated_data['category']
        else:
            category = instance.category


        if instance.sort_weight != sort_weight or instance.category != category:
            # create space for this task
            # just move all higher weight tasks down by 1 in the correct category
            # by incrementing their weight by 1
            # kind of like adding a new row in excel

            model.objects.filter(sort_weight__gte=sort_weight, category=category).update(
                sort_weight=F('sort_weight') + 1
            )

            # now move the instance into this new row
            instance.category = category

            if sort_weight == 0:
                sort_weight = 1
            instance.sort_weight = sort_weight


        instance.save()

        return instance


