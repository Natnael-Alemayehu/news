from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import ListView, DetailView, FormView

from .models import Article
from .forms import CommentFrom


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "article_list.html"


class CommentGet(DetailView):
    model = Article
    template_name = "article_detail.html"

    def get_context_data(self, **kwargs: reverse_lazy):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentFrom()
        return context


class CommentPost(SingleObjectMixin, FormView):
    model = Article
    form_class = CommentFrom
    template_name = "article_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        article = self.object
        return reverse("article_detail", kwargs={"pk": article.pk})


class ArticleDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = (
        "title",
        "body",
    )
    template_name = "article_edit.html"

    def test_func(self) -> bool | None:
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")

    def test_func(self) -> bool | None:
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ("title", "body")
    template_name = "article_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
