import debug_toolbar
from django.contrib import admin
from django.urls import path, include
# from mainapp.views import pageNotFound

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')),
    # path('account/', include('mainapp.account.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', include('django.contrib.auth.urls')),
]


from django.conf import settings
from django.conf.urls.static import static


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# handler404 = pageNotFound