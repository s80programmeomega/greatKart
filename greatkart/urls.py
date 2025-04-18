"""
URL configuration for greatkart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from store import views
from django.contrib.auth import views as auth_views

from django.contrib.sitemaps.views import sitemap

from store.sitemaps import ProductSitemap

sitemaps = {
    "products": ProductSitemap,
}

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("reload/", include("django_browser_reload.urls")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("cart/", include("cart.urls")),
    path("category/", include("category.urls")),
    path("order/", include("order.urls")),
    path("store/", include("store.urls")),
    path(
        "sitemap.xml/",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
