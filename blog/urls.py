from django import views
from django.urls import path
from . import views
from blog.for_ai import test

urlpatterns = [
    path('',views.PostList,name="blog"),
    path('blogtest',views.test,name="blogtest"),
    # path('',views.check,name="check"),
    path('detail/<int:pk>/',views.PostDetail,name="blogdetail"),
    path('post-like/<int:pk>/',views.PostLike,name="postlike"),
    path('update/<int:pk>',views.UpdatePost,name="blogupdate"),
    path('delete/<int:pk>',views.DeletePost,name='blogdelete'),
    path('post/',views.postcreate,name="blogpost"),
    path('myblogs/<slug:pk>',views.myblogs,name="myblogs"),
    path('test/',test.ok,name="test"),
    path('task_status/',test.task_status,name="task_status")
]