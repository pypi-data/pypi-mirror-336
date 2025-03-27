import json
import logging
import requests

from lark_connect import exceptions

logger = logging.getLogger(__name__)


class LarkClient:
    def __init__(self, app_id, app_secret):
        self.__app_id = app_id
        self.__app_secret = app_secret
        self.__tenant_access_token = self._get_tenant_access_token()
        self._header = {
            "Authorization": f"Bearer {self.__tenant_access_token}",
            "Content-Type": "application/json; charset=utf-8",
        }

    def __str__(self):
        return (f'---- Lark App Info ----\n'
                f'App id is {len(self.__app_id)} character start with {self.__app_id[0]}\n'
                f'App secret is {len(self.__app_secret)} character start with {self.__app_secret[0]}')

    def _get_tenant_access_token(self):
        logger.info('Requesting tenant access token from server...')
        request_body = {"app_id": self.__app_id, "app_secret": self.__app_secret}
        response = requests.post(
            "https://open.larksuite.com/open-apis/auth/v3/app_access_token/internal",
            data=request_body,
        )
        self.handle_lark_api_exception(response)

        result = response.json()

        logger.info("Successfully got access token!")
        return result["tenant_access_token"]

    @staticmethod
    def handle_lark_api_exception(response: requests.Response):
        if response.status_code == 200:
            return

        res_json = json.loads(response.text)
        if response.status_code == 404:
            raise exceptions.LarkInvalidRequestError(response.text)
        elif res_json.get("msg", "") == "Permission Fail":
            raise exceptions.LarkAPIPermissionError(response.text)
        else:
            raise exceptions.LarkAPIError(response.text)


class LarkCore(LarkClient):
    # constants
    MESSAGE_API_BASE = "https://open.larksuite.com/open-apis/im/v1/messages"

    def __init__(self, app_id, app_secret):
        super().__init__(app_id, app_secret)

    def upload_file(self, file_path):
        """lark 서버에 파일을 업로드 후 file_token을 반환 받습니다."""
        url = "https://open.larksuite.com/open-apis/im/v1/files"
        files = {
            "file": (file_path, open(file_path, "rb")),
            "file_type": (None, "doc"),  # "doc" 타입으로 HTML 전송
        }
        response = requests.post(url, headers=self._header, files=files)
        response_data = response.json()
        return response_data["data"]["file_token"]

    def send_message(self, receiver_email: str, message: str, upload_file=None):
        content_dict = {"text": message}
        if upload_file:
            file_token = self.upload_file(upload_file)
            content_dict["file_key"] = file_token
        content_str = json.dumps(content_dict)

        api_url = f"{self.MESSAGE_API_BASE}?receive_id_type=email"
        body = {
            "receive_id_type": "email",
            "receive_id": receiver_email,
            "msg_type": "text",
            "content": content_str,
        }

        res = requests.post(url=api_url, headers=self._header, json=body)
        if res.status_code != 200:
            logger.error(res.text)

        return res.json()

    @staticmethod
    def send_bot_alert(msg: str, bot_url, is_for_all=False):
        """
        LarkCore meessage bot api로 메시지를 전달합니다
        :param msg: 전달할 메시지
        :param bot_url: 메시지를 전달할 bot api url. 입력이 없을 시 수집기 봇으로 메시지를 전달합니다.
        :param is_for_all: @모두 태그 설정
        """
        try:
            message = f'<at user_id="all"> </at>  {msg}' if is_for_all else msg
            header = {"Content-Type": "application/json; charset=utf-8"}
            body = {"msg_type": "text", "content": {"text": message}}

            res = requests.post(bot_url, headers=header, data=json.dumps(body))
            if res.status_code != 200:
                raise
        except Exception as e:
            logger.error(e)
