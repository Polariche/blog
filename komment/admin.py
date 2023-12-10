from django.contrib import admin
import komment.models as models
import django.db.models

# Register your models here.

# for k,v in models.__dict__.items():
#     if type(v) == django.db.models.base.ModelBase:
#         if hasattr(v, 'Meta'):
#             if v.Meta.abstract:
#                 continue

#         admin.site.register(v)

admin.site.register(models.Code)
admin.site.register(models.GithubCode)
admin.site.register(models.Comment)