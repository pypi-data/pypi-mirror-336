from rest_framework.serializers import ModelSerializer
from sparkplug_core.fields import UserUuidField

from ..fields import FeatureFlagUuidField
from ..models import FlagAccess
from .feature_flag_teaser import FeatureFlagTeaser


class FlagAccessRead(
    ModelSerializer["FlagAccess"],
):
    feature_flag_uuid = FeatureFlagUuidField()

    feature_flag = FeatureFlagTeaser(read_only=True)

    user_uuid = UserUuidField()

    class Meta:
        model = FlagAccess

        fields = (
            "uuid",
            "feature_flag_uuid",
            "feature_flag",
            "user_uuid",
        )

        read_only_fields = ("__all__",)
