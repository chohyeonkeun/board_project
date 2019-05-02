from django.shortcuts import render

from django.shortcuts import redirect

# Create your views here.
# CRuDL - 이미지를 띄우는 방법
# 제네릭 뷰
# 쿼리셋 변경하기, context_data 추가하기, 권한 체크
# 함수형 뷰 <-> 클래스형 뷰

from .models import Photo

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.views.generic.list import ListView

from django.views.generic.detail import DetailView

from django.http import HttpResponseRedirect

from django.http import HttpResponseForbidden

from django.contrib import messages

from django.shortcuts import redirect

class PhotoList(ListView):
    model = Photo
    template_name = 'photo/photo_list.html'


class PhotoCreate(CreateView):
    model = Photo
    fields = ['author', 'image', 'text']
    template_name_suffix = '_create'

    def form_valid(self, form):
        # 입력된 자료가 올바른지 체크
        form.instance.author_id = self.request.user.id  # form.instance.[필드명]_id
        if form.is_valid():
            # 올바르다면,
            # form : 모델 폼
            form.instance.save()
            return redirect('/')
        else:
            # 올바르지 않다면,
            return self.render_to_response({'form':form})  # render 함수 쓰는게 더 좋

class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['author', 'image', 'text']
    template_name_suffix = '_update'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, "수정할 권한이 없습니다.")
            return HttpResponseRedirect(object.get_absolute_url())
        else:
            return super(PhotoUpdate, self).dispatch(request, *args, **kwargs)


class PhotoDelete(DeleteView):
    model = Photo
    template_name_suffix = '_delete'
    success_url = '/'

    # Life cycle - iOS, Android, Vue, React, Django, Rails
    # 모든 Framework는 라이프 사이클이 존재 --> 어떤 순서로 구동이 되느냐?
    # URLConf -> View -> Model 순으로 동작
    # 라이프 사이클 : 어떤 뷰를 구동할 때 그 안에서 동작하는 순서

    # 사용자가 접속했을 때 get인지 post인지 등을 결정하고 분기하는 부분
    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, "삭제할 권한이 없습니다.")
            return HttpResponseRedirect(object.get_absolute_url())
        else:
            return super(PhotoDelete, self).dispatch(request, *args, **kwargs)

    # 로직을 수행하고, 템플릿을 랜더링한다.
    # def get(self, request, *args, **kwargs):
    #     object = self.get_object()
    #     if object.author != request.user:
    #         messages.warning(request, "삭제할 권한이 없습니다.")
    #         return HttpResponseRedirect(object.get_absolute_url())
    #         # 삭제 페이지에서 권한이 없다! 라고 띄우는 방법
    #         # 원래 디테일 페이지로 돌아가서 삭제에 실패했습니다! 라고 띄우는 방법
    #     else:
    #         super(PhotoDelete, self).get(request, *args, **kwargs)
    # def post(self, request, *args, **kwargs):
    #     pass
    #
    # def get_object(self, queryset=None):
    #     # 해당 쿼리셋을 이용해서 현재 페이지에 필요한 object를 인스턴스화 한다.
    #     pass
    #
    # def get_queryset(self):
    #     # 어떻게 데이터를 가져올 것이냐?
    #     pass

class PhotoDetail(DetailView):
    model = Photo
    template_name_suffix = '_detail'



from django.views.generic.base import View

class PhotoLike(View):
    def get(self, request, *args, **kwargs):
        # like를 할 정보가 있다면 진행, 없다면 중단
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            #1. 어떤 포스팅?
            # url : www.naver.com/blog/like/?photo_id=1
            # request.GET.get('photo_id')
            # 단url : www.naver.com/blog/like/1/
            # path('blog/like/<int:photo_id>/'
            # kwargs['photo_id']
            # 2. 누가?
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.like.all():
                    photo.like.remove(user)
                else:
                    photo.like.add(user)
            return HttpResponseRedirect('/')

class PhotoSaved(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.saved.all():
                    photo.saved.remove(user)
                else:
                    photo.saved.add(user)
            return HttpResponseRedirect('/')

class PhotoSaveList(ListView):
    model = Photo
    template_name_suffix = '_slist'

