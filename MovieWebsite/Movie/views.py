from django.shortcuts import render,redirect,get_object_or_404

from .models import Movie,MovieComment,MovieCommentReport,MovieUpDown
from django.forms.models import model_to_dict
from django.http import JsonResponse,HttpResponse
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .func import fuzzy_finder
from .func import GetOtherInfo
from django.views.generic.base import View
from .forms import CommentForm
from .forms import MovieCommentReportForm
from django.contrib import messages
from Book.models import Book
from topic.models import Topic
from group_func.models import Group
# Create your views here.


# 主页
def index(request):
    movieAll = Movie.objects.all()
    movies = []
    for movie in movieAll:
        if movie.rating >= 9.2:
            movies.append(movie)
    
    bookAll = Book.objects.all()
    books = []
    for book in bookAll:
        if book.rate >= 8.8:
            books.append(book)

    topicAll = Topic.objects.all()
    groupAll = Group.objects.all()
    return render(request, 'index_1.html',locals())


# 电影主页，显示大量电影
def movie_display(request):
    try:
        movies_list = Movie.objects.order_by('-year')  # 降序
        paginator = Paginator(movies_list, 25)
        page = request.GET.get('page')
        movies = paginator.get_page(page)
        return render(request, 'movie_display.html', {'movies': movies})  # 要改回来改成movie_display
    except:
        return render(request, '404.html')


# 某一电影的信息
def movie_detail(request,id):
    try:
        movie = Movie.objects.get(id=id)
        datas = Movie.objects.all()
        comments = MovieComment.objects.filter(movie=movie)
        comments_list = []
        for comment in comments:
            flag = False
            for report in comment.reports.all():
                if report.state == 1:
                    flag = True
                    break
            if not flag:
                comments_list.append(comment)

        recommend_list = []
        for data in datas:
            if movie.genres.split(',')[0] in data.genres:
                recommend_list.append(data)
        recommend_list.remove(movie)  # 去除重复项

        context = {'movie': movie, 'recommend_list': recommend_list[:12], 'comments_list': comments_list[:12]}
        print(comments_list)
        return render(request, 'movie_detail_show.html', context)
    except (KeyError, ValueError):
        return render(request, '404.html')
        # pass


# 页面旁有分类的标签，点击进去可以查看该类型的所有电影
def movie_search_by_genre(request, genre):
    try:
        datas = Movie.objects.all()
        movies_list = []
        for data in datas:
            if genre in data.genres:
                movies_list.append(data)

        paginator = Paginator(movies_list, 12)
        page = request.GET.get('page')
        movies = paginator.get_page(page)
        context = {'movies': movies}
        return render(request, 'movie_genre_show.html', context)
    except:
        return render(request, '404.html')


# 不同年份的电影，点击进去查看不同年份的电影
def movie_search_by_year(request, year):
    # 使用Movie.objects.filter(year = year)更佳
    try:
        datas = Movie.objects.all()
        movies_list = []
        for data in datas:
            if str(year) == data.year:
                movies_list.append(data)
            else:
                if str(year) == data.year[:2]:
                    movies_list.append(data)

        paginator = Paginator(movies_list, 12)
        page = request.GET.get('page')
        movies = paginator.get_page(page)
        context = {'movies': movies}
        return render(request, 'movie_year_show.html', context)
    except:
        return render(request, '404.html')


# def movie_search_form(request):
#     非模糊查询
#     title = request.POST.get('q')
#     movies_list = Movie.objects.filter(title=title)
#     paginator = Paginator(movies_list, 4)
#     page = request.GET.get('page')
#     movies = paginator.get_page(page)
#     return render(request, 'index.html', {'movies': movies})


def movie_search_form(request):
    # 模糊查询
    try:
        q = request.GET.get('q')
        collection = Movie.objects.all()
        movies_list = fuzzy_finder(q, collection)
        paginator = Paginator(movies_list, 30)
        page = request.GET.get('page')
        movies = paginator.get_page(page)
        return render(request, 'movie_search_show.html', {'movies': movies})
    except:
        return render(request, '404.html')


# 电影评论
def add_comment(request, id):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    add_form = CommentForm(request.POST)
    movie = get_object_or_404(Movie,id=id)
    if add_form.is_valid():

        content = request.POST.get("content", "")
        title = request.POST.get("newtitle","")
        print(title)
        print(content)
        if len(title) == 0:
            messages.error(request,'标题不能为空!')
            return redirect(movie)

        if len(content) < 25:
            messages.error(request, '评论字数应不少于25字!')
            return redirect(movie)

        comment = MovieComment(user=request.user, title=title, content=content, movie=movie)
        comment.save()
        comments_list = [] # 最终要展示的评论, 循环中筛选掉被举报的评论
        comments = MovieComment.objects.filter(movie=movie)
        for com in comments:
            flag = False
            for report in com.reports.all():
                if report.state == 1:
                    flag = True
                    break
            if not flag:
                comments_list.append(com)

        print("comment ok!")
        return redirect(movie)
    else:
        print("not ok!")
        messages.error(request, '评论失败!')
        return redirect(movie)


# 点赞评论
def digg(request):
    if request.method == 'POST':
        user = request.user
        if not user.is_authenticated:
            return render(request, 'login.html')

        # ajax 是json格式，特殊情况下需要反序列
        import json
        from django.db.models import F  # 利用F来做自加1操作

        movie_comment_pk = request.POST.get('movie_comment')
        print(movie_comment_pk)
        movie_comment = MovieComment.objects.get(pk=movie_comment_pk)
        print(movie_comment)
        is_up = json.loads(request.POST.get('is_up'))  # 必须反序列化才能为布尔值
        # 点赞人即当前登陆人

        print(user)
        # 过滤已经点赞或者踩了的
        obj = MovieUpDown.objects.filter(user=user, moviecomment=movie_comment).first()
        print(obj)
        # 返回json
        response = {'state': True, 'msg': None}
        print(response)

        if not obj:
            digg = MovieUpDown.objects.create(user=user, moviecomment=movie_comment, is_up=True)
            print(digg)
            # 生成了赞记录， 然后再来更新页面
            if is_up:  # 如果是赞就更新赞
                print("dz!")
                movie_comment.up_count += 1
                movie_comment.save()
                print(movie_comment.up_count)
                # MovieUpDown.objects.filter(user=user,moviecomment=movie_comment).update(up_count=F('up_count') + 1)
            else:
                # 踩的时候
                print("ts")
                movie_comment.down_count += 1
                movie_comment.save()
                print(movie_comment.down_count)
                #MovieUpDown.objects.filter(user=user,moviecomment=movie_comment).update(down_count=F('down_count') + 1)
        else:
            response['state'] = False
            response['handled'] = obj.is_up  # 将已经做过的操作提示

        return JsonResponse(response)  # 必须用json返回
    else:
        render(request,'movie_detail_show.html')


def reportMovieComment(request, comment_id):
    if request.method == "POST":
        bookCommentForm = MovieCommentReportForm(request.POST)
        if bookCommentForm.is_valid():
            print("ok!")
            print(comment_id)
            comment = get_object_or_404(MovieComment, pk=comment_id)
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

            commentReport = MovieCommentReport(reporter=request.user,reason=reason, movieComment=comment)
            commentReport.save()

            print("report ok!")
            return redirect(comment)
        else:
            print("not ok!")
            return HttpResponse("举报评论失败")


#  豆瓣API，暂且可能不使用


def search_by_id(request, id):
    try:
        data = model_to_dict(Movie.objects.get(id=id))
    except:
        raise Http404("Movie does not exist!!!!!!!!!!!!!")
    return JsonResponse(data, safe=False)


# a new api for reference
# def searchbyid(request):
#     try:
#         id = request.GET.get('id')
#         data = model_to_dict(Movie.objects.get(id=id))
#     except:
#         raise Http404("Movie does not exist!!!!!!!!!!!!!")
#     return JsonResponse(data, safe=False)


def search_by_title(request, title):
    try:
        data = model_to_dict(Movie.objects.get(title=title))
        return JsonResponse(data, safe=False)
    except:
        raise Http404("Movie does not exist!!!!!!!!!!!!!")


def search_by_original_title(request, original_title):
    try:
        data = model_to_dict(Movie.objects.get(original_title=original_title))
        return JsonResponse(data, safe=False)
    except:
        raise Http404("Movie does not exist!!!!!!!!!!!!!")


def search_by_genre(request, genre):
    try:
        data = list(Movie.objects.all())
        find = []
        json = {}
        for d in data:
            if genre in model_to_dict(d)['genres']:
                find.append(model_to_dict(d))
        json['subject'] = find
        return JsonResponse(json, safe=False)
    except:
        raise Http404("Movie does not exist!!!!!!!!!!!!!")


def search_by_year(request, year):
    try:
        data = list(Movie.objects.all())
        find = []
        json = {}
        for d in data:
            if year == model_to_dict(d)['year']:
                find.append(model_to_dict(d))
        json['subject'] = find
        return JsonResponse(json, safe=False)
    except:
        raise Http404("Movie does not exist!!!!!!!!!!!!!")





