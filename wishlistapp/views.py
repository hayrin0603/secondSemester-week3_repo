from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from wishlistapp.forms import BlogForm
from .models import Blog, Wishlist


# Create your views here.
def index(request):
    return render(request, 'index.html')

def new(request):
    return render(request, 'new.html')

def create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # 현재 로그인된 사용자를 할당
            post.save()
            return redirect('read')
    else:
        form = BlogForm()
    return render(request, 'create.html', {'form': form})

def read(request):
    blogs = Blog.objects
    return render(request, 'read.html', {'blogs': blogs})

# 요청받은 게시물의 상세 정보와 현재 사용자의 찜 여부를 보여주기 위한 기능 구현
def detail(request, id): #요청과 게시물의 ID를 매개변수로 받아 해당 게시물의 상세 정보를 보여줌
    blog = get_object_or_404(Blog, id=id) #get_object_or_404 함수 -> Blog 모델에서 주어진 게시물 ID 가져오기 / 없으면 404 페이지
    already_in_wishlist = False #변수 False 값으로 초기화
    if request.user.is_authenticated: #user 정보 인증(로그인 된 상태일 때만 찜 여부를 판단)
        already_in_wishlist = Wishlist.objects.filter(user=request.user, post=blog).exists() 
        #Wishlist 모델에서 현재 사용자와 주어진 게시물이 일치하는 찜 목록이 있는 지 확인 (찜 여부 판단)

    return render(request, 'detail.html', {'blog':blog, 'already_in_wishlist': already_in_wishlist})
    #'detial.html' 템플릿 렌더링하여 응답 -> blog 변수에는 가져온 게시물 정보 전달, already_in_wishlist 변수에는 찜 여부 전달


def wishlist(request): #요청 받아와서 현재 사용자의 찜 목록을 보여주는 view
    user = request.user #현재 로그인 된 사용자를 가져와서 user 변수에 저장
    wishlists = Wishlist.objects.filter(user=user) #찜 목록 개체들 중 사용자가 찜한 항목만 filter
        
    return render(request, 'wishlist.html', {'wishlists': wishlists})

#과제 부분
def write(request):
    user = request.user
    blogs = Blog.objects.filter(user=user)

    return render(request, 'write.html', {'blogs' : blogs})


@login_required    # 해당 뷰에 접근하기 전에 사용자가 로그인 되어있는지 확인 (데코레이터) -> 이미 찜 목록에 있는지 확인 후, 없으면 새로운 Wishlist 객체를 생성하는 view
def add_to_wishlist(request, post_id):
    post = get_object_or_404(Blog, pk=post_id) #주어진 게시물 ID에 해당하는 Blog 객체 가져오기 (없으면 404)
    already_in_wishlist = Wishlist.objects.filter(user=request.user, post=post).exists() #해당 사용자와 게시물이 일치하는 찜 목록이 존재하는지
    if not already_in_wishlist:
        wishlist_item = Wishlist.objects.create(user=request.user, post=post) #create-> 지정된 값을 가진 새로운 객체를 생성하고 저장
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, post_id):
    post = get_object_or_404(Blog, pk=post_id)
    wishlist_item = get_object_or_404(Wishlist, user=request.user, post=post) #get_object_or_404(Wishlist.user = request.user.post=post)->현재 사용자와 주어진 게시물이 일치하는 찜 목록 항목 가져오기
    wishlist_item.delete() #wishlist_item 변수에 저장하고 delete() 하기-> 찜 목록에서 해당 항목 삭제
    return redirect('wishlist')