from django.contrib import admin
from .models import Movie,MovieComment,MovieCommentReport, MovieUpDown
# Register your models here.


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'rating')
    search_fields = ('title',)


class MovieCommentAdmin(admin.ModelAdmin):
    list_display = ('pk','title','content')
    search_fields = ('title',)


class MovieUpDownAdmin(admin.ModelAdmin):
    list_display=('user','moviecomment')

class MovieCommentReportAdmin(admin.ModelAdmin):
    list_display = ('reason', 'state')


admin.site.register(Movie,MovieAdmin)
admin.site.register(MovieComment, MovieCommentAdmin)
admin.site.register(MovieUpDown,MovieUpDownAdmin)
admin.site.register(MovieCommentReport,MovieCommentReportAdmin)
