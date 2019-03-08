from shared.serializers import PaginatedResponseDto, SuccessResponseDto


class TodoListResponseDto(PaginatedResponseDto):
    def __init__(self, paginator, page_number, base_path):
        page = paginator.get_page(page_number)
        self.todos = [TodoDto(todo, include_details=False).get_data() for todo in page.object_list.all()]
        super(TodoListResponseDto, self).__init__(len(self.todos), paginator, page_number, base_path)


    def get_data(self):
        return {
            'success': True,
            'page_meta': self.page_meta,
            'todos': self.todos
        }


class TodoDto:
    def __init__(self, todo, include_details=False):
        self.id = todo.id
        self.title = todo.title
        self.completed = todo.completed
        self.created_at = str(todo.created_at)
        self.updated_at = str(todo.updated_at)
        self.include_details = include_details
        if include_details:
            self.description = todo.description

    def get_data(self):
        data = {
            'id': self.id,
            'title': self.title,
            'completed': self.completed,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        if self.include_details:
            data['description'] = self.description

        return data


class TodoDetailsResponseDto(SuccessResponseDto):

    def __init__(self, todo, messages=None):
        super(TodoDetailsResponseDto, self).__init__(messages)
        self.todo = TodoDto(todo, include_details=True).get_data()

    def get_data(self):
        data = super(TodoDetailsResponseDto, self).get_data()
        data.update(self.todo)
        return data
