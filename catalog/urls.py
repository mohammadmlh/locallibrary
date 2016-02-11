from django.urls import path, re_path
from . import views
app_name="catalog"

urlpatterns = [
    re_path(r'^$', views.Index.as_view(), name="index"),
    re_path(r'^books/$', views.BookListView.as_view(), name='books'),
    re_path(r'^authors/$', views.AuthorListView.as_view(), name='authors'),
    re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    re_path(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    re_path(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian.as_view(), name='renew-book-librarian'),

]
