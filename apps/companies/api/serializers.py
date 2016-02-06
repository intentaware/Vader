from rest_framework import serializers

from apps.companies.models import *
from apps.metas.models import PublisherCircle

class BaseCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        exclude = ['users', 'circles']

class CompanySerializer(BaseCompanySerializer):
    circles = serializers.SerializerMethodField()

    def get_circles(self, obj):
        return list(
                obj.publishercircle_set.filter(
                    is_active=True
                ).values_list('circle_id', flat=True)
            )


class UpdateCompanySerializer(CompanySerializer):
    circles = serializers.ListField(child=serializers.IntegerField(), required=False)

    def update(self, instance, validated_data):
        data = validated_data
        circles = set(data.pop('circles', None))
        users = data.pop('users', None)

        # disabling
        PublisherCircle.objects.filter(publisher=instance) \
            .exclude(circle_id__in=circles).update(is_active=False)

        if len(circles):
            for c in circles:
                circle, created = PublisherCircle.objects.get_or_create(
                        publisher=instance,
                        circle_id=c
                    )
                if not circle.is_active:
                    circle.is_active = True
                    circle.save()

        for attr, value in data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
