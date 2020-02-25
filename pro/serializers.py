from rest_framework import serializers

from pro.models import Professional


class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = ['professional_id', 'full_name', 'email', 'phone', 'address', 'industry_expertise', 'about_me']
class CustomTokenSerializer(serializers.Serializer):
    token = serializers.CharField()