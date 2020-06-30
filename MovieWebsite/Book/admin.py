from django.contrib import admin
from .models import BookCommentReport,Book,BookComment,BookUpDown
# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'rate')
    search_fields = ('title',)


class BookCommentAdmin(admin.ModelAdmin):
    list_display = ('title','content')
    search_fields = ('title',)


class BookCommentReportAdmin(admin.ModelAdmin):
    list_display = ('reason', 'state')


class BookUpDownAdmin(admin.ModelAdmin):
    list_display=('user','bookcomment')


admin.site.register(Book, BookAdmin)
admin.site.register(BookComment, BookCommentAdmin)
admin.site.register(BookCommentReport, BookCommentReportAdmin)
admin.site.register(BookUpDown, BookUpDownAdmin)

