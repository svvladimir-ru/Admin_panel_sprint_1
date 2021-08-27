from psycopg2.extensions import connection as _connection


class PostgresSaver:
    """Ужасный метод, но попробую описать.
    Принимает словарь из sqllite_loader.py со значениями из dataclasses
    проходит циклом, каждые 100 записей добавляет в postgres. Пршилось сделать дублирование кода,
    что бы добавлять последние записи.
    В postgres добавляются данные из методов, соответствующих названиям таблиц
    """
    def __init__(self, pg_conn: _connection):
        self.conn = pg_conn
        self.cursor = self.conn.cursor()
        self.counter = 0
        self.tables = ''

    def save_film_work(self, data) -> list:
        args = ','.join(self.cursor.mogrify(
            "('{}', '{}', {}, {}, {}, '{}', '{}', '{}', {}, '{}')".format(
                item.title.replace("'", '"'),
                str(item.description).replace("'", '"') if item.description else 'null',
                item.creation_date if item.file_path else 'null',
                item.certificate if item.file_path else 'null',
                item.file_path if item.file_path else 'null',
                item.type,
                item.created_at,
                item.updated_at,
                item.rating if item.rating else 'null',
                item.id
            )).decode() for item in data)
        return args

    def save_genre(self, data) -> list:
        args = ','.join(self.cursor.mogrify(
            "('{}', {}, '{}', '{}', '{}')".format(
                item.name,
                str(item.description).replace("'", '"').replace("None", 'null'),
                item.created_at,
                item.updated_at,
                item.id
            )).decode() for item in data)
        return args

    def save_genre_film_work(self, data) -> list:
        args = ','.join(self.cursor.mogrify(
            "('{}', '{}', '{}', '{}')".format(
                item.film_work_id,
                item.genre_id,
                item.created_at,
                item.id
            )).decode() for item in data)
        return args

    def save_person(self, data) -> list:
        args = ','.join(self.cursor.mogrify(
            "('{}', {}, '{}', '{}', '{}')".format(
                item.full_name.replace("'", '"'),
                item.birth_date if item.birth_date else 'null',
                item.created_at,
                item.updated_at,
                item.id
            )).decode() for item in data)
        return args

    def save_person_film_work(self, data) -> list:
        args = ','.join(self.cursor.mogrify(
            "('{}', '{}', '{}', '{}', '{}')".format(
                item.film_work_id,
                item.person_id,
                item.role,
                item.created_at,
                item.id,
            )).decode() for item in data)
        return args

    def save_all_data(self, data: dict) -> bool:
        for table in data:
            save_data = []
            method = getattr(self, f'save_{table}')  # получаем имя метода
            for line in data[table]:
                if self.counter < 99:
                    save_data.append(line)
                    self.counter += 1
                    continue
                else:
                    save_data.append(line)
                    self.counter = 0
                    try:
                        self.cursor.execute(f"""
                            INSERT INTO content.{table} ({", ".join(i for i in data[table][0].__annotations__)})
                            VALUES {method(save_data)}
                            ON CONFLICT (id) DO NOTHING
                            """)
                        save_data.clear()
                        self.conn.commit()
                    except Exception as err:
                        print(err)
                        break
                    continue
            try:
                self.cursor.execute(f"""
                    INSERT INTO content.{table} ({", ".join(i for i in data[table][0].__annotations__)})
                    VALUES {method(save_data)}
                    ON CONFLICT (id) DO NOTHING
                    """)
                save_data.clear()
                self.conn.commit()
            except Exception as err:
                print(err)
                break
        return True
