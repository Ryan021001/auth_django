import json

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class QueryListRequest(serializers.Serializer):
    query = serializers.CharField(required=False, max_length=1000, allow_blank=True)
    filter = serializers.DictField(required=False, allow_empty=True)
    limit = serializers.IntegerField(min_value=1, max_value=1000, default=1)
    offset = serializers.IntegerField(min_value=1, max_value=10000, default=1)

    def to_internal_value(self, data):
        try:
            filter_param = data.get('filter')
            data['filter'] = json.loads(filter_param) if filter_param else None
        except Exception as err:
            error_message = {
                "filter": [
                    _("Must be a valid dictionary.")
                ]
            }
            raise serializers.ValidationError(detail=error_message) from err
        return super().to_internal_value(data)


class ErrorResponse(serializers.Serializer):
    error_code = serializers.IntegerField()
    error_message = serializers.CharField(default=None)
    error_detail = serializers.DictField(default={})
