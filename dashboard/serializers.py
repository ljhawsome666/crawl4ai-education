from rest_framework import serializers
from .models import CrawlTask

class CrawlTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlTask
        fields = '__all__'
