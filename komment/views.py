from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from komment.models import GithubCode, Comment

import json
# Create your views here.

def usaco_code_raw(request, ch, prog):
    repo = "polariche/algorithms"
    path = f"USACO/USACO_Training/{ch}/{prog}.cpp"

    if request.method == 'POST':
        # POST
        branch = request.POST.get('branch', 'main')

        code = GithubCode.objects.create(repo=repo, branch=branch, path=path)

        # TODO integrity check (500 response)

        return HttpResponse()

    if request.method == 'GET':
        # GET
        branch = request.GET.get('branch', 'main')
        
        code = GithubCode.objects.get(repo=repo, branch=branch, path=path)
        # if code doesn't exist, return 404

        return HttpResponse(code.get(), content_type="text/plain")


    if request.method == 'DELETE':
        # DELETE
        branch = request.DELETE.get('branch', None)

        if branch is None:
            GithubCode.objects.get(repo=repo, path=path).delete()
            # if code doesn't exist, return 404
        else:
            GithubCode.objects.get(repo=repo, branch=branch, path=path).delete()
            # if code doesn't exist, return 404
        return HttpResponse()

    
def usaco_comments(request, ch, prog):
    repo = "polariche/algorithms"
    path = f"USACO/USACO_Training/{ch}/{prog}.cpp"

    if request.method == 'POST':
        # POST
        # TODO : replace main branch with actual commit name
        branch = request.POST.get('branch', 'main')
        start = request.POST.get('start')
        end = request.POST.get('end')
        content = request.POST.get('content')

        print(branch, start, end, content)

        code = GithubCode.objects.get(repo=repo, branch=branch, path=path)
        # if code doesn't exist, return 404

        Comment.objects.create(code=code, start=start, end=end, content=content)

        return HttpResponse()

    if request.method == 'GET':
        # GET
        branch = request.GET.get('branch', 'main')

        code = GithubCode.objects.get(repo=repo, branch=branch, path=path)
        comments = Comment.objects.filter(code=code)
        comments_json = json.loads(serializers.serialize('json', comments, fields=("start", "end", "content")))
        
        return JsonResponse(comments_json, safe=False)


    if request.method == 'DELETE':
        # DELETE
        branch = request.DELETE.get('branch', None)

        code = None
        if branch is None:
            code = GithubCode.objects.get(repo=repo, path=path)
        else:
            code = GithubCode.objects.get(repo=repo, branch=branch, path=path)

        Comment.objects.filter(code=code).delete()
        
        return HttpResponse()

    
    