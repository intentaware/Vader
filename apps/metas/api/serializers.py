from rest_framework import serializers

from apps.metas.models import Circle, CampaignCircle, PublisherCircle


class CircleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circle
        exclude = ('added_on', 'updated_on')


class CampaignCircleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignCircle
        exclude = ('added_on', 'updated_on')


class PublisherCircleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublisherCircle
        exclude = ('added_on', 'updated_on')
