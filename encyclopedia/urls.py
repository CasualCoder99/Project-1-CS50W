from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/",views.title_view,name='title_view'),
    path("search/",views.search,name='search'),
    path("new/",views.new_post,name='new_post'),
    path("random/",views.get_random,name='get_random'),
    path("edit/<str:title>",views.edit_entry,name='edit_entry')
]
