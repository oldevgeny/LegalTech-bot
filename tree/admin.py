from django.contrib import admin

from .models import *
from .forms import CommentForm


admin.site.register(Post)
admin.site.register(Comment)
