from django.shortcuts import render

# Create your views here.
import re
import markdown
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.generic import ListView, DetailView
from .models import Topic, TopicMemberShip, TopicPost  # Post, Category, Tag,  MoviePost, TopicPost
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm
from django.db.models import Q
from .forms import TopicPostForm
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse
# from django.contrib.auth.models import AbstractUser
# import datetime
# from django.core.paginator import Paginator
# from guardian.shortcuts import get_users_with_perms
# from guardian.shortcuts import get_objects_for_user
# from guardian.shortcuts import assign


def add_post(request, topic_id):
    if request.user.is_authenticated:  # 发帖
        # post_list = Post.objects.all().order_by('-created_time')
        topic = get_object_or_404(Topic, pk=topic_id)
        print("小组名称：")
        print(topic.name)
        print("小组id：")
        print(topic_id)
        form = TopicPostForm(request.POST)
        # 判断request的请求方法，如果是post方法，那么就处理数据
        if form.is_valid():
            # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            # post = form.save(commit=False)
            # 将评论和被评论的文章关联起来。
            title = request.POST.get("title", "")
            body = request.POST.get("body", "")
            if len(title) == 0:
                messages.error(request, '标题不能为空!')
                return redirect(topic)

            if len(body) < 25:
                messages.error(request, '评论字数应不少于25字!')
                return redirect(topic)
            post = TopicPost(title=title, body=body, topic=topic, author=request.user)

            print("提交的用户是：")
            print(request.user)
            # 最终将评论数据保存进数据库，调用模型实例的 save 方法
            # topic.save()
            post.save()
            # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            messages.add_message(request, messages.SUCCESS, '小组帖子发表成功！', extra_tags='success')
            return redirect(topic)

        # 检查到数据不合法，我们渲染一个预览页面，用于展示表单的错误。
        # 注意这里被评论的文章 post 也传给了模板，因为我们需要根据 post 来生成表单的提交地址。
        '''context = {
            'post': topic,
            'form': form,
        }'''
        messages.add_message(request, messages.ERROR, '帖子发表失败！请增加你发表帖子的字数。', extra_tags='danger')
        return redirect(topic)
    else:
        messages.add_message(request, messages.ERROR, "还未登录,请先登录")
        return render(request, '../../Movie/templates/login.html', {'错误': '还未登录！'})


# 添加为小组成员
def add_topic(request, pk):
    if request.method == 'GET':
        if request.user.is_authenticated:

            topic_now = Topic.objects.filter(pk=pk).first()
            user_now = User.objects.filter(username=request.user.username).first()
            mm = TopicMemberShip.objects.filter(person=user_now, topic=topic_now)
            if not mm:
                m1 = TopicMemberShip.objects.create(person=user_now, topic=topic_now, date_join=timezone.now())
            messages.add_message(request, messages.SUCCESS, "加入小组成功")
            return redirect(topic_now)

        else:
            messages.add_message(request, messages.ERROR, "还未登录,请先登录")
            return render(request, '../../Movie/templates/login.html', {'错误': '还未登录！'})
    else:
        return render(request, '../../Movie/templates/login.html')


# 管理员添加
def add_topicmanager(request, name):
    if request.method == 'GET':
        if request.user.is_authenticated:

            topic_now = Topic.objects.filter(name=name).first()
            user_now = User.objects.filter(username=request.user.username).first()
            gg = TopicPost.objects.filter(topic=topic_now)
            if topic_now:
                for gp in gg:
                    assign_perm('topicpost_delete', user_now, gp)

            messages.add_message(request, messages.SUCCESS, "申请管理员成功")
            return redirect(topic_now)

        else:
            messages.add_message(request, messages.ERROR, "还未登录,请先登录")  # 对于登陆的处理，记得模板跳转
            return render(request, '../../Movie/templates/login.html', {'错误': '还未登录！'})
    else:
        return render(request, '../../Movie/templates/login.html')


# 删除小组内的帖子
def deletetopicPost(request, pk, pkk):
    topicp = TopicPost.objects.get(pk=pk)
    topicp.delete()
    topic = Topic.objects.get(pk=pkk)
    messages.add_message(request, messages.SUCCESS, "删除帖子成功")
    return redirect(topic)


# 置顶帖子
def topentopicPost(request, pk, pkk):
    topicp = TopicPost.objects.get(pk=pk)
    topicp.top = True
    topicp.top_time = timezone.now()
    topicp.save()
    topic = Topic.objects.get(pk=pkk)
    messages.add_message(request, messages.SUCCESS, "帖子置顶成功")
    return redirect(topic)


def imtopicPost(request, pk, pkk):
    topicp = TopicPost.objects.get(pk=pk)
    topicp.im = True
    topicp.save()
    topic = Topic.objects.get(pk=pkk)
    messages.add_message(request, messages.SUCCESS, "帖子设精华成功")
    return redirect(topic)


class TopicsIndexView(ListView):
    model = Topic  # 告诉 django 我们要取的数据库模型是class topic
    template_name = 'topics_index.html'
    context_object_name = 'topics_list'


# paginate_by = 10


# class topicPostView(ListView):
#     model = topicPost
#     template_name = 'topic_detail.html'
#     context_object_name = 'topic_post'
#
#     def get_queryset(self):
#         c = topic.objects.filter(pk=self.kwargs['pk']).first()
#
#         return topicPost.objects.filter(topic=c).order_by('-top_time', 'created_time')
#
#     def get_object(self, queryset=None):
#         post = super().get_object(queryset=None)
#         #        md = markdown.Markdown(extensions=[
#         #            'markdown.extensions.extra',
#         #            'markdown.extensions.codehilite',
#         #            TocExtension(slugify=slugify),
#         #        ])
#         #        post.members = md.convert(post.members)
#         #        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
#         #        post.toc = m.topic(1) if m is not None else ''
#         return post


# class topicPostView(DetailView):
#     model = topicPost
#     template_name = 'topic_detail.html'
#
#     def get_context_data(self, **kwargs):
#         c = topic.objects.get(id=self.kwargs['pk'])
#
#         context = {'topic': c,
#                    'topic_post': topicPost.objects.filter(topic=c).order_by('-top_time', 'created_time'),
#                    'id': self.kwargs['pk']}
#         # context = super.get_context_data(**kwargs)
#         # context['id'] = kwargs['pk']
#         return context


def topicPostView(request, pk):
    c = Topic.objects.get(id=pk)
    context = {'topic': c,
               'topic_post': TopicPost.objects.filter(topic=c).order_by('-top_time', 'created_time'),
               'id': pk}
    return render(request, 'topic_detail.html', context)


class TopicDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = TopicPost
    template_name = 'topic_detailmore.html'
    context_object_name = 'topicpost'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(TopicDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()
        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 记得在顶部引入 TocExtension 和 slugify
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
        return post


def topic_search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('topic:topics_index')

    topics_list = Topic.objects.filter(Q(name__icontains=q))
    return render(request, 'topics_index.html', {'topics_list': topics_list})


def topic_post_search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('topic:topics_index')

    topic_post = TopicPost.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'topic_search_result.html', {'topic_post': topic_post})
