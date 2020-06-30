from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    alt = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    original_title = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=10)
    region = models.CharField(max_length=50, null=True, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    directors = models.CharField(max_length=100, null=True, blank=True)
    casts = models.CharField(max_length=100, null=True, blank=True)
    intro = models.TextField(null=True, blank=True)
    genres = models.CharField(max_length=255, null=True, blank=True)
    image = models.URLField(default='')

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'id': self.id})


class MovieComment(models.Model):
    title = models.CharField(verbose_name="评论标题",default='',max_length=32)
    content = models.TextField(verbose_name="评论详情", default='')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='电影')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'id': self.movie.id})


    class Meta:
        verbose_name = '用户评论'
        verbose_name_plural = verbose_name


class MovieUpDown(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    moviecomment = models.ForeignKey(MovieComment, null=True, on_delete=models.CASCADE)
    is_up = models.BooleanField(default=True)  # True:赞 False:灭


class MovieCommentReport(models.Model):
    reporter = models.ForeignKey(User,on_delete=models.CASCADE) # 举报者
    movieComment = models.ForeignKey(MovieComment,on_delete=models.CASCADE, related_name='reports')
    reason = models.TextField(max_length=256)

    state = models.IntegerField(default=0)  # 处理状态,0代表不处理,1代表处理举报
    reportTime = models.DateTimeField(auto_now_add=True) # 举报的时间



