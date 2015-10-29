from django.contrib import admin
from publications.models import Affiliation, Author, Paper, PaperType
# Register your models here.

admin.site.register(Affiliation)
admin.site.register(Author)
admin.site.register(Paper)
admin.site.register(PaperType)
