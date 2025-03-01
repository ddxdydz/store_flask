from wtforms.validators import ValidationError

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB


class FileSizeValidator:
    def __init__(self, max_size=MAX_FILE_SIZE):
        self.max_size = max_size

    def __call__(self, form, field):
        if field.data:
            file = field.data
            if file.content_length > self.max_size:
                raise ValidationError(f'Размер файла не должен превышать {self.max_size / (1024 * 1024)} МБ.')
