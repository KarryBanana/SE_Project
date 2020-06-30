from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import timezone,datetime
# Create your models here.


class Tags(models.Model):
    name = models.CharField(max_length=32, verbose_name="标签")

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"

    def __str__(self):
        return self.name


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    tags = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
        verbose_name="标签",
        related_name="tags",
        blank=True,
        null=True,
    )
    title = models.CharField(verbose_name="书名", max_length=32)
    author = models.CharField(verbose_name="作者", max_length=32)
    intro = models.TextField(verbose_name="描述")
    pic = models.URLField(default='')  # 封面图片
    rate = models.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        verbose_name = "图书"
        verbose_name_plural = "图书"

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'id': self.id})

    def __str__(self):
        return self.title


class BookComment(models.Model):
    title = models.CharField(verbose_name="评论标题",default='',max_length=32)
    content = models.TextField(verbose_name="评论详情", default='')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='书籍')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'id': self.book.id})


    class Meta:
        verbose_name = '用户评论'
        verbose_name_plural = verbose_name


class BookUpDown(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    bookcomment = models.ForeignKey(BookComment, null=True, on_delete=models.CASCADE)
    is_up = models.BooleanField(default=True)  # True:赞 False:灭


class BookCommentReport(models.Model):
    reporter = models.ForeignKey(User,on_delete=models.CASCADE) # 举报者
    bookComment = models.ForeignKey(BookComment,on_delete=models.CASCADE,related_name='reports')
    reason = models.TextField(max_length=256)

    state = models.IntegerField(default=0)  # 处理状态
    reportTime = models.DateTimeField(auto_now_add=True) # 举报的时间
