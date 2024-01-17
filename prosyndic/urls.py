"""
URL configuration for prosyndic project.

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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('copro.urls')),
    path('copro/', include('copro.urls')),
    path('home/', include('copro.urls')),
    path('simu/', include('simulator.urls')),
    path('cart/', include('cartcom.urls')),
    path("polls/", include("polls.urls")),
    path('markdownx/', include('markdownx.urls')), # MarkdownX URL patterns
    path("doc/", include("drivedoc.urls")),
    
]

# ... the rest of your URLconf goes here ...
## add static 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
## add static 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# add debug_toolbar 
if settings.DEBUG :
    import debug_toolbar
    urlpatterns += path('__debug__', include(debug_toolbar.urls) ),

    