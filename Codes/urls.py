from django.conf.urls.defaults import patterns
import handlers

urlpatterns = patterns(
    '', 
    
    (r'^notification/$',
        handlers.notification_resource,
        {},
        'notification'),
    
    )
