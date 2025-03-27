import requests
from typing import Optional

from . import LarkCore


class LarkDocManager(LarkCore):
    BASE_URL = 'https://open.larksuite.com/open-apis/docx/v1/documents'

    def __init__(self, app_id, app_secret):
        super().__init__(app_id, app_secret)

    def create_document(self, doc_title, folder_token) -> str:
        """
        참고 문서
        https://open.larksuite.com/document/server-docs/docs/docs/docx-v1/document/create

        doc_title: 생성할 문서의 타이틀
        folder_token: 문서가 위치할 폴더의 토큰
        :return: 생성된 document_id
        """

        request_body = {
            "folder_token": folder_token,
            "title": doc_title
        }

        res = requests.post(
            url=self.BASE_URL,
            headers=self._header,
            json=request_body,
        )

        self.handle_lark_api_exception(res)
        res_json = res.json()

        return res_json["data"]["document"]["document_id"]

    def write_doc_block(self, doc_id, block_content: dict, parent_block_id=None) -> list[str]:
        """
        문서에 블록을 추가하는 메서드

        LarkCore Suite API를 사용하여 지정된 문서에 새로운 블록을 추가합니다.
        https://open.larksuite.com/document/server-docs/docs/docs/docx-v1/document-block/create

        Args:
        - doc_id (str): 문서의 고유 식별자
        - block_content (dict): 추가할 블록 내용 (make_doc_block, make_block_child 참고)
        - parent_block_id (str): 부모 블록의 block_id
          - 부모 블록에 하위 블록을 추가하려면 해당 블록의 block_id를 입력합니다.
          - 문서 트리의 루트 노드에 하위 블록을 추가하려면 document_id를 입력할 수 있습니다.

        Return:
        - str: 추가된 블록의 block_id
        """
        if parent_block_id is None:
            parent_block_id = doc_id
        api_endpoint = self.BASE_URL + f"/{doc_id}/blocks/{parent_block_id}/children"
        res = requests.post(
            url=api_endpoint,
            headers=self._header,
            json=block_content,
        )

        self.handle_lark_api_exception(res)
        res_json = res.json()

        block_children = res_json["data"]["children"]
        block_ids = [block_child["block_id"] for block_child in block_children]

        return block_ids

    @staticmethod
    def make_doc_block(children: Optional[list[dict]] = None, index: Optional[int] = None) -> dict:
        doc_block = {}
        if children is not None:
            doc_block["children"] = children
        if index is not None:
            doc_block["index"] = index
        return doc_block

    @staticmethod
    def make_block_child(block_type: int, param_name, child_content) -> dict:
        return {
            "block_type": block_type,
            param_name: child_content
        }

    @staticmethod
    def make_text_element(text: str, style: Optional[dict] = None) -> dict:
        text_elements = {
            "elements": [
                {
                    "text_run": {
                        "content": text,
                        "text_element_style": {
                            "bold": True,
                        }
                    }
                }
            ],
            "style": {}
        }
        if style is not None:
            text_elements["style"] = style
        return text_elements
