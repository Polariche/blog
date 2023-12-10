from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from rest_framework import generics, mixins
from rest_framework.views import APIView
from komment.models import GithubCode, Comment
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from komment.serializers import *

import json
# Create your views here.

def get_repo_path(ch, prog):
    repo = "polariche/algorithms"
    path = f"USACO/USACO_Training/{ch}/{prog}.cpp"

    return repo, path

class UsacoGithubCodeView(APIView):
    serializer = GithubCodeDetailedSerializer

    def post(self, request, ch, prog):
        branch = request.POST.get('branch', None)
        repo, path = get_repo_path(ch, prog)

        if branch is None:
            code = GithubCode.objects.create(repo=repo, path=path)
        else:
            code = GithubCode.objects.create(repo=repo, branch=branch, path=path)
        
        code = GithubCode.objects.get(repo=repo, path=path)
        return JsonResponse(self.serializer(code).data, safe=False)

    def get(self, request, ch, prog):
        repo, path = get_repo_path(ch, prog)
        code = GithubCode.objects.get(repo=repo, path=path)
        
        return JsonResponse(self.serializer(code).data, safe=False)

    def delete(self, request, ch, prog):
        # DELETE
        branch = request.DELETE.get('branch', None)

        if branch is None:
            GithubCode.objects.get(repo=repo, path=path).delete()
        else:
            GithubCode.objects.get(repo=repo, branch=branch, path=path).delete()
        return HttpResponse()


class UsacoCommentView(APIView):
    serializer = CommentSerializer

    def post(self, request, ch, prog):
        branch = request.POST.get('branch', 'main')
        start = request.POST.get('start')
        end = request.POST.get('end')
        content = request.POST.get('content')

        repo, path = get_repo_path(ch, prog)

        code = GithubCode.objects.get(repo=repo, branch=branch, path=path)

        Comment.objects.create(code=code, start=start, end=end, content=content)
        comments = Comment.objects.get(code=code)

        return JsonResponse(self.serializer(comments).data, safe=False)

    def get(self, request, ch, prog):
        # GET
        branch = request.GET.get('branch', 'main')
        repo, path = get_repo_path(ch, prog)

        code = GithubCode.objects.get(repo=repo, branch=branch, path=path)
        comments = Comment.objects.get(code=code)

        return JsonResponse(self.serializer(comments).data, safe=False)

    def delete(self, request, ch, prog):
        # DELETE
        branch = request.DELETE.get('branch', None)
        repo, path = get_repo_path(ch, prog)

        code = None
        if branch is None:
            code = GithubCode.objects.get(repo=repo, path=path)
        else:
            code = GithubCode.objects.get(repo=repo, branch=branch, path=path)

        Comment.objects.filter(code=code).delete()
        
        return HttpResponse()
        

    
    