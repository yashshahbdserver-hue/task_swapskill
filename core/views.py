from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    return render(request, "core/home.html")

class HomeView:
    @classmethod
    def as_view(cls):
        return home

class DashboardView:
    @classmethod
    def as_view(cls):
        return lambda r: render(r, "core/dashboard.html")

class BrowseUsersView:
    @classmethod
    def as_view(cls):
        return lambda r: render(r, "core/browse_users.html")

class UserProfileView:
    @classmethod
    def as_view(cls):
        return lambda r, user_id: render(r, "core/user_profile.html")

class SearchView:
    @classmethod
    def as_view(cls):
        return lambda r: render(r, "core/search.html")

class NotificationListView:
    @classmethod
    def as_view(cls):
        return lambda r: render(r, "core/notifications.html")

def mark_notification_read(request, notification_id):
    return JsonResponse({"status": "success"})

def mark_all_notifications_read(request):
    return JsonResponse({"status": "success"})
