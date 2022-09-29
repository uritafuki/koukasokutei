import logging

from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages

from journal.models import Journal
from .forms import InquiryForm
from .forms import InquiryForm, JournalCreateForm


# Create your views here.
class IndexView(generic.TemplateView):
    template_name = "base.html"


class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('journal:inquiry')


class JournalListView(LoginRequiredMixin, generic.ListView):
    model = Journal
    template_name = 'journal_list.html'
    paginate_by = 2

    def get_queryset(self):
        diaries = Journal.objects.filter(user=self.request.user).order_by('-created_at')
        return diaries


    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        '''logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))'''
        return super().form_valid(form)


class JournalDetailView(LoginRequiredMixin, generic.DetailView):
    model = Journal
    template_name = 'journal_detail.html'


class JournalCreateView(LoginRequiredMixin, generic.CreateView):
    model = Journal
    template_name = 'journal_create.html'
    form_class = JournalCreateForm
    success_url = reverse_lazy('journal:journal_list')

    def form_valid(self, form):
        journal = form.save(commit=False)
        journal.user = self.request.user
        journal.save()
        messages.success(self.request, '日記を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "日記の作成に失敗しました。")
        return super().form_invalid(form)


class JournalUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Journal
    template_name = 'journal_update.html'
    form_class = JournalCreateForm

    def get_success_url(self):
        return reverse_lazy('journal:journal_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '日記を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "日記の更新に失敗しました。")
        return super().form_invalid(form)


class JournalDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Journal
    template_name = 'journal_delete.html'
    success_url = reverse_lazy('journal:journal_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "日記を削除しました。")
        return super().delete(request, *args, **kwargs)