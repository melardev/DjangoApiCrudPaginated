import json

from django.core.paginator import Paginator
from django.http import HttpResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from shared.serializers import ErrorResponseDto, SuccessResponseDto
from todos.models import Todo
from todos.serializers import TodoListResponseDto, TodoDetailsResponseDto


@csrf_exempt
def get_or_delete_all(request, *args, **kwargs):
    if request.method == 'GET':
        return get_page_json(request)
    elif request.method == 'DELETE':
        Todo.objects.all().delete()
        return get_response(SuccessResponseDto('All todos successfully').get_data())
    elif request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        description = data.get('description', '')
        completed = data.get('completed', False)

        # todo = Todo.objects.create(title=title, description=description, completed=completed)
        # or
        todo = Todo.objects.create(**data)
        return get_response(TodoDetailsResponseDto(todo).get_data())


def get_completed(request, *args, **kwargs):
    return get_page_json(request, completed=True)


def get_pending(request, *args, **kwargs):
    return get_page_json(request, completed=False)


def read_or_write_by_id(request, *args, **kwargs):
    try:
        todo = Todo.objects.get(pk=kwargs['id'])
        if request.method == 'GET':

            dto = TodoDetailsResponseDto(todo).get_data()
            return get_response(dto)

        elif request.method == 'PUT':
            data = json.loads(request.body)
            todo.title = data.get('title')
            description = data.get('description', None)

            if description is not None:
                todo.description = description

            todo.completed = data.get('completed', False)
            todo.save()
            return get_response(TodoDetailsResponseDto(todo).get_data())
        elif request.method == 'DELETE':
            todo.delete()
            return get_response(SuccessResponseDto('Todo deleted successfully').get_data())

    except Todo.DoesNotExist:
        return get_response(ErrorResponseDto('Todo not found').get_data())


def get_pagination_params(request):
    page_size = int(request.GET.get('page_size', 5))
    if page_size < 0 or page_size > 20:
        page_size = 5

    page = int(request.GET.get('page', 1))
    if page < 0:
        page = 1
    offset = (page - 1) * page_size
    return page, page_size


def get_page_json(request, completed=None):
    queryset = Todo.objects
    if completed is True or completed is False:
        queryset = queryset.filter(completed=completed)

    page_number, page_size = get_pagination_params(request)
    todos = queryset.order_by('-created_at').only('id', 'title', 'created_at', 'updated_at').all()
    paginator = Paginator(todos, page_size)
    dto = TodoListResponseDto(paginator, page_number, request.path)
    return HttpResponse(json.dumps(dto.get_data()), content_type='application/json')


def get_response(dto):
    return HttpResponse(json.dumps(dto), content_type='application/json')
