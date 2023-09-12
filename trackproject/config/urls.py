"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.urls import include

from blog.urls import router as blog_router
from blog import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", views.UserListView.as_view()),
    path("blog/", include(blog_router.urls)),
    path("follow/", views.FollowViewSet.as_view({"post": "create"})),
    path(
        "follow/unfollow/<str:username>/",
        views.FollowViewSet.as_view({"delete": "destroy"}),
    ),
    path("follow/follower/", views.FollowViewSet.as_view({"get": "follower"})),
    path("follow/following/", views.FollowViewSet.as_view({"get": "following"})),
    path("api-auth", include("rest_framework.urls")),
    # drf-spectacular
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-swagger-ui",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
