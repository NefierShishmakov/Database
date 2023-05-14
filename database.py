import psycopg2
from database_parser import SQLRequestParser as SQLParser


class DatabaseController:
    __ADD_REQUEST = "add"
    __DELETE_REQUEST = "delete"
    __UPDATE_REQUEST = "update"

    def __init__(self):
        self.__database = "theatre"
        self.__user = "mrx_db"
        self.__password = "123"
        self.__host = "localhost"
        self.__port = "5432"
        self.__connection: psycopg2.connection = None
        self.__cursor: psycopg2.cursor = None

    def open_connection(self) -> None:
        self.__open_connection_with_database()
        self.__open_cursor()

    def __open_connection_with_database(self) -> None:
        self.__connection = psycopg2.connect(database=self.__database,
                                             user=self.__user,
                                             password=self.__password,
                                             host=self.__host, port=self.__port)

    def __open_cursor(self) -> None:
        self.__cursor = self.__connection.cursor()

    def close_connection(self) -> None:
        self.__close_connection_with_database()
        self.__close_cursor()

    def __close_connection_with_database(self) -> None:
        self.__connection.close()

    def __close_cursor(self) -> None:
        self.__cursor.close()

    def process_request(self, data: dict) -> None:
        modify_type = data['type']
        table_name = data['table_name']
        del data['type']
        del data['table_name']

        match modify_type:
            case self.__ADD_REQUEST:
                self.__add_data_to_table(table_name, data)
            case self.__DELETE_REQUEST:
                self.__delete_table_data(table_name, data)
            case self.__UPDATE_REQUEST:
                self.__update_table_data(table_name, data)

    def __add_data_to_table(self, table_name: str, data: dict) -> None:
        self.__cursor.execute(SQLParser.parse_insert_request(table_name, data))
        self.__connection.commit()

    def __delete_table_data(self, table_name: str, data: dict) -> None:
        self.__cursor.execute(SQLParser.parse_delete_request(table_name, data))
        self.__connection.commit()

    def __update_table_data(self, table_name: str, data: dict) -> None:
        self.__cursor.execute(SQLParser.parse_update_request(table_name, data))
        self.__connection.commit()
