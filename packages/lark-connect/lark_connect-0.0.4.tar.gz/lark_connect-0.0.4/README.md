# Lark Connect
**Lark App**는 Lark API를 쉽게 연동하여 메시지 전송, 봇 관리, 앱 통합 등의 기능을 제공하는 Python 패키지입니다.  

## 🚀 설치  
```bash
pip install lark-connect


📌 주요 기능
✅ Lark 메시지 전송 (LarkClient)
✅ Lark Docs 문서 관리 (LarkDocManager)
✅ Lark Sheet 스프레드시트 관리 (LarkSheetManager)
✅ API 응답 타입 정의 및 예외 처리 (typings.py, exceptions.py)

# 사용 예시

python
from lark_connect.core import LarkCore

app_id = "YOUR_APP_ID"
app_access_secret = "YOUR_APP_SECRET"

client = LarkCore(app_id, app_access_secret)

client.send_message("안녕하세요! Lark App을 사용해보세요 🚀")