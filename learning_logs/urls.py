"""定义learning_logs的URL模式"""

from django.urls import path, re_path

from . import views

urlpatterns = [
    # 主页
    path('', views.index, name='index'),

    #显示所有的主题
    path('topics/', views.topics, name='topics'),

    #显示特定的主题
    path('topics/<int:topic_id>/', views.topic, name='topic'),

    #用于添加新主题的网页
    path('new_topic/', views.new_topic, name='new_topic'),

    # 用于添加新条目的网页
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),

    # 用于编辑条目的网页
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),

    # 用于删除自有条目的页面
    re_path('delete_entry/(?P<entry_id>\d+)/', views.delete_entry, name='delete_entry'),

    # 用于删除自有主题的页面
    re_path('delete_topic/(?P<topic_id>\d+)/', views.delete_topic, name='delete_topic'),
]