# Тестирование
## Задания:

### 2 КТ
CSV Файл:
    - Создайте новый CSV файл на основе данных из файла "grades.csv".
    - Объедините данные "Имя" и "Фамилия" в одно поле.
    - Исключите все отрицательные значения.
    - Вычтите средний балл каждого человека из его оценок.
JSON Файл:
    - Преобразуйте JSON файл в словарь.
    - Добавьте информацию о двух новых членах команды.
    - Отсортируйте членов команды по количеству их способностей.
    - Создайте дополнительный JSON файл с информацией о другой команде.
    - Сравните средний возраст и количество способностей членов двух команд в числовой форме.

### 3 КТ
1.	Тестируемый API - https://petstore.swagger.io/
2.	Репозиторий с примерами API – https://github.com/sadboy2001/api_testing.git
3.	Перейти в папку api_testing и файл base_request
4.	Посмотреть на реализацию класса для работы с api
5.	Создать свои запросы для сущностей тестируемого API (по 4 запроса) user и store по базовому url с реализацией базового класса тестирования(пример приведен в репозитории)

### 4 КТ
1. Составить MindMap по предложенным API (https://dog.ceo/dog-api/).
2. Написать 5 тестов к каждой сущности для наибольшего покрытия сущностей.
3. Прислать отчет о проведенном тестировании.

Использовать: pytest, httpx, allure, jsonschema, pydantic