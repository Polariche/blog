from rest_framework import serializers
from komment.models import GithubCode, Comment

class GithubCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GithubCode
        fields = ('repo', 'branch', 'path')

class GithubCodeDetailedSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = GithubCode
        fields = ('repo', 'branch', 'path', 'content')

    def get_content(self, obj):
        return obj.get()

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('start', 'end', 'content')