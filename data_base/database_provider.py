from data_base.database_service import DatabaseService
from data_base.database_service_impl import DatabaseServiceImpl
from data_base.database_service_impl_as_dict import DatabaseServiceImplAsDict, shared_data
from typing import Callable

# Define a type for the database provider function
DatabaseProvider = Callable[[], DatabaseService]

def get_dict_db_service() -> DatabaseServiceImplAsDict:
    return DatabaseServiceImplAsDict(shared_data)

def get_sql_db_service() -> DatabaseServiceImpl:
    return DatabaseServiceImpl()


database_provider: DatabaseProvider = get_sql_db_service