from django.conf.urls import url

from todos.views import get_or_delete_all, get_completed, get_pending, read_or_write_by_id

app_name = 'todos'
urlpatterns = [
    url(r'completed/?$', get_completed, name='get_completed'),
    url(r'pending/?$', get_pending, name='get_pending'),
    url(r'(?P<id>([0-9])+)$', read_or_write_by_id, name='by_id'),
    url(r'/?$', get_or_delete_all, name='get_all'),
]
