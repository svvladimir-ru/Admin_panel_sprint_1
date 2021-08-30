from psycopg2.extensions import connection as _connection


class PostgresSaver:
    """Класс для сохранения данных в бд
    Принимает словарь из sqllite_loader.py со значениями из dataclasses
    проходит циклом, каждые 100 записей добавляет в postgres.
    В postgres добавляются данные из методов, соответствующих названиям таблиц
    """
    def __init__(self, pg_conn: _connection):
        self.conn = pg_conn
        self.cursor = self.conn.cursor()
        self.counter = 0
        self.methods = {
            'film_work': self.film_work,
            'genre': self.genre,
            'genre_film_work': self.genre_film_work,
            'person': self.person,
            'person_film_work': self.person_film_work,
        }

    def film_work(self, data) -> list:
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

    def genre(self, data) -> list:
        args = ','.join(self.cursor.mogrify(
            "('{}', {}, '{}', '{}', '{}')".format(
                item.name,
                str(item.description).replace("'", '"').replace("None", 'null'),
                item.created_at,
                item.updated_at,
                item.id
            )).decode() for item in data)
        return args

    def genre_film_work(self, data) -> list:
        args = ','.join(self.cursor.mogrify(
            "('{}', '{}', '{}', '{}')".format(
                item.film_work_id,
                item.genre_id,
                item.created_at,
                item.id
            )).decode() for item in data)
        return args

    def person(self, data) -> list:
        args = ','.join(self.cursor.mogrify(
            "('{}', {}, '{}', '{}', '{}')".format(
                item.full_name.replace("'", '"'),
                item.birth_date if item.birth_date else 'null',
                item.created_at,
                item.updated_at,
                item.id
            )).decode() for item in data)
        return args

    def person_film_work(self, data) -> list:
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
            save_data = []  # оставил для надежности.
            method = self.methods[f'{table}']  # завел как переменную, что бы ниже не было f'{f'{}'}' и убрал getattr
            for line in data[table]:
                save_data.append(line)
            while len(save_data):  # решил использовать за место batch метода, мне кажется так будет лучше.
                try:
                    self.cursor.execute(f"""
                        INSERT INTO content.{table} ({', '.join(i for i in data[table][0].__annotations__)})
                        VALUES {method(save_data[:100])}
                        ON CONFLICT (id) DO NOTHING
                        """)
                    self.conn.commit()
                    del save_data[:100]
                except Exception:  # для учебный целей не стал подключать логирование, просто сделал выход.
                    return False
        return True
