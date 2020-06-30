from django.urls import path  # 导入path函数
from . import views  # 从当前的目录下导入views模块

app_name = 'group_func'
urlpatterns = [  # 网址和处理函数的关系写在urlpatterns列表里面
    path('groups_index/', views.GroupsIndexView.as_view(), name='groups_index'),
    path('groups/<int:pk>', views.GroupPostView, name='group_detail'),
    path('grouppost/<int:pk>', views.GroupDetailView.as_view(), name='group_detailmore'),
    path('add/<int:group_id>', views.add_post, name='add'),
    path('group_search/', views.group_search, name='group_search'),
    path('group_post_search/', views.group_post_search, name='group_post_search'),
    path('groups_index/<int:pk>', views.add_group, name='addgroup'),
    path('groups_index/<str:name>', views.add_groupmanager, name='addgroupmanager'),
    path(r'delete/<int:pk>/<int:pkk>', views.deleteGroupPost, name='delete_grouppost'),
    path(r'top/<int:pk>/<int:pkk>', views.topenGroupPost, name='topen_grouppost'),
    path(r'im/<int:pk>/<int:pkk>', views.imGroupPost, name='im_grouppost'),
    # path('group_in/', views.GroupPostView.as_view(), name='group_in'),

]
