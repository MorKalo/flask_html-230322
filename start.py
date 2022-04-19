from DB.DbRepo import DbRepo
from DB.db_config import local_session, create_all_entities

repo = DbRepo(local_session)

repo.drop_all_tables()
create_all_entities()
repo.reset_db()