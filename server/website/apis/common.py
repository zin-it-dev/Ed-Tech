from rest_framework import serializers

from .models import Tag


class TimeStampSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["date_created", "date_updated"]


class CommonSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["slug", "is_active"]
        extra_kwargs = {"slug": {"read_only": True}}


class TagSerializer(CommonSerializer):
    class Meta(CommonSerializer.Meta):
        model = Tag
        fields = CommonSerializer.Meta.fields + ["label"]


class TaggedObjectSerializer(CommonSerializer):
    tags = TagSerializer(many=True)

    class Meta(CommonSerializer.Meta):
        fields = CommonSerializer.Meta.fields + ["tags"]
