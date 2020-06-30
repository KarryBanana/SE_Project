from django.db.models import Q
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from .models import Book,BookComment,BookUpDown,BookCommentReport
from .forms import BookCommentForm, BookCommentReportForm
from django.core.paginator import Paginator
from django.contrib import messages
from Book.models import Book
from topic.models import Topic
from group_func.models import Group
from django.views.generic.base import View

# Create your views here.

# 分页器
def books_paginator(books,page):
    paginator = Paginator(books,4)
    if page is None:
        page = 1
    books = paginator.page(page)
    return books


# 图书主页展示一堆书
def book_display(request):
    try:
        movies_list = Book.objects.order_by('-rate')  # 降序
        paginator = Paginator(movies_list, 10)
        page = request.GET.get('page')
        books = paginator.get_page(page)
        return render(request, 'book_display.html', {'books': books})
    except:
        return render(request, '404.html')


# 搜索书籍
def book_search(request):
    print(request.method)
    if request.method == "POST":  # 如果搜索界面
        key = request.POST["q"]
        request.session["q"] = key  # 记录搜索关键词解决跳页问题
    else:
        key = request.GET.get("q")  # 得到关键词
        print(key)
        books = Book.objects.filter(
        Q(title__icontains=key) | Q(intro__icontains=key) | Q(author__icontains=key)
    )  # 进行内容的模糊搜索
    page_num = request.GET.get("page", 1)
    books = books_paginator(books, page_num)

    return render(request, "book_search.html", {"books": books})


# 具体某本书，展示推荐的书籍
def book_detail(request, id):
    try:
        book = Book.objects.get(id=id)
        # 展示所有评论
        comments = BookComment.objects.filter(book=book)

        comments_list = []
        for comment in comments:
            flag = False
            for report in comment.reports.all():
                if report.state == 1:
                    flag = True
                    break;
            if not flag:
                comments_list.append(comment)
        datas = Book.objects.all() # 展示推荐的书籍
        recommend_list = []
        for data in datas:
            if book.author in data.author or book.tags ==  data.tags:
                recommend_list.append(data)
        recommend_list.remove(book)  # 去除重复项
        context = {'book': book, 'recommend_list': recommend_list[:12]}
        return render(request, 'book_detail_show.html', locals())
    except (KeyError, ValueError):
        return render(request, '404.html')


#  查看不同类型的书籍
def book_search_by_genre(request, genre):
    try:
        datas = Book.objects.all()
        books_list = []  # 推荐书籍
        for data in datas:
            print(data.tags)
            if genre == data.tags.name:
                books_list.append(data)

        print(books_list)
        paginator = Paginator(books_list, 12)
        page = request.GET.get('page')
        books = paginator.get_page(page)
        context = {'books': books,'books_list':books_list}
        return render(request, 'book_genre_show.html', context)
    except:
        return render(request, '404.html')


# 书本评论
def add_comment(request, id):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    add_form = BookCommentForm(request.POST)
    book = get_object_or_404(Book,id=id)
    if add_form.is_valid():
        #content = add_form.cleaned_data['content']
        content = request.POST.get("content", "")
        print(content)

        if len(content) < 25:
            messages.error(request, '评论字数应不少于25字!')
            return redirect(book)

        #title = add_form.cleaned_data['title']
        title = request.POST.get("newtitle", "")
        
        if len(title) == 0:
            messages.error(request,'标题不能为空!')
            return redirect(book)

        print(title)
        comment = BookComment(user=request.user, title=title, content=content, book=book)
        comment.save()
        comments_list = [] # 最终要展示的评论, 循环中筛选掉被举报的评论
        reports = BookCommentReport.objects.all()
        print(reports)
        if reports:
            for report in reports:
                if report.state == 0:
                    comments_list.append(report.bookComment)

        print("comment ok!")
        return redirect(book)
    else:
        print("not ok!")
        messages.error(request, '评论失败!')
        return redirect(book)


# 点赞评论
def digg(request):
    user = request.user
    if not user.is_authenticated:
        return render(request, 'login.html')

    # ajax 是json格式，特殊情况下需要反序列
    import json
    from django.db.models import F  # 利用F来做自加1操作

    book_comment_pk = request.POST.get('book_comment')
    print(book_comment_pk)
    book_comment = BookComment.objects.get(pk=book_comment_pk)
    print(book_comment)
    is_up = json.loads(request.POST.get('is_up'))  # 必须反序列化才能为布尔值
    # 点赞人即当前登陆人

    print(user)
    # 过滤已经点赞或者踩了的
    obj = BookUpDown.objects.filter(user=user, bookcomment=book_comment).first()
    print(obj)
    # 返回json
    response = {'state': True, 'msg': None}
    print(response)

    if not obj:
        BookUpDown.objects.create(user=user, bookcomment=book_comment, is_up=True)
        # 生成了赞记录， 然后再来更新页面
        if is_up:  # 如果是赞就更新赞
            print("dz!")
            book_comment.up_count += 1
            book_comment.save()
            # MovieUpDown.objects.filter(user=user,moviecomment=movie_comment).update(up_count=F('up_count') + 1)
        else:
            # 踩的时候
            print("ts")
            book_comment.down_count += 1
            book_comment.save()
            #MovieUpDown.objects.filter(user=user,moviecomment=movie_comment).update(down_count=F('down_count') + 1)
    else:
        response['state'] = False
        response['handled'] = obj.is_up  # 将已经做过的操作提示

    return JsonResponse(response)  # 必须用json返回


def reportBookComment(request, comment_id):
    if request.method == "POST":
        bookCommentForm = BookCommentReportForm(request.POST)
        if bookCommentForm.is_valid():
            print("ok!")
            print(comment_id)
            comment = get_object_or_404(BookComment, pk=comment_id)
            print(comment)
            title = request.POST.get("title","")
            reason = request.POST.get("reason","")
            print(title)
            print(reason)
            if len(title) == 0:
                messages.error(request, '标题不能为空!')
                return redirect(comment)
            if len(reason) <15:
                print("字太少了!")
                messages.error(request, '举报字数应不少于15字!')
                return redirect(comment)

            commentReport = BookCommentReportForm(reporter=request.user,reason=reason, bookComment=comment)
            commentReport.save()

            print("report ok!")
            return redirect(comment)
        else:
            print("not ok!")
            return HttpResponse("举报评论失败")

