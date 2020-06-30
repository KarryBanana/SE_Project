from django.urls import path  # 导入path函数
from . import views  # 从当前的目录下导入views模块

app_name = 'topic'
urlpatterns = [  # 网址和处理函数的关系写在urlpatterns列表里面
    path('topics_index/', views.TopicsIndexView.as_view(), name='topics_index'),
    path('topics/<int:pk>', views.topicPostView, name='topic_detail'),
    path('topicpost/<int:pk>', views.TopicDetailView.as_view(), name='topic_detailmore'),
    path('add/<int:topic_id>', views.add_post, name='add'),
    path('topic_search/', views.topic_search, name='topic_search'),
    path('topic_post_search/', views.topic_post_search, name='topic_post_search'),
    path('topics_index/<int:pk>', views.add_topic, name='addtopic'),
    path('topics_index/<str:name>', views.add_topicmanager, name='addtopicmanager'),
    path(r'delete/<int:pk>/<int:pkk>', views.deletetopicPost, name='delete_topicpost'),
    path(r'top/<int:pk>/<int:pkk>', views.topentopicPost, name='topen_topicpost'),
    path(r'im/<int:pk>/<int:pkk>', views.imtopicPost, name='im_topicpost'),
    # path('topic_in/', views.topicPostView.as_view(), name='topic_in'),

]
