from psycopg2.extensions import connection as _connection


class PostgresSaver:
    def __init__(self, pg_conn: _connection):
        self.conn = pg_conn
        self.cursor = self.conn.cursor()
        self.counter = 0
        self.tables = ''

    def save_film_work(self, data):
        args = ','.join(self.cursor.mogrify(
                        f"({item.id},"
                        f"{item.title},"
                        f"{item.description},"
                        f"{item.creation_date},"
                        f"{item.certificate},"
                        f"{item.file_path}, "
                        f"{item.rating}, "
                        f"{item.type},"
                        f"{item.created_at},"
                        f"{item.updated_at})"
                        ).decode() for item in data)
        return args

    def save_genre(self, data):
        args = ','.join(self.cursor.mogrify(
                        f"({item.id},"
                        f"{item.name},"
                        f"{item.description},"
                        f"{item.created_at},"
                        f"{item.updated_at})"
                        ).decode() for item in data)
        return args

    def save_genre_film_fork(self, data):
        args = ','.join(self.cursor.mogrify(
                        f"({item.id},"
                        f"{item.film_work_id},"
                        f"{item.genre_id},"
                        f"{item.created_at})"
                        ).decode() for item in data)
        return args

    def save_person(self, data):
        args = ','.join(self.cursor.mogrify(
                        f"({item.id},"
                        f"{item.full_name},"
                        f"{item.birth_date},"
                        f"{item.created_at},"
                        f"{item.updated_at})"
                        ).decode() for item in data)
        return args

    def save_person_film_work(self, data):
        args = ','.join(self.cursor.mogrify(
                        f"({item.id},"
                        f"{item.film_work_id},"
                        f"{item.person_id},"
                        f"{item.role},"
                        f"{item.created_at})"
                        ).decode() for item in data)
        return args

    def save_all_data(self, data):
        for table in data:
            lines = iter(data[table])
            save_data = []
            method = getattr(self, f'save_{table}')
            for line in lines:
                if self.counter < 99:
                    save_data.append(line)
                    self.counter += 1
                    next(lines)
                    continue
                else:
                    save_data.append(line)
                    self.counter = 0
                    # try:
                    self.cursor.execute(f"""
                        INSERT INTO content.{table} (id, name)
                        VALUES {method(save_data)}
                        ON CONFLICT (id) DO UPDATE SET name=EXCLUDED.name
                        """)
                    save_data.clear()
                    # except Exception as err:
                    #     return err
                    continue
            # try:
            self.cursor.execute(f"""
                INSERT INTO content.{table} (id, name)
                VALUES {method(save_data)}
                ON CONFLICT (id) DO UPDATE SET name=EXCLUDED.name
                """)
            save_data.clear()
            # except Exception as err:
            #     return err
        return "Ok"