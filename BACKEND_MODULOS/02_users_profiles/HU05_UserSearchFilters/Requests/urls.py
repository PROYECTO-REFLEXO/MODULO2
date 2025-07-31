from django.urls import path
from HU05_UserSearchFilters.views.search_controller import search_users_view

urlpatterns = [
    path('search/', search_users_view, name='search_users'),
    path('', search_users_view),  # ← opcional: para GET /api/users
]
