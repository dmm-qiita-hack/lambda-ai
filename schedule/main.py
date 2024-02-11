import json

import requests


def handler(event, context):
    # APIエンドポイントのURL
    api_url = "https://aiconnectdev.net/v1/messages/schedule"

    # GETリクエストを送信
    response = requests.get(api_url)

    # レスポンスのステータスコードと本文をログに出力
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    # Lambda関数のレスポンスを返す
    return {"statusCode": 200, "body": json.dumps("API Request Successful!")}
