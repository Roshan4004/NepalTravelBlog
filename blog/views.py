from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from .models import Post,Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect
from django.db.models import Q
from django.shortcuts import render,redirect,get_object_or_404
from .forms import PostForm
from django.contrib.auth.models import User
import json
#Showing the lists/posts
def PostList(request):
    search_task=request.GET.get('search')
    if search_task:
        posts = Post.objects.filter(Q(local_name__icontains=search_task) |  Q(local_body__icontains=search_task) | Q(title__icontains=search_task))
        if posts:
            return render(request,'blog/index.html',{'post_list':posts})
        else:
            return render(request,'blog/index.html',{'post_list':Post.objects.all(),'error':'No posts found with given parameters'})
    objects=Post.objects.all()
    context={'post_list':objects}
    return render(request,'blog/index.html',context)

def PostLike(request, pk):
    post = Post.objects.filter(id=pk).first()
    print(post.likes)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('blogdetail', args=[str(pk)]))

def test(request):
    return render(request,'blog/test.html')

def PostDetail(request,pk):
    if is_ajax(request=request):
        if request.POST.get('form')=='cmntupdatefunction':
            new_body=request.POST.get('new_body')
            post=Post.objects.get(id=pk)
            try:
                comment=Comment.objects.filter(post=post,id=request.POST.get('cmnt_id')).first()
                comment.body=new_body
                comment.save(update_fields=['body'])
                updated_body=comment.body
                response={'msg':'Comment Successfully Updated','updated_body':updated_body}
                return JsonResponse(response)
            except:
                response={'msg':'Error'}
                return JsonResponse(response)
        if request.POST.get('form')=='commentdeletefunction':
            id=request.POST.get("cmnt_id")
            post=Post.objects.get(id=pk)
            try:
                comment=Comment.objects.get(post=post,id=id)
                if comment.user==request.user:
                    comment.delete()
                    response={'msg':"done"}
                else:
                    response={'msg':"Error"}
                return JsonResponse(response)
            except:
                response={'msg':'Error'}
                return JsonResponse(response)
        if request.GET.get('form')=='cmntlikefunction':
            post=Post.objects.get(id=pk)
            comment=Comment.objects.filter(post=post,id=request.GET.get('cmnt_id')).first()
            try:
                if comment.cmnt_likes.filter(id=request.user.id).exists():
                    comment.cmnt_likes.remove(request.user)
                    new_number_of_comm_likes=comment.number_of_comment_likes()
                    response={'color':'transparent','new_number_of_comm_likes':new_number_of_comm_likes}
                    return JsonResponse(response)
                else:
                    comment.cmnt_likes.add(request.user)
                    new_number_of_comm_likes=comment.number_of_comment_likes()
                    response={'color':'red','new_number_of_comm_likes':new_number_of_comm_likes}
                    return JsonResponse(response)
            except:
                response={'color':'','new_number_of_comm_likes':new_number_of_comm_likes}
                return JsonResponse(response)
        if request.GET.get('form')=='likefunction':
            post = Post.objects.filter(id=pk).first()
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
                new_number_of_likes=post.number_of_likes()
                response={'color':'transparent','new_number_of_likes':new_number_of_likes}
            else:
                post.likes.add(request.user)
                new_number_of_likes=post.number_of_likes()
                response={'color':'red','new_number_of_likes':new_number_of_likes}
            return JsonResponse(response)
        response={'color':'','new_number_of_likes':''}
        return JsonResponse(response)
    if request.method=="POST":
        body=request.POST.get('comment')
        post=Post.objects.get(id=pk)
        Comment.objects.create(post=post,body=body,user=request.user)
        return redirect('blogdetail',pk=pk)
    post=Post.objects.get(id=pk)
    comment=Comment.objects.filter(post=post)
    commented= False
    if comment.filter(user=request.user.id).exists():
        commented= True
    likes_connected=get_object_or_404(Post, id=pk)
    liked=False
    if likes_connected.likes.filter(id=request.user.id).exists():
        liked=True
    author=post.author
    author_posts=Post.objects.filter(author=author).exclude(id=post.id)
    context={'post':post,'number_of_likes':likes_connected.number_of_likes(),'post_is_liked':liked,'comment':comment,'post_is_commented':commented,'author_posts':author_posts[:2]}
    # print(post.content)
    return render(request,'blog/detail.html',context)

#Updating posts
def UpdatePost(request,pk):
    post=Post.objects.get(id=pk)
    context={'post':post,'form':PostForm(request.POST or None, instance=post)}    
    if request.method=="POST":
        title=request.POST.get('title')
        local_body=request.POST.get('local_body')
        local_name=request.POST.get('local_name')
        main_img_new=request.FILES.get("main_img")
        content=request.POST.get('content')
        Post.objects.filter(id=pk).update(title=title,local_body=local_body,local_name=local_name,content=content)
        if main_img_new:
            obj=Post.objects.get(id=pk)
            previous_img=obj.main_img
            obj.main_img=main_img_new
            obj.save(update_fields=['main_img'])
            previous_img.delete(False)
        return redirect('blogdetail',pk=pk)
    return render(request,'blog/post_update.html',context)

#Deleting posts
def DeletePost(request,pk):
    if request.method=="POST":
        post=Post.objects.get(id=pk)
        if request.user==post.author:
            try:
                img=post.main_img
                post.delete()
                img.delete(False)
                return redirect("blog")
            except:
                return redirect('blogdetail',pk=pk)
        else:
            return redirect('blogdetail',pk=pk)
    return redirect("blog")

import xml.etree.ElementTree,xml,re

CLEANR = re.compile('<.*?>') 

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

#Posting new datas
def postcreate(request):
    if not request.user.is_authenticated:
        messages.error(request,'You must be logged in to post')
        return redirect("/account/login1")
    context={'form':PostForm}
    if request.method=="POST":
        title=request.POST.get('title')
        local_body=request.POST.get('local_body')
        local_name=request.POST.get('local_name')
        main_img=request.FILES.get("main_img")
        content=request.POST.get('content')
        Post.objects.create(title=title,local_body=local_body,local_name=local_name,main_img=main_img,content=content,author=request.user)
        return redirect("blog")
    return render(request, 'blog/post.html',context)

#myblogs
def myblogs(request,pk):
    pre_url = request.META.get('HTTP_REFERER')
    if request.user.is_authenticated:
        if len(User.objects.filter(username=pk))<=0:
            messages.error(request,'Profile not found for given username..')
            return redirect("blog")
        else:
            user=User.objects.filter(username=pk).first()
            links=json.loads(user.profile.links)
            posts=Post.objects.filter(author=user)
            return render(request,'blog/myblogs.html',{'author':user,'posts':posts,'links':links})
    else:
        if pre_url is not None:
            messages.error(request,'You must be logged in to visit profiles..')
            return redirect(pre_url)
        messages.error(request,'You must be logged in to visit profiles..')
        return redirect("blog")

#for ajax
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'