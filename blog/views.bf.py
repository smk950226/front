from django.shortcuts import render, get_object_or_404, resolve_url
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Post, Comment
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from .serializers import PostSerializer
from rest_framework.renderers import JSONRenderer
from django.template.defaultfilters import truncatewords
from .forms import CommentForm

class PostListView(ListView):
    model = Post
    paginate_by=10

    def get_template_names(self):
        if self.request.is_ajax():
            return ['blog/_post_list.html']
        return ['blog/index.html']


index = PostListView.as_view(model=Post, template_name='blog/index.html', paginate_by=10)


class PostDetailView(DetailView):
    model = Post

    def render_to_response(self, context):
        if self.request.is_ajax():
            return JsonResponse({
                'title': self.object.title,
                'summary': truncatewords(self.object.content,100),
            })
        return super().render_to_response(context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


post_detail = PostDetailView.as_view()


post_edit = UpdateView.as_view(model=Post, fields='__all__')


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')


post_delete = PostDeleteView.as_view()

post_new = CreateView.as_view(model=Post, fields='__all__')


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        response = super().form_valid(form)
        
        if self.request.is_ajax():
            return JsonResponse({
                'id': comment.id,
                'message': comment.message,
                'updated_at': comment.updated_at,
                'edit_url': resolve_url('blog:comment_edit', comment.post.pk, comment.pk),
                'delete_url': resolve_url('blog:comment_delete', comment.post.pk, comment.pk),
            })
        return response
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(dict(form.errors, is_success = False))
        return super().form_invalid(form)

    def get_success_url(self):
        return resolve_url(self.object.post)

comment_new = CommentCreateView.as_view()


class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        return resolve_url(self.object.post)


comment_edit = CommentUpdateView.as_view()


class CommentDeleteView(DeleteView):
    model = Comment
    
    def get_success_url(self):
        return resolve_url(self.object.post)


comment_delete = CommentDeleteView.as_view()

def post_list_json(request):
    qs = Post.objects.all()
    
    serializer = PostSerializer(qs, many=True)
    json_utf8_string = JSONRenderer().render(serializer.data)
    return HttpResponse(json_utf8_string, content_type='application/json; charset=utf-8')
