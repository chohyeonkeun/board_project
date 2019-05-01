from django.shortcuts import render

# Create your views here.
# CRuDL - 이미지를 띄우는 방법
# 제네릭 뷰
# 쿼리셋 변경하기, context_data 추가하기, 권한 체크
# 함수형 뷰 <-> 클래스형 뷰

from .models import Photo

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.views.generic.list import ListView

from django.views.generic.detail import DetailView

class PhotoList(ListView):
    model = Photo
    template_name = 'photo/photo_list.html'

from django.shortcuts import redirect
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
            return self.render_to_response({'form':form})

class PhotoDelete(DeleteView):
    model = Photo
    template_name_suffix = '_delete'

class PhotoDetail(DetailView):
    model = Photo
    template_name_suffix = '_detail'
