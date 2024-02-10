# 概要
チャット履歴を考慮してLLMに問い合わせするAPI
Lambda + DynamoDB(チャット履歴の保存)環境で
Python + Langchainで実装

# 使い方

エンドポイント
https://vhujivoxartumnuhje53lm6rii0nrnuu.lambda-url.ap-northeast-1.on.aws/

パラメーター
user_id: ユーザーを一意に特定できるIDに
message: 入力プロンプト


## 使用例
https://vhujivoxartumnuhje53lm6rii0nrnuu.lambda-url.ap-northeast-1.on.aws/?user_id=1&message=こんにちわ

