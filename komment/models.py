from django.db import models
import requests as requests
import urllib.parse
from abc import *

# Create your models here.
class Code(models.Model):
    subclasses = []
    
    def __str__(self):
        for subclass in Code.subclasses:
            scls = getattr(self, subclass)
            if(scls):
                return scls.__str__()

    def url(self):
        for subclass in Code.subclasses:
            scls = getattr(self, subclass)
            if(scls):
                return scls.url()

    def get(self):
        url = str(self)
        response = requests.get(self.url())
        return response.text

class GithubCode(Code):
    Code.subclasses.append("githubcode")

    repo = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    path = models.CharField(max_length=100)

    class Meta:
        unique_together = ["repo", "branch", "path"]

    def url(self):
        return urllib.parse.urljoin("https://raw.githubusercontent.com", "/".join([self.repo, self.branch, self.path]))
    
    def __str__(self):
        return self.path.split("/")[-1]


class Comment(models.Model):
    code = models.ForeignKey(Code, on_delete=models.CASCADE)
    start = models.CharField(max_length=16)
    end = models.CharField(max_length=16, blank=True, null=True)
    content = models.CharField(max_length=1000)

    def __str__(self):
        if self.end:
            return f"{self.code}#{self.start}-{self.end}: {self.content}"
        else:
            return f"{self.code}#{self.start}: {self.content}"