import json
from datetime import datetime
import os

def mask_card_number(card_number):
    """Замаскировать номер карты."""
    return f"{card_number[:6]} {card_number[6:10]} ** **** {card_number[-4:]}"

def mask_account_number(account_number):
    """Замаскировать номер счета."""
    return f"**{account_number[-4:]}"

def format_operation(operation):
    """Форматировать одну операцию для вывода."""
    date = datetime.fromisoformat(operation['date']).strftime('%d.%m.%Y')
    description = operation['description']

    # Получаем информацию о сумме и валюте
    amount = float(operation['operationAmount']['amount'])  # Преобразуем в float
    currency = operation['operationAmount']['currency']['name']

    # Получаем информацию о карте или счете
    from_account = operation.get('from', 'Счет не указан')
    to_account = operation.get('to', 'Счет не указан')

    # Замаскируем номера
    if 'card' in from_account:
        from_account = mask_card_number(from_account.split()[-1])
    else:
        from_account = mask_account_number(from_account.split()[-1])

    if 'Счет' in to_account:
        to_account = mask_account_number(to_account.split()[-1])
    else:
        to_account = mask_card_number(to_account.split()[-1])

    return f"{date} {description}\n{from_account} -  {to_account}\n{amount:.2f} {currency}"

def print_last_operations(operations_json):
    """Выводит последние 5 выполненных операций."""
    operations = json.loads(operations_json)

    # Фильтруем только выполненные операции
    executed_operations = [op for op in operations if op.get('state') == 'EXECUTED']

    # Сортируем по дате (последние операции первыми)
    executed_operations.sort(key=lambda x: x['date'], reverse=True)

    # Берем последние 5 операций
    last_operations = executed_operations[:5]

    # Форматируем и выводим каждую операцию
    for i, operation in enumerate(last_operations):
        print(format_operation(operation))
        if i < len(last_operations) - 1:
            print()  # Пустая строка между операциями


file_path = os.path.join(os.getcwd(), 'operations.json')
with open(file_path, 'r') as file:
    data = json.load(file)

# Вызов функции для вывода последних операций
print_last_operations(json.dumps(data))
