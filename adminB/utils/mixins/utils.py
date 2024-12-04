import re

from django.forms import ValidationError

def is_valid_username(username: str):
    """
    Validates the provided username against specific criteria.
    
    Args:
        username (str): The username to validate.
    
    Raises:
        ValidationError: If the username is invalid based on the defined rules.
    
    Returns:
        None: The function raises an exception if the username is invalid.
    """
    if len(username) < 3 or len(username) > 30:
        raise ValidationError('Username must be between 3 and 30 characters long.')
    
    if not re.match(r'^[\w.]+$', username):
        raise ValidationError('Username can only contain letters, numbers, ".", and "_".')
    
    if username[0] in ['.', '_']:
        raise ValidationError('Username cannot start with "." or "_".')
    
    return None

def logger(topic: str = None) -> list:
    """
    Логгер, возвращающий сообщения об ошибках для заданной темы.

    Parameters:
        limitLogger (int): Ограничение на количество записей лога.
        topic (str): Категория, для которой нужны сообщения лога.

    Returns:
        list: Список сообщений, связанных с заданной темой.

    Raises:
        ValueError: Если limitLogger <= 0 или тема не найдена.
    """
    
    loggers = {
        'search': [
            'No results found for the search query',  # Когда поиск не дал результатов
            'Search query is too short',             # Когда запрос слишком короткий
            'Search service is currently unavailable'  # Когда поиск временно недоступен
        ],
        'authentication': [
            'Invalid username or password',          # Когда данные для входа неверны
            'Account is locked due to multiple failed login attempts',  # Блокировка из-за неудачных попыток
            'User account is inactive',              # Пользователь заблокирован
            'Session has expired'                    # Истек срок действия сессии
        ],
        'database': [
            'Database connection lost',              # Потеря соединения с БД
            'Failed to fetch data',                  # Не удалось получить данные
            'Data write failed'                      # Ошибка записи данных
        ],
        'file_upload': [
            'File type not supported',               # Тип файла не поддерживается
            'File size exceeds the limit',           # Превышен размер файла
            'File upload interrupted'                # Прерывание загрузки файла
        ],
        'payment': [
            'Payment gateway not responding',        # Проблема с платёжной системой
            'Payment declined by the bank',          # Отклонение платежа банком
            'Insufficient funds'                     # Недостаточно средств
        ]
    }
    
    if topic not in loggers:
        raise ValueError("Invalid topic provided")

    return loggers[topic]
    

def form_valid(form = None, time_save_return = False):
    """
    Validates the form and saves it conditionally.
    
    Parameters:
        form: The form to be validated.
        time_save_return (bool): If True, returns an unsaved instance of the form model.
                                 If False, returns the form object (usually for further processing).
    
    Returns:
        An unsaved instance of the model (if time_save_return is True and the form is valid),
        or the form object (if time_save_return is False and the form is valid).
        None if the form is invalid.
    
    Raises:
        ValueError: If the form argument is None.
    """
    
    if form is None:
        return None
    
    if form.is_valid():
        if time_save_return:
            return form.save(commit=False)
        return form

    return None
    