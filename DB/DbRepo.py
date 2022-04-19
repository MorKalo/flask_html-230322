from User import User
from werkzeug.security import generate_password_hash


class DbRepo:
    def __init__(self, local_session):
        self.local_session = local_session

    def get_user_by_id(self, id):
        return self.local_session.query(User).get(id).all()

    def get_all_users(self):
        return self.local_session.query(User).all()

    def post_user(self, user):
        self.local_session.add(user)
        self.local_session.commit()

    def update_by_column_value(self, table_class, column_name, value, data):
        self.local_session.query(table_class).filter(column_name == value).update(data)
        self.local_session.commit()

    def get_user_by_username(self, value):
        return self.local_session.query(User).filter(User.username == value).all()

    def get_user_by_email(self, value):
        return self.local_session.query(User).filter(User.email == value).all()

    def add_all(self, rows_list):
        self.local_session.add_all(rows_list)
        self.local_session.commit()

    def delete_user_by_id(self, id_column_name, id_to_remove):
        self.local_session.query(User).filter(id_column_name == id_to_remove).delete(synchronize_session=False)
        self.local_session.commit()

    def put_by_id(self, id_column_name, id, data):
        exist_object = self.local_session.query(User).filter(id_column_name == id)
        if not exist_object:
            self.local_session.add(exist_object)
        exist_object.update(data)
        self.local_session.commit()

    def patch_by_id(self, id_column_name, id, data):
        exist_object = self.local_session.query(User).filter(id_column_name == id)
        if not exist_object:
            return
        exist_object.update(data)
        self.local_session.commit()

    def drop_all_tables(self):
        self.local_session.execute('drop TABLE users CASCADE')
        self.local_session.commit()

    def reset_db(self):
        self.add_all([User(username='MorMor', email='mormor@gmail.com', password=generate_password_hash('M12345')),
                      User(username='Shlomki', email='shlomki@gmail.com', password=generate_password_hash('S12345')),
                      User(username='Pnina', email='pnina@gmail.com', password=generate_password_hash('P12345')),
                      User(username='Efi', email='efi@gmail.com', password=generate_password_hash('E12345')),
                      User(username='Or', email='or@gmail.com', password=generate_password_hash('O12345'))])

