import sys
import pytest
import os
import json
from datetime import datetime
from main import mask_card_number, mask_account_number, format_operation

# Добавляем путь к папке src в системный путь
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Путь к файлу
file_path = os.path.join(os.path.dirname(__file__), 'operations.json')

if not os.path.exists(file_path):
    raise FileNotFoundError(f"Файл не найден: {file_path}")

# Открываем файл и загружаем данные
with open(file_path, 'r') as file:
    operations_data = json.load(file)

def test_mask_card_number():
    result = mask_card_number("1234567890123456")
    expected = "123456 7890  ** 3456"

    # Печатаем результаты для отладки
    print(f"Result: {repr(result)}")
    print(f"Expected: {repr(expected)}")

    # Сравниваем с удалением лишних пробелов
    assert result.strip() == expected.strip()

def test_mask_account_number():
    assert mask_account_number("4081781009999999") == "**9999"
    assert mask_account_number("4070281000000000") == "**0000"
    assert mask_account_number("4081781000000000") == "**0000"

def test_format_operation():
    for operation in operations_data:
        expected_output = (
            f"{datetime.fromisoformat(operation['date']).strftime('%d.%m.%Y')} {operation['description']}\n"
            f"{mask_account_number(operation['from'].split()[-1])} - "
            f"{mask_account_number(operation['to'].split()[-1])}\n"
            f"{operation['operationAmount']['amount']} {operation['operationAmount']['currency']['name']}"
        )
        assert format_operation(operation) == expected_output

if __name__ == "__main__":
    pytest.main()
