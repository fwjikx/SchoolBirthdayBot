import sqlite3


class Database:
    def __init__(self, dp_file):
        self.connection = sqlite3.connect(dp_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):  # Проверка на наличие в бд
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))

    def add_name(self, name, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `name` = ? WHERE `user_id` = ?", (name, user_id,))

    def get_users(self):  # Для рассылки сообщений (В идее проекта это не будет использоваться и сделано на будущее)
        with self.connection:
            return self.cursor.execute("SELECT `user_id`, `birthday_data`, `already`, `name` FROM `users`").fetchall()

    def set_active(self, user_id, active):  # Проверка на то, активен ли пользователь или нет
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `already` = ? WHERE `user_id` = ?", (active, user_id,))

    def set_block(self, user_id, active):  # Проверка на то, активен ли пользователь или нет
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `block` = ? WHERE `user_id` = ?", (active, user_id,))

    def add_birthday(self, birthday_data, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `birthday_data` = ? WHERE `user_id` = ?",
                                       (birthday_data, user_id,))
