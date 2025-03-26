'''A simple logger'''

import os
import datetime
import uuid
from typing import Optional

def gen_uuid() -> str:
    '''Generates a UUID'''
    return str(uuid.uuid4())

class LoggerError(Exception):
    '''Exception raised for log file related errors'''

class Logger:
    '''A simple logger class'''

    __slots__: list[str] = ["file_path",
                            "encoding",
                            "time_format",
                            "separator",
                            "__silent",
                            "__enable_remove",
                            "__strip_content"]

    def __init__(self,
                 file_path: Optional[str] = None,
                 encoding: str = "utf-8-sig",
                 time_format: str = "%Y.%m.%d %H:%M:%S",
                 separator: str = "\t",
                 silent: bool = False,
                 enable_remove: bool = False,
                 strip_content: bool = False) -> None:
        '''
            Logger class

            Parameters:
                file_path: path of the log file
                encoding: encoding of the log file
                time_format: time format
                separator: separator
                silent: if True, it will not print the log, just write it to the file
                enable_remove: if True, it will enable the remove function
                strip_content: if True, it will strip the content
        '''
        self.file_path: str = file_path if file_path else os.path.join(os.getcwd(), f"{gen_uuid()}.log")
        self.encoding: str = encoding
        self.time_format: str = time_format
        self.separator: str = separator
        self.__silent: bool = silent
        self.__enable_remove: bool = enable_remove
        self.__strip_content: bool = strip_content

    def __str__(self) -> str:
        return f"Log file: {self.file_path}"

    def __error(self,
                message: str | None = None) -> LoggerError:
        '''
            Prints error message

            Parameters:
                message (str): error message
        '''
        raise LoggerError(str(message or ""))

    def __str_time(self) -> str:
        '''Returns the current time as a string'''
        current_time = datetime.datetime.now()
        try:
            return current_time.strftime(self.time_format)
        except Exception as e: # pylint: disable=broad-except
            print(f"Error: {e}")
            return current_time.strftime("%Y.%m.%d %H:%M:%S")

    def __log_to_file(self,
                      content: any) -> None:
        '''
            Appends file

            Args:
                content (str): content
        '''
        with open(self.file_path,
                  "a+",
                  encoding = self.encoding) as file:
            file.write(str(content))

    def __strip(self,
                content: str) -> str:
        '''
            Strips the content

            Parameters:
                content (str): content
        '''
        return content.strip() if self.__strip_content else content

    def log(self,
            content: any = None) -> None:
        '''
            Logs content to file

            Parameters:
                content (str): content
        '''
        self.__log(content = content)

    def change_path(self,
                    file_path: str) -> None:
        '''
            Changes the log file path

            Parameters:
                file_path (str): path of the log file
        '''
        self.__change_path(file_path = file_path)

    def change_encoding(self,
                        encoding: str) -> None:
        '''
            Changes the log file encoding

            Parameters:
                encoding (str): encoding of the log file
        '''
        self.__change_encoding(encoding = encoding)

    def change_time_format(self,
                           time_format: str) -> None:
        '''
            Changes the time format

            Parameters:
                time_format (str): time format
        '''
        self.__change_time_format(time_format = time_format)

    def change_separator(self,
                         separator: str) -> None:
        '''
            Changes the separator

            Parameters:
                separator (str): separator
        '''
        self.__change_separator(separator = separator)

    def clear(self) -> None:
        '''
            Clears the log file
        '''
        self.__clear()

    def remove(self) -> None:
        '''
            Removes the log file
        '''
        self.__remove()

    def __log(self,
              content: str = "") -> None:
        content = self.__str_time() + self.separator + str(self.__strip(content)) + "\n"
        if not self.__silent:
            print(content.strip())
        self.__log_to_file(content)

    def __change_path(self,
                      file_path: str) -> None:
        self.file_path = file_path
        print(f"Changed path from {self.file_path} to {file_path}")

    def __change_encoding(self,
                          encoding: str) -> None:
        self.encoding = encoding
        print(f"Changed encoding to {encoding}")

    def __change_time_format(self,
                             time_format: str) -> None:
        self.time_format = time_format
        print(f"Changed time format to {time_format}")

    def __change_separator(self,
                           separator: str) -> None:
        self.separator = separator
        print(f"Changed separator to {separator}")

    def __clear(self) -> None:
        if self.__enable_remove:
            if os.path.exists(self.file_path):
                with open(self.file_path,
                          "w",
                          encoding = self.encoding) as _:
                    print(f"Log file cleared ({self.file_path})")
            self.__error(f"Log file does not exist ({self.file_path})")
        self.__error("Removal is not enabled")

    def __remove(self) -> None:
        if self.__enable_remove:
            if os.path.exists(self.file_path):
                os.remove(self.file_path)
                print(f"Log file removed ({self.file_path})")
            self.__error(f"Log file does not exist ({self.file_path})")
        self.__error("Removal is not enabled")
