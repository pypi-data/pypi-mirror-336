from rest_framework.serializers import (
    ModelSerializer,
)

from ..models import FeatureFlag


class FeatureFlagTeaser(
    ModelSerializer["FeatureFlag"],
):
    class Meta:
        model = FeatureFlag

        fields = (
            "uuid",
            "created",
            "title",
            "description",
            "enabled",
        )

        read_only_fields = ("__all__",)
