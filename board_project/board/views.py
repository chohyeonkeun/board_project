from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.db.models import Q
# QuerySet은 모델의 디폴트 매니저를 통해 실행한다.
import math
from .models import Document
def document_list(request):
    # QuerySet
    # 1. 객체를 선택
    # 2. 객체 생성
    # 3. 객체 필터링
    # 4. 객체 삭제
    page = int(request.GET.get('page', 1))
    # page가 없다면, default값 1로 설정  --> 127.0.0.1:8000/ 검색 --> 127.0.0.1:8000/?page=1
    # 페이지당 갯수
    paginated_by = 3
    # 1. 모델의 전체 데이터 불러오기
    # documents = Document.objects.all() # all 전체를 가져온다.  # Document.objects.filter(title__icontains="검색어")

    # request.METHOD.get --> 아이템 1개 가져온다 (데이터가 1개 이상일 경우 맨 마지막 데이터를 가져온다)
    # request.METHOD.getlist --> 리스트 형태로 가져온다.
    search_type = request.GET.getlist('search_type', None)
    # search_type = ['username', 'title', 'text']
    search_q = None
    search_key = request.GET.get('search_key', None)

    # 웹 애플리케이션 : 인프라 최적화, 소스코드 최적
    if search_key:
        # for type in search_type:
        #     if type == 'username':
        #         temp_q = Q(author__username__icontains=search_key)
        #         search_q = search_q | temp_q if search_q else temp_q
        #     else:
        #         temp_q = Q(type+"__icontains", search_key)    # 코드 수정 필요
        #         search_q = search_q | temp_q if search_q else temp_q
        # documents = get_list_or_404(Document, search_q)

        if 'title' in search_type:
            temp_q = Q(title__icontains=search_key)
            search_q = search_q | temp_q if search_q else temp_q
        if 'text' in search_type:
            temp_q = Q(text__icontains=search_key)
            search_q = search_q | temp_q if search_q else temp_q
        if 'username' in search_type:
            temp_q = Q(author__username__icontains=search_key)
            search_q = search_q | temp_q if search_q else temp_q
        documents = get_list_or_404(Document, search_q)



    # if search_key:
    #     documents = get_list_or_404(Document, title__icontains=search_key)
    else:
        # documents = get_list_or_404(Document)
        documents = Document.objects.all()
    # QuerySet 객체를 슬라이싱 할 때 [시작번호:끝번호]
    # 1페이지 - 0 ==== 3(뒷번호)
    # 2페이지 - paginated_by*(page-1) ==== 6
    # 3페이지 - paginated_by*(page-1) ==== 9
    total_count = len(documents)
    total_page = math.ceil(total_count/paginated_by)
    page_range = range(1, total_page+1)
    start_index = paginated_by * (page-1)
    end_index = paginated_by * page
    documents = documents[start_index:end_index]

    return render(request, 'board/document_list.html',
                  {'object_list':documents, 'total_page':total_page,
                   'page_range':page_range}) # context_value를 가져온다 {} - dic 형태


from .forms import DocumentForm
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
@login_required
# 로그인 한 유저만 작동하도록 진행
def document_create(request):
   # Document.object.create() - 실행과 동시에 DB에 삽입
   # 분기 - post, get
   if request.method == "POST":
       # 처리
       # request.POST : 폼에서 입력한 텍스트 데이터
       # request.FILES : 파일만 보낸다
       form = DocumentForm(request.POST, request.FILES)
       form.instance.author_id = request.user.id
       if form.is_valid():
           document = form.save()
           print(document)
           return redirect(reverse('board:detail', args=[document.id]))
   else:
       # 입력 창
       form = DocumentForm()

       return render(request, 'board/document_create.html',{'form':form})

def document_update(request, document_id):
   # 객체 불러와서, 데이터를 수정
   if request.method == "POST":
       # document = Document.objects.get(pk=document_id)
       document = get_object_or_404(Document, pk=document_id)
       form = DocumentForm(request.POST, request.FILES, instance=document)
       # document = Document.objects.get(pk=1)
       # document.id = None
       # document.save() --> 원래 기존 id 삭제하고 다시 만든다.(복사 느낌)
       # 모델폼을 사용할 때 instance를 넘겨주면, 해당 인스턴스값으로 초기화가 되고,
       # 만약 pk가 있는 instance(instance가 있으면 id 생성)라면, create가 아닌 update를 수행한다. 
       # (원래는 update 누르게 되면 create로 인식해서 동일한 입력으로 보고 수정 불가)
       # request.POST와 instance가 같이 전달되면 POST 데이터가 우선순위가 높다. --> instance 값 삭제되고, POST로 덮어씌운다.라는 느낌
       if form.is_valid():
           document = form.save()  # form.save() 하면 instance 생성 --> document 로 담는다
           return redirect(document)
   else:
       # document = Document.objects.get(pk=document_id)
       document = get_object_or_404(Document, pk=document_id)
       # modelform init with instance(model object) 구글 검색
       form = DocumentForm(instance=document)

   return render(request, 'board/document_update.html', {'form': form})

# ajax 사용하여 댓글 기능 구현
from django.template.loader import render_to_string
def comment_create(request, document_id):
    # is_ajax : ajax 기능에 의해 호출된 것인지 구분하기 위한 값
    is_ajax = request.POST.get('is_ajax')

    document = get_object_or_404(Document, pk=document_id)
    comment_form = CommentForm(request.POST)
    comment_form.instance.author_id = request.user.id
    comment_form.instance.document_id = document_id
    if comment_form.is_valid():
        comment = comment_form.save()

    # 만약 ajax에 의해 호출되었다면 redirection 없이 Json 형태로 응답
    if is_ajax:
        # html = """
        # <tr>
        # <td colspan="3">{}</td>
        # <td>{}</td>
        # <td>{}</td>
        # <td><a href="{}" class="btn btn-warning btn-sm">update</a></td>
        # <td><a href="{}" class="btn btn-danger btn-sm">delete</a></td>
        # </tr>
        # """.format(comment.text, comment.author.username, comment.created, "url1", "url2")
        # 데이터 만들어서 던져주기
        html = render_to_string('board/comment/comment_single.html',{'comment':comment})
        return JsonResponse({'html':html})
    # return redirect(reverse('board:detail', args=[document_id]))
    return redirect(document)

from .models import Comment
from django.contrib import messages

def comment_update(request, comment_id):
    is_ajax, data = (request.GET.get('is_ajax'), request.GET) if 'is_ajax' in request.GET else (request.POST.get('is_ajax', False), request.POST)

    comment = get_object_or_404(Comment, pk=comment_id)
    document = get_object_or_404(Document, pk=comment.document.id)
    if request.user != comment.author:
        messages.warning(request, "권한 없음")
        return redirect(document)

    if is_ajax:
        form = CommentForm(data, instance=comment)
        if form.is_valid():
            form.save()
            return JsonResponse({'works':True})

    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(document)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'board/comment/comment_update.html', {'form':form})

def comment_delete(request, comment_id):
    is_ajax = request.GET.get('is_ajax') if 'is_ajax' in request.GET else request.POST.get('is_ajax',False)
    comment = get_object_or_404(Comment, pk=comment_id)
    document = get_object_or_404(Document, pk=comment.document.id)

    if request.user != comment.author and not request.user.is_staff and request.user != document.author:
        messages.warning(request, "권한 없음")
        return redirect(document)

    if is_ajax:
        comment.delete()
        return JsonResponse({"works":True})

    # if request.method == "POST":
    #     comment.delete()
    #     return redirect(document)
    else:
        return render(request, 'board/comment/comment_delete.html', {'object': comment})

def document_detail(request, document_id):
   # document = Document.objects.get(pk=document_id)
   document = get_object_or_404(Document, pk=document_id)

   # comment_form = CommentForm()
   # comment_form이 request.method == "POST" 위에 위치했을 때는 입력폼에 입력값이 Comment 클릭해도 없어지지 않음

   # if request.method =="POST":
   #     comment_form = CommentForm(request.POST)
   #     comment_form.instance.author_id = request.user.id
   #     comment_form.instance.document_id = document_id
   #     if comment_form.is_valid():
   #         comment = comment_form.save()

   comment_form = CommentForm()
   # comment_form이 request.method == "POST" 아래 위치할 경우, Comment 클릭하면 입력값 초기화
   comments = document.comments.all()


   return render(request, 'board/document_detail.html', {'object':document, 'comments':comments, 'comment_form':comment_form})

def document_delete(request, document_id):
   # 객체 불러와서, delete만 호출
   document = get_object_or_404(Document, pk=document_id)
   return render(request, 'board/document_delete.html', {'object':document})

from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount
# 시그널이 발생했을 때 실행될 함수
def naver_signup(request, user, **kwargs):
    social_user = SocialAccount.objects.filter(user=user)
    if social_user.exists():
        user.last_name = social_user[0].extra_data['name']
        user.save()
# 시그널과 해당 함수를 connect
# 시그널 연결 방법 2가지 : receiver 쓰는 방법, connect 쓰는 방법
user_signed_up.connect(naver_signup)


# 일반적인 경우, 데이터 전송하기 위해 json 사용
from django.http import JsonResponse

# ajax 연습
def get_data_ajax(request):
    data = {
        'name' : 'Jonus',
        'age' : 30,
        'bloodtype' : 'O형'
    }
    return JsonResponse(data)
