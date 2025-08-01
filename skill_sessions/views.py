from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone

from .models import SkillSwapRequest, SkillSwapSession, SessionReview
from .forms import SkillSwapRequestForm, RequestResponseForm, SessionScheduleForm, SessionReviewForm
from skills.models import OfferedSkill, DesiredSkill

# Create your views here.

class RequestListView(LoginRequiredMixin, ListView):
    model = SkillSwapRequest
    template_name = 'skill_sessions/request_list.html'
    context_object_name = 'requests'
    
    def get_queryset(self):
        return SkillSwapRequest.objects.filter(
            requester=self.request.user
        ).select_related('recipient', 'offered_skill')


class SentRequestListView(LoginRequiredMixin, ListView):
    model = SkillSwapRequest
    template_name = 'skill_sessions/sent_requests.html'
    context_object_name = 'requests'
    
    def get_queryset(self):
        return SkillSwapRequest.objects.filter(
            requester=self.request.user
        ).select_related('recipient', 'offered_skill')


class ReceivedRequestListView(LoginRequiredMixin, ListView):
    model = SkillSwapRequest
    template_name = 'skill_sessions/received_requests.html'
    context_object_name = 'requests'
    
    def get_queryset(self):
        return SkillSwapRequest.objects.filter(
            recipient=self.request.user
        ).select_related('requester', 'offered_skill')


class SendRequestView(LoginRequiredMixin, CreateView):
    model = SkillSwapRequest
    form_class = SkillSwapRequestForm
    template_name = 'skill_sessions/send_request.html'
    success_url = reverse_lazy('skill_sessions:request_list')
    
    def form_valid(self, form):
        form.instance.requester = self.request.user
        form.instance.recipient_id = self.kwargs['user_id']
        return super().form_valid(form)


class RequestDetailView(LoginRequiredMixin, DetailView):
    model = SkillSwapRequest
    template_name = 'skill_sessions/request_detail.html'
    context_object_name = 'request'
    
    def get_queryset(self):
        return SkillSwapRequest.objects.filter(
            requester=self.request.user
        ) | SkillSwapRequest.objects.filter(
            recipient=self.request.user
        )


class RequestResponseView(LoginRequiredMixin, UpdateView):
    model = SkillSwapRequest
    form_class = RequestResponseForm
    template_name = 'skill_sessions/request_response.html'
    success_url = reverse_lazy('skill_sessions:received_requests')
    
    def get_queryset(self):
        return SkillSwapRequest.objects.filter(recipient=self.request.user)


@login_required
def cancel_request(request, pk):
    request_obj = get_object_or_404(SkillSwapRequest, pk=pk, requester=request.user)
    request_obj.status = 'cancelled'
    request_obj.save()
    return redirect('skill_sessions:request_list')


class SessionListView(LoginRequiredMixin, ListView):
    model = SkillSwapSession
    template_name = 'skill_sessions/session_list.html'
    context_object_name = 'sessions'
    
    def get_queryset(self):
        return SkillSwapSession.objects.filter(
            teacher=self.request.user
        ) | SkillSwapSession.objects.filter(
            learner=self.request.user
        )


class UpcomingSessionListView(LoginRequiredMixin, ListView):
    model = SkillSwapSession
    template_name = 'skill_sessions/upcoming_sessions.html'
    context_object_name = 'sessions'
    
    def get_queryset(self):
        return SkillSwapSession.objects.filter(
            scheduled_date__gte=timezone.now()
        ).filter(
            teacher=self.request.user
        ) | SkillSwapSession.objects.filter(
            scheduled_date__gte=timezone.now()
        ).filter(
            learner=self.request.user
        )


class SessionHistoryView(LoginRequiredMixin, ListView):
    model = SkillSwapSession
    template_name = 'skill_sessions/session_history.html'
    context_object_name = 'sessions'
    
    def get_queryset(self):
        return SkillSwapSession.objects.filter(
            scheduled_date__lt=timezone.now()
        ).filter(
            teacher=self.request.user
        ) | SkillSwapSession.objects.filter(
            scheduled_date__lt=timezone.now()
        ).filter(
            learner=self.request.user
        )


class SessionDetailView(LoginRequiredMixin, DetailView):
    model = SkillSwapSession
    template_name = 'skill_sessions/session_detail.html'
    context_object_name = 'session'
    
    def get_queryset(self):
        return SkillSwapSession.objects.filter(
            teacher=self.request.user
        ) | SkillSwapSession.objects.filter(
            learner=self.request.user
        )


class SessionUpdateView(LoginRequiredMixin, UpdateView):
    model = SkillSwapSession
    form_class = SessionScheduleForm
    template_name = 'skill_sessions/session_form.html'
    success_url = reverse_lazy('skill_sessions:session_list')
    
    def get_queryset(self):
        return SkillSwapSession.objects.filter(
            teacher=self.request.user
        ) | SkillSwapSession.objects.filter(
            learner=self.request.user
        )


@login_required
def cancel_session(request, pk):
    session = get_object_or_404(SkillSwapSession, pk=pk)
    session.status = 'cancelled'
    session.save()
    return redirect('skill_sessions:session_list')


@login_required
def start_session(request, pk):
    session = get_object_or_404(SkillSwapSession, pk=pk)
    session.status = 'in_progress'
    session.started_at = timezone.now()
    session.save()
    return redirect('skill_sessions:session_detail', pk=pk)


@login_required
def end_session(request, pk):
    session = get_object_or_404(SkillSwapSession, pk=pk)
    session.status = 'completed'
    session.ended_at = timezone.now()
    session.save()
    return redirect('skill_sessions:session_detail', pk=pk)


class SessionReviewCreateView(LoginRequiredMixin, CreateView):
    model = SessionReview
    form_class = SessionReviewForm
    template_name = 'skill_sessions/review_form.html'
    success_url = reverse_lazy('skill_sessions:session_list')
    
    def form_valid(self, form):
        session = get_object_or_404(SkillSwapSession, pk=self.kwargs['session_id'])
        form.instance.session = session
        form.instance.reviewer = self.request.user
        if self.request.user == session.teacher:
            form.instance.reviewee = session.learner
        else:
            form.instance.reviewee = session.teacher
        return super().form_valid(form)


class SessionReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = SessionReview
    form_class = SessionReviewForm
    template_name = 'skill_sessions/review_form.html'
    success_url = reverse_lazy('skill_sessions:review_list')
    
    def get_queryset(self):
        return SessionReview.objects.filter(reviewer=self.request.user)


class ReviewListView(LoginRequiredMixin, ListView):
    model = SessionReview
    template_name = 'skill_sessions/review_list.html'
    context_object_name = 'reviews'
    
    def get_queryset(self):
        return SessionReview.objects.filter(
            reviewer=self.request.user
        ) | SessionReview.objects.filter(
            reviewee=self.request.user
        )


class CalendarView(LoginRequiredMixin, ListView):
    model = SkillSwapSession
    template_name = 'skill_sessions/calendar.html'
    context_object_name = 'sessions'
    
    def get_queryset(self):
        return SkillSwapSession.objects.filter(
            teacher=self.request.user
        ) | SkillSwapSession.objects.filter(
            learner=self.request.user
        )


class ScheduleSessionView(LoginRequiredMixin, CreateView):
    model = SkillSwapSession
    form_class = SessionScheduleForm
    template_name = 'skill_sessions/schedule_session.html'
    success_url = reverse_lazy('skill_sessions:session_list')
    
    def form_valid(self, form):
        request_obj = get_object_or_404(SkillSwapRequest, pk=self.kwargs['request_id'])
        form.instance.request = request_obj
        form.instance.teacher = request_obj.recipient
        form.instance.learner = request_obj.requester
        form.instance.skill = request_obj.offered_skill.skill
        return super().form_valid(form)
