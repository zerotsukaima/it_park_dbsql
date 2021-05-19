import sqlite3

def id_of():
    file = open('id.txt', 'r')
    id_txt = file.read()
    file.close()
    id = int(id_txt)
    return id

def id_in(id):
    id += 1
    id_str = str(id)
    file = open('id.txt', 'w')
    file.write(id_str)
    file.close()

def hello():
    print('\nДобро пожаловать в программу по работе с таблицами на базе sqlite3.\n'
          'Пожалуйста, выберите действие:\n')
    start()

def start():
    step = input('1 - войти в систему.\n'
                 '2 - зарегистрироваться.\n')
    if step == '1':
        login()
    elif step == '2':
        print('Регистрация в системе.\n'
              'Для выхода в главное меню введите: 0.\n')
        user_add()
    else:
        print('\nПожалуйста, выберите одно из действие:\n\n')
        start()

def login():
    print('\nВход в систему.\nДля выхода в главное меню введите: 0.\n')
    flag = 1
    user = input('Введите Ваш логин:\n')
    if user == '0':
        start()
    else:
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        for row in cursor.execute('SELECT user, password from users'):
            if row[0] == user:
                flag = 0
                check_pas(row[1], user)
        conn.close()
        if flag == 1:
            not_user(user)

def check_pas(pas, user):
    password = input('\nВведите пароль:\n')
    if pas == password:
        print(f'\n{user}, Вы вошли в систему.\n')
        in_system(user)
    else:
        print('\nНеверный пароль!')
        step = input('Выберите дальнейшее действие:\n'
                     '1 - повторить ввод пароля.\n'
                     '2 - выход в главное меню.\n')
        if step == '1':
            check_pas(pas, user)
        elif step == '2':
            start()
        else:
            print('\nНекорректный ввод.\n')
            start()

def not_user(user):
    print(f'\nПользватель с логином {user} не найден.\nВозможно, Вы ошиблись '
          f'при вводе данных либо Вы еще не зарегистрированы.\n')
    step = input('Выберите дальнейшее действие:\n'
                 '1 - повторить ввод логина.\n'
                 '2 - перейти к регистрации.\n'
                 '3 - выход в главное меню.\n')
    if step == '1':
        login()
    elif step == '2':
        user_add()
    elif step == '3':
        start()
    else:
        print('\nНекорректный ввод.\n')
        start()

def user_add():
    user = input('\nПридумайте логин (не менее 3-х символов):\n')
    if len(user) >= 3:
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        for row in cursor.execute('SELECT user from users'):
            if row[0] == user:
                print(f'\nЛогин {user} уже знаят.\n')
                user_add()
        conn.close()
        password(user)
    elif user == '0':
        start()
    else:
        user_add()

def password(user):
    password = input('\nПридумайте пароль:\n')
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    id = id_of()
    q = f"INSERT INTO users (id, user, password) VALUES ('{id}', '{user}', '{password}')"
    id_in(id)
    cursor.execute(q)
    conn.commit()
    conn.close()
    print(f'{user}, Вы успешно зарегистрированы.')
    in_system(user)

def in_system(user):
    step = input(f'\nМеню пользователя.\n{user}, Выберите действие:\n\n'
                 '1 - создать новую таблицу.\n'
                 '2 - выбрать таблицу для работы.\n'
                 '3 - выйти из системы.\n')
    if step == '1':
        table_add(user)
    elif step == '2':
        table_show(user)
    elif step == '3':
        print('\nПожалуйста, выберите действие:\n')
        start()
    else:
        print('\nНекорректный ввод.\n')
        in_system(user)

def table_add(user):
    table = input('\nПридумайте название таблицы: (не менее 3 символов):\n')
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    if len(table) >= 3:
        for row in cursor.execute('SELECT name_tab from tables'):
            for i in row:
                if i == table:
                    print(f'\nТаблица с именем {table} уже существует.\n')
                    table_add(user)
        id = id_of()
        q = f"INSERT INTO tables (id, name_tab, owner) VALUES ('{id}', '{table}', '{user}')"
        cursor.execute(f"CREATE TABLE '{table}' (id INT PRIMARY KEY NOT NULL);")
        print('\nТаблица успешна создана!\n'
              f'ID-номер таблицы: {id}\n'
              f'Название таблицы: {table}\n'
              f'Владелец таблицы: {user}\n')
        id_in(id)
        cursor.execute(q)
        conn.commit()
        conn.close()
        step = input('1 - добавить столбцы в таблицу.\n'
                     '2 - перейти в меню пользователя.\n')
        if step == '1':
            add_column(user, table)
        elif step == '2':
            in_system(user)
        else:
            in_system(user)

def table_show(user):
    full = []
    read = []
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    for row in cursor.execute(f"SELECT * from tables"):
        if row[2] != None:
            owner = row[2].split(', ')
            for i in owner:
                if i == user:
                    full.append(row[1])
    for row in cursor.execute(f"SELECT * from tables"):
        if row[3] != None:
            users = row[3].split(', ')
            for i in users:
                if i == user:
                    read.append(row[1])
    conn.close()
    if len(full) >= 1:
        count = 0
        print('\nВаши таблицы с полным доступом:\n')
        for i in full:
            count += 1
            print(f'{count} таблица: {i}.\n')
    if len(read) >= 1:
        count = 0
        print('\nВаши таблицы с доступом только для чтения: \n')
        for i in read:
            count += 1
            print(f'{count} таблица: {i}.\n')
    select_table(user, full, read)
    if len(full) == 0 == len(read):
        print('У Вас нет доступных таблиц.')
        in_system(user)

def select_table(user, full, read):
    flag = 0
    table = input('Для выхода в меню пользователя введите: 0\n\n'
                  'Введите название таблицы, с которой хитите поработать:\n')
    if table == '0':
        in_system(user)
    else:
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        for row in cursor.execute('SELECT name_tab from tables'):
            for i in row:
                if table == i:
                    flag = 2
                    for i in full:
                        if i == table:
                            flag = 2
                            edit_table(user, table)
                    for i in read:
                        if i == table:
                            flag = 2
                            show_data(user, table)
        conn.close()
        if flag == 0:
            print(f'Таблица {table} не найдена.\nПожалуйста, проверьте корректность '
                  f'введенных данных и повторите ввод.\n')
            select_table(user, full, read)
        if flag == 2:
            print(f'У Вас нет доступа к таблице {table}.\n')
            select_table(user, full, read)

def edit_table(user, table):
    print(f'{user}, Ваша таблица {table} готова к работе.\n')
    step = input('Выберите действие:\n'
                 '1 - работать с данными таблицы.\n'
                 '2 - добавить столбцы в таблицу.\n'
                 '3 - настроить доступ к таблице.\n'
                 '4 - выход в меню пользователя.\n')
    if step == '1':
        data(user, table)
    elif step == '2':
        add_column(user, table)
    elif step == '3':
        access(user, table)
    elif step == '4':
        in_system(user)
    else:
        print('Пожалуйста, проверьте корректность введенных данны '
              'и повторите ввод либо введите 0 для выхода в меню.')
        edit_table(user, table)

def data(user, table):
    step = input(f'Выберите действие с данными таблицы {table}:\n'
                 '1 - вывод данных.\n'
                 '2 - добавление данных.\n'
                 '3 - удаление данных.\n'
                 '4 - замена данных.\n'
                 '5 - выход в меню пользователя.\n')
    if step == '1':
        show_data(user, table)
    elif step == '2':
        add_data(user, table)
    elif step == '3':
        delete_data(user, table)
    elif step == '4':
        replace_data(user, table)
    elif step == '5':
        in_system(user)
    else:
        print('Пожалуйста, проверьте корректность введенных данны '
              'и повторите ввод либо введите 0 для выхода в меню.')
        data(user, table)

def show_data(user, table):
    step = input('\nВыберите действие:\n'
                 '1 - показать все данные из таблицы.\n'
                 '2 - показать данные выборочно по столбцам.\n')
    if step == '1':
        all_data(user, table)
    elif step == '2':
        sel_column(user, table)
    if step == '0':
        in_system(user)
    else:
        print('Пожалуйста, проверьте корректность введенных данны '
              'и повторите ввод либо введите 0 для выхода в меню.')
        show_data(user, table)

def all_data(user, table):
    print(f'Все данные таблицы {table}\n')
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info('{table}')")
    col = cursor.fetchall()
    for i in col:
        print(i[1], end=' ')
    print('')
    for i in col:
        print(i[2], end=' ')
    print('\n')
    conn.close()
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM '{table}'")
    rows = cursor.fetchall()
    for row in rows:
        print(*row)
    conn.close()
    data(user, table)

def sel_column(user, table):
    flag = 0
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info('{table}')")
    col = cursor.fetchall()
    print(f'Столбцы таблицы {table}:\n')
    for i in col[1::]:
        print(i[1])
    column = input('\nВведите название столбца для вывода данных:\n')
    if column == '0':
        in_system(user)
    else:
        for i in col[1::]:
            if i[1] == column:
                show_column(user, table, column)
                flag = 1
        if flag == 0:
            print(f'Столбец с названием {column} в таблице {table} не найден.\n')
            sel_column(user, table)
    conn.close()

def show_column(user, table, column):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    print(f'Данные по столбцу {column} таблицы {table}:\n')
    for row in cursor.execute(f"SELECT {column} FROM {table}"):
        print('---------')
        print(*row)
    conn.close()
    step = input('\nВыберите дальнейшее действие с таблицей:\n'
                 f'1 - продолжить работу с таблицей {table}.\n'
                 '2 - выход в меню пользователя.\n')
    if step == '1':
        edit_table(user, table)
    elif step == '2':
        in_system(user)
    else:
        print('Пожалуйста, проверьте корректность введенных данных.')
        show_column(user, table, column)

def add_data(user, table):
    flag = 0
    columns = []
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info('{table}')")
    col = cursor.fetchall()
    print(f'Столбцы таблицы {table}:\n')
    for i in col[1::]:
        columns.append(i[1])
        print(i[1])
    column = input('\nДля выхода в меню пользователя введите: 0\n\n'
                   'Введите название столбца для записи данных:\n')
    cursor.close()
    if column == '0':
        in_system(user)
    else:
        for i in columns:
            if i == column:
                flag = 1
                conn = sqlite3.connect('db.sqlite')
                cursor = conn.cursor()
                data = input('Введите данные:\n')
                id = id_of()
                q = f"INSERT INTO '{table}' (id, '{column}') VALUES ('{id}', '{data}')"
                cursor.execute(q)
                conn.commit()
                cursor.close()
                id_in(id)
                print(f'Данные {data} в столбец {column} таблицы {table} добавлены.\n')
                step = input('Выберите дальнейшее действие с таблицей:\n'
                             f'1 - продолжить работу с таблицей {table}.\n'
                             '2 - выход в меню пользователя.\n')
                if step == '1':
                    edit_table(user, table)
                elif step == '2':
                    in_system(user)
                else:
                    print('Пожалуйста, проверьте корректность введенных данных.')
                    add_data(user, table)
        if flag == 0:
            print(f'Cтолбец {column} в таблице {table} не найден.\n')
            add_data(user, table)

def delete_data(user, table):
    flag = 0
    columns = []
    d = []
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info('{table}')")
    col = cursor.fetchall()
    print(f'Столбцы таблицы {table}:\n')
    for i in col[1::]:
        columns.append(i[1])
        print(i[1])
    column = input('\nВведите название столбца, в котором хранятся данные для удаления: \n')
    if column == '0':
        in_system(user)
    else:
        for i in columns:
            if i == column:
                flag = 1
                for row in cursor.execute(f"SELECT {column} from {table}"):
                    d.append(*row)
                print(f'Данные столбца {column}:\n')
                for i in d:
                    print(i)
                data = input('\nВведите данные, которые хотите удалить:\n')
                for i in d:
                    print(i)
                    if str(i) == data:
                        flag = 2
                        conn.execute(f"DELETE from {table} where {column} = '{data}'")
                        conn.commit()
                        print(f'Информаця {data} из столбца {column} таблицы {table} удалена.')
                        in_system(user)
    if flag == 1:
        print(f'Информация {data} в столбце {column} не найдена.'
              'Повторите ввод либо введите 0 для выхода в меню пользователя.')
        delete_data(user, table)
    if flag == 0:
        print(f'Столбец {column} в таблице {table} не найдена.'
              'Повторите ввод либо введите 0 для выхода в меню пользователя.')
        delete_data(user, table)

def replace_data(user, table):
    columns = []
    id = []
    d = []
    flag = 0
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info('{table}')")
    col = cursor.fetchall()
    print(f'Столбцы таблицы {table}:\n')
    for i in col[1::]:
        columns.append(i[1])
        print(i[1])
    column = input('\nВведите название столбца, в котором хранятся данные для замены: \n')
    if column == '0':
        in_system(user)
    else:
        for i in columns:
            if i == column:
                flag = 1
                for row in cursor.execute(f"SELECT id, {column} from {table}"):
                    id.append(row[0])
                    d.append(row[1])
                print(f'\nДанные по столбцу {column}:')
                for i in d:
                    print(i)
                data = input('\nВведите данные, которые хотите заменить:\n')
                for i in d:
                    if i == data:
                        flag = 2
                        ind = d.index(i)
                        swap = input('Введите новые данные:\n')
                        conn.execute(f"UPDATE {table} set {column} = '{swap}' where id = {id[ind]}")
                        print(f'Информаця {data} столбца {column} таблицы {table} заменена на {swap}.')
                        conn.commit()
                        conn.close()
                        in_system(user)
    if flag == 1:
        print(f'Информация {data} в столбце {column} не найдена.'
              'Повторите ввод либо введите 0 для выхода в меню пользователя.')
        replace_data(user, table)
    if flag == 0:
        print(f'Столбец {column} в таблице {table} не найдена.'
              'Повторите ввод либо введите 0 для выхода в меню пользователя.')
        replace_data(user, table)

def add_column(user, table):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    count = 0
    try:
        column_count = int(input('Введите количество столбцов: '))
        while column_count > 0:
            count += 1
            column_name = input(f'Введите название {count} столбца:\n')
            column_type = input(f'Выберите тип столбца {column_name}:\n'
                                    '1 - число.\n2 - текст.\n')
            if column_type == '1':
                column_type = 'INT'
            if column_type == '2':
                column_type = 'TEXT'
            cursor.execute(f"ALTER TABLE '{table}' add column '{column_name}' {column_type}")
            conn.commit()
            column_count -= 1
        cursor.close()
        print('Столбцы добавлены.')
        count = 0
        edit_table(user, table)
    except:
        print('Проверьте корректность введенных данных '
              '(Вы должны ввести число) и повторите ввод.\n')
        add_column(user, table)

def access(user, table):
    level = input(f'Выберите уровень доступа к таблице - {table}.\n'
                  '1 - только для чтения.\n'
                  '2 - полный доступ.\n')
    if level == '1':
        read_access(user, table)
    elif level == '2':
        full_access(user, table)

def full_access(user, table):
    a = []
    person = input(f'Введите имя пользователя, которому хотите '
                   f'предоставить полный доступ к таблице - {table}\n')
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    for row in cursor.execute(f"SELECT * from tables name_tab where name_tab = '{table}'"):
        a.append(row[2])
    cursor.close()
    a.append(person)
    owners = ', '.join(a)
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    conn.execute(f"UPDATE tables set owner = '{owners}' where name_tab = '{table}'")
    conn.commit()
    cursor.close()
    print(f'Пользователю {person} открыт полный доступ к таблице {table}.')
    in_system(user)

def read_access(user, table):
    a = []
    person = input(f'Введите имя пользователя, которому хотите '
                   f'предоставить доступ (для чтения) к таблице - {table}:\n')
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    for row in cursor.execute(f"SELECT * from tables name_tab where name_tab = '{table}'"):
        if row[3] != None:
            a.append(row[3])
    a.append(person)
    users = ', '.join(a)
    conn.execute(f"UPDATE tables set users = '{users}' where name_tab = '{table}'")
    conn.commit()
    cursor.close()
    print(f'Пользователю {person} открыт для чтения доступ к таблице {table}.\n')
    in_system(user)

hello()