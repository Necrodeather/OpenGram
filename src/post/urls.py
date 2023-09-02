from django.urls import path

from post.views import CreatePostView, ListPostView

urlpatterns = [
    path("post/", CreatePostView.as_view()),
    path("post/all", ListPostView.as_view()),
]
