from django.conf.urls import url
from listings import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search/(?P<search_string>[\w\W]+)/$', views.search, name='search'),

    url(r'^category/(?P<category>\w+)/$', views.view_category, name='view_category'),
    url(r'^tag/(?P<tag>[\w\W]+)/$', views.view_tag, name='view_tag'),
    url(r'^post/(?P<post_id>\d+)/$', views.view_post, name='view_post'),
    url(r'^favorites/add/(?P<post_id>\d+)/$', views.favorites_add, name='favorites_add'),

    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^myposts/view/$', views.my_posts, name='my_post'),
    url(r'^myposts/view/(?P<post_id>\d*)/$', views.view_my_post, name='view_my_post'),
    url(r'^myposts/edit/(?P<post_id>\d*)/$', views.edit_post, name='edit_post'),
    url(r'^myposts/upload/(?P<post_id>\d+)/$', views.upload_photos, name='upload_photos'),
    url(r'^myposts/delete/(?P<post_id>\d*)/$', views.delete_post, name='delete_post'),
    url(r'^myposts/publish/(?P<post_id>\d*)/$', views.publish_post, name='publish_post'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^signout/$', views.signout, name='signout'),
    ]