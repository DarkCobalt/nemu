from django.contrib import admin
from models import *


class ChapterAdmin(admin.ModelAdmin):
    list_display = ['project', 'number', 'display_status']
    search_fields = ['project']
    save_on_top = True



admin.site.register(Chapter, ChapterAdmin)
admin.site.register(MangaStatus)
admin.site.register(ChapterStatus)
admin.site.register(Project)