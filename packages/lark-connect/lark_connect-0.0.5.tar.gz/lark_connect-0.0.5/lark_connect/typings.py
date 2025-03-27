from typing import TypedDict


class SheetCoordinate:
    ROW = 0
    COL = 1


class SheetProperty(TypedDict):
    ownerUser: int
    revision: int
    sheetCount: int
    title: str


class Merge(TypedDict):
    columnCount: int
    rowCount: int
    startColumnIndex: int
    startRowIndex: int


class Sheet(TypedDict):
    columnCount: int
    frozenColCount: int
    frozenRowCount: int
    index: int
    merges: list[Merge]
    rowCount: int
    sheetId: str
    title: str


class SheetData(TypedDict):
    property: SheetProperty
    sheets: list[Sheet]
    spreadsheetToken: str


class LarkSheetInfoAPI(TypedDict):
    code: int
    data: SheetData
    msg: str

