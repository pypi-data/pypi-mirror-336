'''
    Excel writer module
'''

import os
from datetime import date
from decimal import Decimal
import uuid
import xlsxwriter

def gen_uuid(length: int = 8) -> str:
    '''
        Generating a random UUID
        
        Parameters:
            length (int): length of the UUID
    '''
    return str(uuid.uuid4())[:length]


def is_list(obj: any) -> bool:
    '''
        Return if the object is a list
        
        Parameters:
            obj (any): object
    '''
    return isinstance(obj, list)


class WorkSheet:
    '''
        Worksheet class
    '''

    MIN_WIDTH: int = 10
    MAX_WIDTH: int = 40

    __slots__: list[str] = ["name",
                            "header",
                            "data",
                            "header_comment"]

    def __init__(self,
                 name: str,
                 header: list[str] = None,
                 data: list[list[any]] = None,
                 header_comment: list = None) -> None:
        '''
            Worksheet class

            Parameters:
                name (str): name of the worksheet
                header (list[str]): header of the worksheet
                data (list[list[any]]): data of the worksheet
                header_comment (list[str, str]): comment for the header
        '''
        self.name: str = name if len(name) < 32 else name[:31]
        self.header: list[str] = header
        self.data: list[list] = data
        self.header_comment: list = header_comment if header_comment else []


    # Seggesting a column width with min. and max. filter
    def suggest_width(self,
                      col: int,
                      min_width: int = MIN_WIDTH,
                      max_width: int = MAX_WIDTH) -> None:
        '''
            Suggesting a column width with min. and max. filter
        
            Parameters:
                col (int): column index
                min_width (int): minimum width
                max_width (int): maximum width
        '''

        length: int = min_width
        if self.header:
            if len(str(self.header[col])) > length:
                length: int = len(str(self.header[col]))
        if self.data:
            for row in self.data:
                if len(row) > col and len(str(row[col])) > length:
                    length: int = len(str(row[col]))

        return (length if length < max_width else max_width)


    def set_min_width(self,
                      min_width: int) -> None:
        '''
            Setting the minimum width
        
            Parameters:
                min_width (int): minimum width
        '''
        self.MIN_WIDTH = min_width


    def set_max_width(self,
                      max_width: int) -> None:
        '''
            Setting the maximum width
        
            Parameters:
                max_width (int): maximum width
        '''
        self.MAX_WIDTH = max_width


class WorkBook:
    '''Workbook class'''

    __slots__: list[str] = ["name",
                            "sheets",
                            "__is_list",
                            "sheet_count",
                            "__uuid"]

    def __init__(self,
                 name: str,
                 sheets: list[WorkSheet]) -> None:
        '''
            Workbook class

            Parameters:
                name (str): name of the workbook
                sheets (list[WorkSheet]): worksheets of the workbook
        '''
        self.name: str = name
        self.sheets: list[WorkSheet] = sheets
        self.__is_list: bool = is_list(sheets)
        self.sheet_count: int = self.__get_sheet_count()
        self.__uuid: str = gen_uuid()


    def __get_sheet_count(self) -> int:
        '''
            Return the number of sheets
        '''
        return 1 if not self.__is_list else len(self.sheets)


    # Creating the .xlsx
    def xlsx_create(self,
                    file_path: str = None) -> str:
        '''
            Creating the .xlsx

            Parameters:
                file_path (str): path of the .xlsx file
        '''

        file_path = file_path or os.path.join(os.getcwd(),
                                              f"{self.__uuid}.xlsx")

        # Creating the .xlsx
        file: xlsxwriter.Workbook = xlsxwriter.Workbook(filename = file_path)
        bold_format = file.add_format({"bold": True})
        date_format = file.add_format({'num_format': 'yyyy.mm.dd'})
        number_format = file.add_format({'num_format': '#,##0.00'})

        # Fetching the worksheet(s)
        worksheets: list = []
        if self.__is_list:
            for sheet in self.sheets:
                worksheets.append(sheet)
        else:
            worksheets.append(self.sheets)

        print(f"{file_path} is {str(len(worksheets))} worksheet{'s' if self.__is_list else ''}:")

        # Creating the worksheet(s)
        for wsheet in worksheets:
            print(f"\t {wsheet.name}")
            sheet = file.add_worksheet(wsheet.name)
            row: int = 0
            col: int = 0
            last_row: int = row
            last_col: int = col

            # If available, then creating a header
            if wsheet.header:
                sheet.freeze_panes(1, 0)
                for element in wsheet.header:
                    width = wsheet.suggest_width(col)
                    sheet.set_column(col, col, width)
                    sheet.write(row, col, element, bold_format)
                    # If available, then adding comments
                    if wsheet.header_comment:
                        for comment in wsheet.header_comment:
                            if element == comment[0]:
                                sheet.write_comment(row, col, comment[1])
                    col += 1
                    last_col = (col if col > last_col else last_col)
                row += 1

            # If available, then creating the data
            if wsheet.data:
                last_row = (row if row > last_row else last_row)
                for line in wsheet.data:
                    col = 0
                    for element in line:
                        # Checking for basic types
                        if isinstance(element, date):
                            try:
                                sheet.write_datetime(row, col, element, date_format)
                            except Exception: # pylint: disable=broad-exception-caught
                                pass
                        elif isinstance(element, Decimal):
                            try:
                                sheet.write(row, col, element, number_format)
                            except Exception: # pylint: disable=broad-exception-caught
                                pass
                        else:
                            try:
                                sheet.write(row, col, element)
                            except Exception: # pylint: disable=broad-exception-caught
                                pass
                        col += 1
                        last_col = (col if col > last_col else last_col)
                    row += 1
                    last_row = (row if row > last_row else last_row)

            # If header is available, then adding an aoutfilter
            if wsheet.header:
                if last_col != 0:
                    last_col -= 1
                sheet.autofilter(0, 0, last_row, last_col)

        # Closing the .xlsx
        file.close()

        print(f"xlsx created: {file_path}")

        return file_path
