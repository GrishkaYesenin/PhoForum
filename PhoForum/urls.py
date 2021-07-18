import debug_toolbar
from django.contrib import admin
from django.urls import path, include
# from forum.views import pageNotFound

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', include('django.contrib.auth.urls')),
    path('account/', include('account.urls')),
    path('', include('forum.urls')),

]


from django.conf import settings
from django.conf.urls.static import static


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# handler404 = pageNotFound