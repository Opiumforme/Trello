import sys
import requests

base_url = "https://api.trello.com/1/{}"
auth_params = {
    'key': "cd6d319567777c21320670799123bb1c",
    'token': "1fa8931c9b33dfbc9fe5f450bf4926d8067444aaf31addc2845ba04285d0d1dc"}
board_id = "LcWtIk5N"


def read():
    # Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:
    for column in column_data:
        # Получим данные всех задач в колонке и перечислим все названия
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print("{0} (количество задач {1})".format(column['name'], len(task_data)))
        if not task_data:
            print('\t' + 'Нет задач!')
            continue
        for task in task_data:
            print('\t' + task['name'])


def create(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна
    found = False
    column_id = ''
    for column in column_data:
        if column['name'] == column_name:
            task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards',
                                     params=auth_params).json()
            column_id = column['id']
            for task in task_data:
                if task['name'] == name:
                    print('Задача не создана! Найдена существующая задача с таким именем!')
                    found = True
                    break

    if not found:
        # создаем, если не нашли совпадений
        requests.post(base_url.format('cards'), data={'name': name, 'idList': column_id, **auth_params})


def create_list(name):
    # Получим данные всех колонок на доске
    lists_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    for column in lists_data:
        if column['name'] == name:
            # если нашли - не создаем
            print('Уже существует колонка с таким именем!')
            return

    res = requests.post(base_url.format('boards') + '/' + board_id + '/lists', params={'name': name, **auth_params})
    if res.status_code == 200:
        print('Колонка создана')
    else:
        print('Ошибка № {0}'.format(res.status_code))


def move(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Среди всех колонок нужно найти задачу по имени и получить её id
    task_array = []
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                task_array.append({'task_id': task['id'], 'column_name': column['name']})

    if len(task_array) == 0:
        print('Не найдено ни одной задачи с таким именем')
        return

    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу
    column_id = None
    for column in column_data:
        if column['name'] == column_name:
            column_id = column['id']
            break

    if not column_id:
        print('Не найдена колонка для перемещения!')

    if len(task_array) == 1:
        move_task(task_array[0]['task_id'], column_id)
    else:
        for i, task in enumerate(task_array):
            x = i + 1
            print('{0}. Колонка: {1}, ID задачи: {2}'.format(x, task['column_name'], task['task_id']))
        i = int(input('Найдено больше одной задачи! Выберете номер задачи для перемещения: '))
        i = i - 1
        if 0 <= i < len(task_array):
            move_task(task_array[i]['task_id'], column_id)
        else:
            print('Введен некорректный номер задачи!')


def move_task(task_id, column_id):
    res = requests.put(base_url.format('cards') + '/' + task_id + '/idList',
                 data={'value': column_id, **auth_params})
    if res.status_code == 200:
        print('Задача перемещена')
    else:
        print('Ошибка № {0}'.format(res.status_code))


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'create_list':
        create_list(sys.argv[2])


