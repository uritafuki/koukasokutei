from django.urls import path

from . import views


app_name = 'journal'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('inquiry/', views.InquiryView.as_view(), name="inquiry"),
    path('journal-list/', views.JournalListView.as_view(), name="journal_list"),
    path('journal-detail/<int:pk>/', views.JournalDetailView.as_view(), name="journal_detail"),
    path('journal-create/', views.JournalCreateView.as_view(), name="journal_create"),
    path('journal-update/<int:pk>/', views.JournalUpdateView.as_view(), name="journal_update"),
    path('journal-delete/<int:pk>/', views.JournalDeleteView.as_view(), name="journal_delete"),
]
