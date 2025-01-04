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
import cloudinary
from blogg.settings import CLOUDINARY_NAME, CLOUDINARY_KEY, CLOUDINARY_SECRET, EMAIL_HOST_USER
from rest_framework.response import Response
from rest_framework.decorators import api_view
import base64
from django.core.mail import send_mail
import re
import requests

#for cloudinary
cloudinary.config( 
  cloud_name = CLOUDINARY_NAME, 
  api_key =CLOUDINARY_KEY, 
  api_secret = CLOUDINARY_SECRET,
  api_proxy = "http://proxy.server:3128"
)

import cloudinary.uploader

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
    return render(request,'blog/detail.html',context)

#Updating posts
def UpdatePost(request,pk):
    post=Post.objects.get(id=pk)
    context={'post':post,'form':PostForm(request.POST or None, instance=post)}    
    if request.method=="POST":
        content_old=Post.objects.get(id=pk).content
        title=request.POST.get('title')
        local_body=request.POST.get('local_body')
        local_name=request.POST.get('local_name')
        main_img_new=request.FILES.get("main_img")
        content=request.POST.get('content')
        new_content=content
        old_imgs=[]
        new_imgs=[]
        for url in re.findall(r"<img[^>]* src=\"([^\"]*)\"[^>]*>", content_old):
            old_imgs.append(url)
        for url in re.findall(r"<img[^>]* src=\"([^\"]*)\"[^>]*>", content):
            new_imgs.append(url)
            if not url in old_imgs:
                upload=cloudinary.uploader.upload(request.build_absolute_uri(url), public_id = url[36:],folder="summernote")
                new_content=new_content.replace(url,upload["url"])
        for test in old_imgs:
            if test not in new_imgs:
                cloudinary.uploader.destroy("summernote/"+test[72:len(test)-4])
        Post.objects.filter(id=pk).update(title=title,local_body=local_body,local_name=local_name,content=new_content)
        if main_img_new:
            obj=Post.objects.get(id=pk)
            prev_m_img_url=obj.m_img_url
            cloudinary.uploader.destroy(prev_m_img_url[61:len(prev_m_img_url)-4])
            m_img_url=cloudinary.uploader.upload(main_img_new,folder="main_imgs")
            obj.m_img_url=m_img_url["url"]

            # previous_img=obj.main_img
            # obj.main_img=main_img_new
            obj.save(update_fields=['m_img_url'])
            # previous_img.delete(False)
        return redirect('blogdetail',pk=pk)
    return render(request,'blog/post_update.html',context)

#Deleting posts
def DeletePost(request,pk):
    if request.method=="POST":
        post=Post.objects.get(id=pk)
        if request.user==post.author:
            try:
                # img=post.main_img
                content=post.content
                for url in re.findall(r"<img[^>]* src=\"([^\"]*)\"[^>]*>", content):
                    public_id=url[72:len(url)-4]
                    cloudinary.uploader.destroy("summernote/"+public_id)
                m_img_url=post.m_img_url
                cloudinary.uploader.destroy(m_img_url[61:len(m_img_url)-4])
                post.delete()
                # img.delete(False)
                return redirect("blog")
            except:
                return redirect('blogdetail',pk=pk)
        else:
            return redirect('blogdetail',pk=pk)
    return redirect("blog")

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
        new_content=content
        m_img_url=cloudinary.uploader.upload(main_img,folder="main_imgs")    
        for url in re.findall(r"<img[^>]* src=\"([^\"]*)\"[^>]*>", content):
            upload=cloudinary.uploader.upload(request.build_absolute_uri(url), public_id = url[36:],folder="summernote")
            new_content=new_content.replace(url,upload["url"])
        Post.objects.create(title=title,local_body=local_body,local_name=local_name,content=new_content,author=request.user,m_img_url=m_img_url["url"])
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
            links=json.loads(user.profile.links.replace("'", '"'))
            posts=Post.objects.filter(author=user)
            return render(request,'blog/myblogs.html',{'author':user,'posts':posts,'links':links})
    else:
        if pre_url is not None:
            messages.error(request,'You must be logged in to visit profiles..')
            return redirect(pre_url)
        messages.error(request,'You must be logged in to visit profiles..')
        return redirect("blog")

@api_view(['GET'])
def get_titles(request):
    o=Post.titles_list()
    k=list(o)
    next_id = Post.objects.latest('created').id+1
    return Response({'data':k,'next':next_id})

import io, base64
from PIL import Image

@api_view(['POST'])
def post_ai(request):
    title=request.data.get('title')
    local_body=request.data.get('local_body')
    main_img=request.data.get("main_img")
    content=request.data.get('content')
    for_avatar=request.data.get('for_avatar')
    
    image = base64.b64decode(str(main_img))       
    imagePath = 'temp_ai.jpeg'
    img = Image.open(io.BytesIO(image))
    img.save(imagePath, 'jpeg')

    m_img_url=cloudinary.uploader.upload('temp_ai.jpeg',folder="main_imgs")    
    Post.objects.create(title=title,local_body=local_body,local_name="NA",content=content,author=User.objects.get(id=2),m_img_url=m_img_url["url"],for_avatar=for_avatar)
    send_mail_about_new_blog(title,content,m_img_url["url"])
    return Response({"msg":"Done!"})

def send_mail_about_new_blog(blog_title, blog_content, image):
    subject = 'New Blog Post Added-AI'
    message = f'Hi,\n\nA new blog post has been added.\n{blog_title}\nContent:{blog_content}\nImage:{image}'
    email_from = EMAIL_HOST_USER
    recipient_list = ['neptravelblog@gmail.com ']  # Replace with your email
    send_mail(subject, message, email_from, recipient_list)

def audio_to_base64(audio_url):
    try:
        response = requests.get(audio_url)
        response.raise_for_status()
        audio_base64 = base64.b64encode(response.content).decode('utf-8')
        return audio_base64
    except requests.exceptions.RequestException as e:
        print(f"Error fetching audio file: {e}")
        return None

def read_json_transcript(json_url):
    try:
        response = requests.get(json_url)
        response.raise_for_status()
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching JSON file: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON content: {e}")
        return None

@api_view(['POST'])
def audio_visual(request):
    final_data=[]
    q=request.data.get("post_num")
    data=Post.objects.get(id=q).for_avatar
    total=len(data[0])
    for i in range(total):
        message={"text":"Random","facialExpression": "smile","animation": "Idle","audio":audio_to_base64(data[0][i]),"lipsync":read_json_transcript(data[1][i])}
        final_data.append(message)
    return Response({"for_avatar":final_data})

#for ajax
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'