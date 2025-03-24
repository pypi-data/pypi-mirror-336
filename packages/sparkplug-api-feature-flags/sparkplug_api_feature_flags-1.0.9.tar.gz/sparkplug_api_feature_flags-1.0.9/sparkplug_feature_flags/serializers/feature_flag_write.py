from rest_framework import serializers

from ..models import FeatureFlag


class FeatureFlagWrite(
    serializers.ModelSerializer["FeatureFlag"],
):
    class Meta:
        model = FeatureFlag

        fields = ("enabled",)
