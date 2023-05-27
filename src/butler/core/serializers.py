import uuid

from rest_framework import serializers

from . import models


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"


class ProtectedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProtectedFile
        fields = "__all__"

    def create(self, validated_data):
        filename = validated_data["file"].name
        new_filename = f"{uuid.uuid4().hex}-{filename}"
        validated_data["file"].name = new_filename
        return models.ProtectedFile.objects.create(**validated_data)
