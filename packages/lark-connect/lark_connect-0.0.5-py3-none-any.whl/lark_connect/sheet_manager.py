import re
import logging
import requests
import datetime
from typing import Tuple, Optional, Iterable

from . import LarkCore
from .typings import SheetCoordinate, LarkSheetInfoAPI

logger = logging.getLogger('__name__')


class LarkSheetManager(LarkCore):
    """
    라크 시트의 정보를 가져오거나, 셀을 업데이트 하는 등 라크 시트 동작 정의 클래스
    라크 API status code 참고 문서\n
    https://open.larksuite.com/document/server-docs/getting-started/server-error-codes
    """

    BASE_URL = "https://open.larksuite.com/open-apis/sheets/v2/spreadsheets"

    def __init__(self, app_id, app_secret, sheet_url):
        super().__init__(app_id, app_secret)
        sheet_token, sheet_id = self.get_sheet_token_n_id_from_url(sheet_url)
        self.sheet_id = sheet_id

        self.sheet_info_api = f"{self.BASE_URL}/{sheet_token}/metainfo"
        self.prepend_sheet_values_api = f"{self.BASE_URL}/{sheet_token}/values_prepend"
        self.update_sheet_values_api = (
            f"{self.BASE_URL}/{sheet_token}/values_batch_update"
        )
        self.sheet_values_api = f"{self.BASE_URL}/{sheet_token}/values"
        self.find_cell_api = f"https://open.larksuite.com/open-apis/sheets/v3/spreadsheets/{sheet_token}/sheets/{sheet_id}/find"

    @staticmethod
    def get_sheet_token_n_id_from_url(url: str) -> tuple[str, str]:
        temp = url.split("?", 2)
        sheet_token = temp[0].split("/")[-1]
        params = temp[1].split("&")

        sheet_id = None
        for param in params:
            if "sheet=" in param:
                sheet_id = param.split("=")[-1]
        if sheet_id is None:
            raise
        return sheet_token, sheet_id

    def _get_sheet_id_match_title(self, sheet_title):
        sheet_id = None

        response = requests.get(self.sheet_info_api, headers=self._header)

        if response.status_code != 200:
            raise Exception(f"request to get sheet info failed: {response.text}")

        result: LarkSheetInfoAPI = response.json()
        sheets_data = result["data"]["sheets"]

        for sheet in sheets_data:
            if sheet["title"] == sheet_title:
                sheet_id = sheet["sheetId"]
                break

        if sheet_id is None:
            raise Exception("시트 제목과 일치하는 시트를 찾을 수 없습니다.")

        return sheet_id

    def format_cell_range(
        self,
        nth: Optional[int] = None,
        coord_type: Optional[SheetCoordinate] = None,
        start_cell: Optional[str] = None,
        end_cell: Optional[str] = None,
    ):
        if start_cell and end_cell:
            return f"{self.sheet_id}!{start_cell}:{end_cell}"

        if coord_type == SheetCoordinate.ROW and nth:
            row = str(nth)
            sheet_range = f"{self.sheet_id}!{row}:{row}"
        elif coord_type == SheetCoordinate.COL and nth:
            col = LarkSheetManager.column_num_to_name(nth)
            sheet_range = f"{self.sheet_id}!{col}:{col}"
        else:
            sheet_range = self.sheet_id
        return sheet_range

    @staticmethod
    def convert_date_obj_cell_in_values(values: list[Iterable]):
        return [
            [
                {"type": "formula", "text": f"=DATE({cell.year},{cell.month},{cell.day})"}
                if isinstance(cell, datetime.date) else cell for cell in value
            ]
            for value in values
        ]

    def prepend_sheet_cells(self, start_cell: str, end_cell: str, values: list):
        """
            참고 문서\n
            https://open.larksuite.com/document/server-docs/docs/sheets-v3/data-operation/prepend-data

            sheet_range: <sheetId>!<start_cell>:<end cell>, e.g) 0b**12!A:B
            title: Change sheet title
            :return:
        """
        update_range = f"{self.sheet_id}!{start_cell}:{end_cell}"

        request_body = {
            "valueRange": {
                "range": f"{update_range}",
                "values": values
            }
        }

        res = requests.post(
            url=self.prepend_sheet_values_api,
            headers=self._header,
            json=request_body,
        )

        self.handle_lark_api_exception(res)

    def update_sheet_cells(self, start_cell: str, end_cell: str, values: list):
        """
        참고 문서\n
        https://open.larksuite.com/document/server-docs/docs/sheets-v3/data-operation/write-data-to-multiple-ranges\n
        https://open.larksuite.com/document/server-docs/docs/sheets-v3/guide/overview

        sheet_range: <sheetId>!<start_cell>:<end cell>, e.g) 0b**12!A:B
        title: Change sheet title
        :return:
        """
        update_range = f"{self.sheet_id}!{start_cell}:{end_cell}"

        request_body = {
            "valueRanges": [
                {"range": f"{update_range}", "values": [values]},
            ]
        }

        res = requests.post(
            url=self.update_sheet_values_api,
            headers=self._header,
            json=request_body,
        )

        self.handle_lark_api_exception(res)

    def find_cell_in_row_or_col(
        self,
        target: str,
        nth: int = None,
        coord_type: SheetCoordinate = SheetCoordinate.COL,
    ) -> list:
        """
        특정 행 또는 열에서 지정된 문자열을 검색합니다.
        참고 문서 : https://open.larksuite.com/document/server-docs/docs/sheets-v3/data-operation/find
        :param target: 찾고자 하는 문자열
        :param nth: 검색할 행 또는 열 번호
        :param coord_type: 검색할 대상 (SheetCoordinate.ROW 또는 SheetCoordinate.COL
        :return: 일치하는 셀 목록
        """
        cell_range = self.format_cell_range(nth, coord_type)
        req_body = {
            "find_condition": {
                "range": cell_range,
                "match_case": True,
                "match_entire_cell": True,
                "include_formulas": True,
            },
            "find": target,
        }

        response = requests.post(
            self.find_cell_api, headers=self._header, json=req_body
        )
        self.handle_lark_api_exception(response)

        find_result = response.json()
        found_cells = find_result["data"]["find_result"]["matched_cells"]
        if not found_cells:
            logger.warning("일치하는 셀이 없습니다.")
            raise ValueError("일치하는 셀이 없습니다.")

        return found_cells

    def get_sheet_range_values(
        self,
        nth: int | None = None,
        coord_type: SheetCoordinate | None = None,
        start_cell: str | None = None,
        end_cell: str | None = None,
    ):
        cell_range = self.format_cell_range(
            nth=nth, coord_type=coord_type, start_cell=start_cell, end_cell=end_cell
        )
        data_api = f"{self.sheet_values_api}/{cell_range}?dateTimeRenderOption=FormattedString"
        res = requests.get(data_api, headers=self._header)

        self.handle_lark_api_exception(res)

        sheet_data = res.json()
        values = sheet_data.get("data", {}).get("valueRange", {}).get("values", [])

        return values

    @staticmethod
    def position_to_cords(cell: str) -> Tuple[int, int]:
        """
        셀의 위치 값 (e.g., 'A1', 'B2') 을 (row, col) 튜플로 변환
        """
        match = re.match(r"([A-Z]+)(\d+)", cell)
        if not match:
            raise ValueError(f"Invalid cell format: {cell}")

        col_str, row_str = match.groups()
        col = LarkSheetManager.column_str_to_index(col_str)
        row = int(row_str)

        return row, col

    @staticmethod
    def cords_to_position(row: int, col: int) -> str:
        """
        (row, col) 튜플을 시트 포지션 스타일 스트링('A2') 으로 변환.
        """
        col_str = LarkSheetManager.column_num_to_name(col)
        return f"{col_str}{row}"

    @staticmethod
    def column_num_to_name(n: int) -> str:
        """
        n번째 칼럼의 칼럼명을 구한다. (e.g., 1 -> A, 27 -> AA).
        :param n: Column number (1-based index).
        :return: Column name.
        """
        if n < 1:
            raise ValueError("Column number must be a positive integer")

        column_name = ""
        while n > 0:
            n -= 1
            column_name = chr(n % 26 + ord("A")) + column_name
            n //= 26

        return column_name

    @staticmethod
    def column_str_to_index(col_str: str) -> int:
        """
        칼럼 이름 (e.g., 'A', 'B', 'AA')을 정수형 인덱스 값으로 반환
        """
        index = 0
        for char in col_str:
            index = index * 26 + (ord(char) - ord("A") + 1)
        return index

    @staticmethod
    def are_cells_adjacent(
        cell1: str, cell2: str, adj_type: SheetCoordinate | None = None
    ) -> bool:
        """
        adj_type 이 ROW일때 두 셀의 행이 인접한 행, COL일때 두 셀이 인접한 열인지 체크
        입력 값이 없을때 바로 옆의 셀인지 체크
        """
        pos1 = LarkSheetManager.position_to_cords(cell1)
        pos2 = LarkSheetManager.position_to_cords(cell2)

        row1, col1 = pos1
        row2, col2 = pos2

        if adj_type == SheetCoordinate.ROW:
            result = abs(row2 - row1) == 1
        elif adj_type == SheetCoordinate.COL:
            result = abs(col2 - col1) == 1
        else:
            result = (row1 == row2 and abs(col2 - col1)) == 1 or (
                col1 == col2 and abs(row2 - row1) == 1
            )

        return result

    @staticmethod
    def get_cell_raw_data(cell):
        """
        라크시트 셀 한개의 데이터로부터 해당 셀의 입력 스트링을 파싱합니다.
        :param cell:
        :return:
        """
        if isinstance(cell, str):
            return cell
        if isinstance(cell, list):
            for element in cell:
                if isinstance(element, dict):
                    if element.get("type") == "mention":
                        return element["link"]
                    elif element.get("type") == "url":
                        return element["text"]

