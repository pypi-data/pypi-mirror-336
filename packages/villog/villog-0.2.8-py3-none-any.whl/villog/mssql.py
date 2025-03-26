'''
    MsSQL module
'''

import os
import platform
from time import sleep
from dataclasses import dataclass
from ping3 import ping
import pyodbc
from villog.log import Logger
from villog.writexcel import WorkSheet, WorkBook

class VillSqlException(Exception):
    '''
        Exception for Octopus 8 python module'
    '''
    def __init__(self,
                    message: str) -> None:
        '''
            Exception for Octopus 8 python module'

            Args:
                message (str): Message
        '''
        super().__init__(message)


@dataclass(slots = True)
class SQLConfig:
    '''
        VillSQL configuration class
        Helps to store SQL configuration

        Args:
            server (str): Server name
            database (str): Database name
            username (str): Username
            password (str): Password
    '''
    server: str
    database: str
    username: str
    password: str


class MsSQLClient:
    '''
        MsSQL client class
    '''

    __slots__: list[str] = ["server",
                            "database",
                            "username",
                            "password",
                            "allow_execute",
                            "logger",
                            "driver",
                            "connection",
                            "cursor"]

    def __init__(self,
                 server: str,
                 database: str,
                 username: str,
                 password: str,
                 is_trusted: bool = True,
                 allow_execute: bool = False,
                 logger: Logger | None = None) -> None:
        '''
            MsSQL client class

            Args:
                server (str): Server name
                database (str): Database name
                username (str): Username
                password (str): Password
                is_trusted (bool, optional): Is trusted connection. Defaults to True.
                logger (Logger, optional): Logger. Defaults to None.
        '''
        self.server: str = server
        self.database: str = database
        self.allow_execute: bool = allow_execute
        self.logger: Logger | None = logger
        self.driver: str = self.__get_driver()
        if not self.driver:
            raise VillSqlException("No ODBC driver found")
        if not self.__ping():
            raise VillSqlException("Can't reach the server")
        try:
            self.connection: pyodbc.Connection = self.__connect(username, # pylint: disable=c-extension-no-member
                                                                password,
                                                                is_trusted)
            self.cursor: pyodbc.Connection.cursor = self.connection.cursor() # pylint: disable=c-extension-no-member
        except Exception as error:
            if self.__is_mac_arm():
                raise VillSqlException("If you got a pyodbc error and using a MacOS with ARM cpu, then try to install it with 'pip install --no-binary :all: pyodbc'") from error # pylint: disable=line-too-long
            raise error


    def __str__(self) -> str:
        return f"{self.database}@{self.server}"


    def __log(self,
              content: str) -> None:
        '''
            Log content

            Args:
                content (str): Content to log
        '''
        if self.logger:
            self.logger.log(content)
        else:
            print(content)


    def __is_mac_os(self) -> bool:
        '''
            Check if the OS is Mac
        '''
        return 'darwin' in platform.system().lower()


    def __is_arm(self) -> bool:
        '''
            Check if the CPU is ARM
        '''
        return 'arm' in platform.machine().lower()


    def __is_mac_arm(self) -> bool:
        '''
            Check if the OS is Mac and the CPU is ARM
        '''
        return self.__is_mac_os() and self.__is_arm()


    def __ping(self,
               attempt: int = 5,
               wait: int = 10) -> bool:
        '''
            Ping the server

            Args:
                attempt (int, optional): Number of attempts. Defaults to 5.
                wait (int, optional): Wait time between attempts. Defaults to 10.
        '''
        if attempt != 0:
            response_time: float | None = ping(self.server)
            if response_time or response_time == 0:
                self.__log(f"{self.server} reached")
                return True
            else:
                self.__log(f"Can't reach {self.server}")
                attempt -= 1
                if attempt != 0:
                    self.__log(f"Retrying in {wait} seconds")
                    sleep(wait)
                    self.__ping(attempt, wait)
        self.__log(f"Can't reach {self.server}, no more attempts")
        return False


    def __get_driver(self) -> str | None:
        '''
            Get ODBC driver
        '''
        drivers: list[str] = pyodbc.drivers() # pylint: disable=c-extension-no-member
        for driver in drivers:
            if driver.startswith("ODBC Driver ") and driver.endswith(" for SQL Server"):
                return driver.replace("ODBC Driver ",
                                      "").replace(" for SQL Server",
                                                  "")
        if drivers:
            return drivers[0]
        return None


    def __connect(self,
                  username: str,
                  password: str,
                  is_trusted: bool = True) -> pyodbc.Connection: # pylint: disable=c-extension-no-member
        '''
            Connect to the server

            Args:
                username (str): Username
                password (str): Password
                is_trusted (bool, optional): Is trusted connection. Defaults to True.
        '''
        connection_string: str = ""
        connection_string += 'DRIVER={ODBC Driver ' + self.driver
        connection_string += ' for SQL Server};SERVER=' + self.server
        connection_string += ';DATABASE=' + self.database
        connection_string += ';UID=' + username
        connection_string += ';PWD=' + password
        connection_string += ";TrustServerCertificate=" + ("yes" if is_trusted else "no") + ";"
        self.__log(f"Connecting to {self.database}@{self.server}")
        connection: pyodbc.Connection = pyodbc.connect(connection_string) # pylint: disable=c-extension-no-member
        self.__log(f"Connected to {self.database}@{self.server}")
        return connection


    def close(self) -> None:
        '''
            Close connection
        '''
        self.cursor.close()
        self.connection.close()
        self.__log(f"Connection to {self.server} closed")


    def execute(self,
                query: str,
                insert: list | None = None) -> None:
        '''
            Execute query

            Args:
                query (str): Query
                insert (list, optional): Insert values. Defaults to None.
        '''
        if self.allow_execute:
            if insert is not None:
                self.cursor.execute(query, insert)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            self.__log("Executed.")
        else:
            raise VillSqlException("Execution is not allowed, set 'allow_execute' to True")


    def select(self,
               query: str,
               insert: list | None = None) -> tuple|None:
        '''
            Select query

            Args:
                query (str): Query
                insert (list, optional): Insert values. Defaults to None.
        '''
        if insert is not None:
            self.cursor.execute(query, insert)
        else:
            self.cursor.execute(query)
        result = self.cursor.fetchall()
        columns = [description[0] for description in self.cursor.description]
        return columns, result


    def one_value_select(self,
                         query: str,
                         insert: list | None = None) -> any:
        '''
            Select one value
            (If the query returns more than one value, it will return the first one)

            Args:
                query (str): Query
                insert (list, optional): Insert values. Defaults to None.
        '''
        _, result = self.select(query,
                                insert)
        return result[0][0] if result else None


class Table:
    '''
        Table class for Octopus 8
    '''

    __slots__ = ["columns",
                 "rows"]

    def __init__(self,
                 columns: list,
                 rows: list[list]) -> None:
        '''
            Table class for Octopus

            Args:
                columns (list): Columns
                rows (list[list]): Rows
        '''
        self.columns: list = columns
        self.rows: list[list] = rows


    def __column_index(self,
                       column_name: str) -> int | None:
        '''
            Get column index

            Args:
                column_name (str): Column name
        '''
        for index, column in enumerate(self.columns):
            if column.lower() == column_name.lower():
                return index
        return None


    def return_column(self,
                      column_name: str) -> list[str] | None:
        '''
            Return the given column if exists

            Args:
                column_name (str): Column name
        '''
        if isinstance(column_name, list):
            raise VillSqlException("For multiple columns use 'return_columns'")
        column_index: int | None = self.__column_index(column_name)
        if column_index is not None:
            return [row[column_index] for row in self.rows]
        return None


    def return_columns(self,
                       column_names: list[str]) -> list[list] | None:
        '''
            Return the given columns if exists

            Args:
                column_names (list[str]): Column names
        '''
        if not isinstance(column_names,
                          list):
            if isinstance(column_names,
                          str):
                raise VillSqlException("For single column use 'return_column'")
            raise VillSqlException("Column names must be a list")
        new_rows: list[list] = []
        for row in self.rows:
            new_row: list = []
            for column_name in column_names:
                column_index: int = self.__column_index(column_name)
                if column_index is not None:
                    new_row.append(row[column_index])
            new_rows.append(new_row)
        return new_rows


    def set_filter(self,
                   column_names: list[str]) -> None:
        '''
            Filter table by column names

            Args:
                column_names (list[str]): Column names
        '''
        self.rows = self.return_columns(column_names)
        self.columns = column_names


    def export_to_excel(self,
                        path: str) -> str:
        '''
            Export table to excel

            Args:
                path (str, optional): Path. Defaults to None.
                sheet_name (str, optional): Sheet name. Defaults to None.
        '''
        WorkBook(name = "Book1",
                 sheets = WorkSheet(name = "Sheet1",
                                    header = self.columns,
                                    data = self.rows)).xlsx_create(file_path = path)


class VillSQL:
    '''
        Octopus 8 class
    '''

    __slots__: list[str] = ["__do_logs",
                            "__logger",
                            "__client",
                            "__row_limit",
                            "__tables",
                            "__allow_execute"]

    def __init__(self,
                 sql_config: SQLConfig | None = None,
                 server: str | None = None,
                 database: str | None = None,
                 username: str | None = None,
                 password: str | None = None,
                 is_server_trusted: bool = True,
                 do_logs: bool = True,
                 logger: Logger | None = None,
                 row_limit: int | None = None,
                 do_table_fetch: bool = False,
                 allow_execute: bool = False) -> None:
        '''
            Octopus 8 class

            Args:
                sql_config (SQLConfig, optional): SQL configuration. Defaults to None.
                server (str, optional): Server name. Defaults to None.
                database (str, optional): Database name. Defaults to None.
                username (str, optional): Username. Defaults to None.
                password (str, optional): Password. Defaults to None.
                is_server_trusted (bool, optional): Is trusted connection. Defaults to True.
                do_logs (bool, optional): Do logs. Defaults to True.
                logger (Logger, optional): Logger. Defaults to None.
                row_limit (int, optional): Row limit. Defaults to None.
                do_table_fetch (bool, optional): Do table fetch. Defaults to True.
                allow_execute (bool, optional): Allow execute. Defaults to False.
        '''
        self.__do_logs: bool = do_logs
        if do_logs:
            self.__logger: Logger = logger or Logger(file_path = os.path.join(os.getcwd(),
                                                                              "octopus.log"))
        server_c: str = sql_config.server if sql_config else server
        database_c: str = sql_config.database if sql_config else database
        username_c: str = sql_config.username if sql_config else username
        password_c: str = sql_config.password if sql_config else password
        self.__client: MsSQLClient = MsSQLClient(server = server_c,
                                                 database = database_c,
                                                 username = username_c,
                                                 password = password_c,
                                                 is_trusted = is_server_trusted,
                                                 logger = logger,
                                                 allow_execute = allow_execute)
        del server_c, database_c, username_c, password_c
        self.__row_limit: int | None = row_limit
        self.__tables: list[str] = self.__get_tables()

        if do_table_fetch:
            for table in self.__tables:
                if table.lower() != "table":
                    setattr(self,
                            f"get_table_{table.lower()}",
                            lambda table = table,
                            raw_filter = "",
                            order_by = None,
                            **kfilter:
                            self.get_table(table,
                                           raw_filter,
                                           order_by,
                                           **kfilter))
        self.__allow_execute: bool = allow_execute


    def __str__(self) -> str:
        return str(self.__client)


    def __log(self,
              content: str) -> None:
        '''
            Log content
        
            Args:
                content (str): Content to log
        '''
        if self.__do_logs:
            self.__logger.log(content)
        else:
            print(content)


    def __get_row_limit(self) -> str:
        '''
            Get row limit for query
        '''
        if self.__row_limit and self.__row_limit > 0:
            return f" top {str(self.__row_limit)}"
        return ""


    def set_row_limit(self,
                      row_limit: int) -> None:
        '''
            Set row limit
        
            Args:
                row_limit (int): Row limit
        '''
        self.__row_limit = row_limit


    def __get_tables(self) -> list[str]:
        '''
            Get tables from database
        '''
        print("Getting tables")
        _, results = self.__client.select("select name from sys.tables")
        tables = [result[0] for result in results]
        if not tables:
            raise VillSqlException("No tables found")
        return tables


    def __is_table(self,
                   table: str) -> bool:
        '''
            Check if table exists

            Args:
                table (str): Table name
        '''
        for tbl in self.__tables:
            if tbl.lower() == table.lower():
                self.__log(f"Table '{table}' found")
                return True
        self.__log(f"Table '{table}' not found")
        return False


    def __kfilter_to_query(self,
                           kfilter_item: list) -> str:
        '''
            Convert kwargs filter to query
        
            Args:
                kfilter_item (list): Kwargs filter item
        '''
        if isinstance(kfilter_item[1],
                      str):
            if kfilter_item[1].lower() in ("null", "is null"):
                return f"{kfilter_item[0]} is null"
            if kfilter_item[1].lower() in ("not null", "is not null"):
                return f"{kfilter_item[0]} is not null"
            return f"{kfilter_item[0]} = '{kfilter_item[1]}'"
        if isinstance(kfilter_item[1],
                      int):
            return f"{kfilter_item[0]} = {kfilter_item[1]}"


    def get_table(self,
                  table: str,
                  raw_filter: str = "",
                  order_by: list[tuple] | None = None,
                  **kfilter) -> Table:
        '''
            Selects a table from the database and returns it as a Table object

            Args:
                table (str): Database table's name
                raw_filter (str, optional): Raw filter string after where clause. Defaults to "". 
                    Eg. "column like '%xyz%'"
                order_by (list[tuple], optional): Order by clause. Defaults to None. 
                    Eg. [("column_name_1", "ASC"), ("column_name_2", "DESC")]
                **kfilter: Kwargs filter after the where clause. Defaults to {}. 
                    Eg. column_name_1 = "value_1", column_name_2 = 123
        '''
        if self.__is_table(table):
            query: str = f"select {self.__get_row_limit()} * from {table} with (nolock) where 1 = 1"
            if raw_filter:
                query += f" and {raw_filter}"
            if kfilter:
                for kfilter_item in kfilter.items():
                    query += f" and {self.__kfilter_to_query(kfilter_item)}"
            if order_by:
                query += " order by "
                for i, order in enumerate(order_by):
                    query += f"{order[0]} {order[1]}{'' if len(order_by) - 1 == i else ', '} "
            self.__log(f"Executing: {(query)}")
            columns, result = self.__client.select(query)
            if result:
                return Table(columns, result)
        return None


    def custom_query(self,
                     query: str,
                     inserter: list[any] | None = None) -> tuple | None:
        '''
            Selects a custom query from the database

            Arg:
                query (str): Query string
                inserter (list[any], optional): Insert values. Defaults to None.
        '''
        if self.__allow_execute:
            return self.__client.select(query,
                                        inserter)
        raise VillSqlException("Custom query is only allowed if 'allow_execute' is set to True")


    def custom_query_to_table(self,
                              query: str,
                              inserter: list[any] | None = None) -> Table:
        '''
            Selects a custom query from the database and returns it as a Table object

            Arg:
                query (str): Query string
                inserter (list[any], optional): Insert values. Defaults to None.
        '''
        columns, result = self.custom_query(query,
                                            inserter)
        if result:
            return Table(columns, result)
        return None


    def custom_query_only_columns(self,
                                  query: str,
                                  inserter: list[any] | None = None) -> list[str] | None:
        '''
            Selects a custom query from the database and returns only the columns

            Arg:
                query (str): Query string
                inserter (list[any], optional): Insert values. Defaults to None.
        '''
        columns, _ = self.__client.select(query,
                                          inserter)
        return columns


    def custom_query_only_values(self,
                                 query: str,
                                 inserter: list[any] | None = None) -> list[list] | None:
        '''
            Selects a custom query from the database and returns only the values

            Arg:
                query (str): Query string
                inserter (list[any], optional): Insert values. Defaults to None.
        '''
        _, result = self.__client.select(query,
                                         inserter)
        return result


    def execute(self,
                query: str,
                insert: list | None = None) -> None:
        '''
            Execute a query

            Args:
                query (str): Query string
                insert (list, optional): Insert values. Defaults to None.
        '''
        if self.__allow_execute:
            self.__client.execute(query,
                                  insert)
        else:
            raise VillSqlException("Execution is not allowed, set 'allow_execute' to True")


    def __read_file(self,
                    path: str,
                    encoding: str = "utf-8-sig") -> str:
        '''
            Read file content

            Args:
                path (str): File path
                encoding (str, optional): Encoding. Defaults to "utf-8-sig".
        '''
        if not os.path.exists(path):
            raise VillSqlException(f"File not found: {path}")
        with open(file = path,
                  mode = "r",
                  encoding = encoding) as file:
            return file.read()


    def execute_file(self,
                     path: str,
                     encoding: str = "utf-8-sig") -> None:
        '''
            Execute file content

            Args:
                path (str): File path
                encoding (str, optional): Encoding. Defaults to "utf-8-sig".
        '''
        return self.custom_query(self.__read_file(path,
                                                  encoding))


    def execute_file_to_table(self,
                              path: str,
                              encoding: str = "utf-8-sig") -> Table:
        '''
            Execute file content and return as Table

            Args:
                path (str): File path
                encoding (str, optional): Encoding. Defaults to "utf-8-sig".
        '''
        return self.custom_query_to_table(self.__read_file(path,
                                                           encoding))


    def close(self) -> None:
        '''
            Close connection
        '''
        self.__client.close()
