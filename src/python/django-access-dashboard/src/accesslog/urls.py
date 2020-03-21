from django.conf.urls import patterns, url, include

from accesslog.views import (
    AccessLogViewSet,
    SourceViewSet,
    DayViewSet,
    MonthViewSet
)

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'log', AccessLogViewSet)
router.register(r'source', SourceViewSet)
router.register(r'stats/daily', DayViewSet)
router.register(r'stats/monthly', MonthViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
)
