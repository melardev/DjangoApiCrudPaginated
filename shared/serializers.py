class PaginatedResponseDto:
    def __init__(self, current_items_count, paginator, page_number, base_path):
        page = paginator.get_page(page_number)
        self.page_meta = {'total_items_count': paginator.count, 'current_items_count': current_items_count,
                          'offset': page.start_index() - 1,
                          'requested_page_size': paginator.per_page, 'current_page_number': page_number,
                          'prev_page_number': 1, 'number_of_pages': paginator.num_pages,
                          'has_prev_page': page.has_previous(), 'has_next_page': page.has_next()}

        if page.has_next():
            self.page_meta['next_page_number'] = page.next_page_number()
        else:
            self.page_meta['next_page_number'] = 1

        if page.has_previous():
            self.page_meta['prev_page_number'] = page.previous_page_number()
        else:
            self.page_meta['prev_page_number'] = 1

        self.page_meta['next_page_url'] = '%s?page=%d&page_size=%d' % (
            base_path, self.page_meta['next_page_number'], self.page_meta['requested_page_size'])
        self.page_meta['prev_page_url'] = '%s?page=%d&page_size=%d' % (
            base_path, self.page_meta['prev_page_number'], self.page_meta['requested_page_size'])


class AppResponseDto:
    def __init__(self, success, messages):
        self.success = success
        if type(messages) == list:
            self.full_messages = messages
        elif type(messages) == str:
            self.full_messages = [messages]
        else:
            self.full_messages = []

    def get_data(self):
        return {
            'success': self.success,
            'full_messages': self.full_messages
        }


class ErrorResponseDto(AppResponseDto):
    def __init__(self, messages):
        super(ErrorResponseDto, self).__init__(False, messages)


class SuccessResponseDto(AppResponseDto):
    def __init__(self, messages=None):
        super(SuccessResponseDto, self).__init__(True, messages)
