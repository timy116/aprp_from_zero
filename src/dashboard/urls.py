from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

from dashboard.views import Index

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('apps.accounts.urls', namespace='accounts')),
]

urlpatterns += i18n_patterns(
    url(r'^$', Index.as_view(), name='index'),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
