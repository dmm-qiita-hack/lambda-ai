import json
import traceback
from langchain.chat_models import AzureChatOpenAI
from langchain.memory.chat_message_histories import DynamoDBChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

chat = AzureChatOpenAI(openai_api_version="2023-05-15", deployment_name="takatsu")

def chat_with_bot(session_id: str, message: str):
    chat_history = DynamoDBChatMessageHistory(table_name="qiita-ai", session_id=session_id)
    memory = ConversationBufferMemory(
        memory_key="chat_history", chat_memory=chat_history, return_messages=True
    )
    prompt = PromptTemplate(
        input_variables=["chat_history","Query"],
        template="""
        あなたはエンジニアマネージャーです。
        駆け出しエンジニアと会話してください。
        ```

        ```チャット履歴
        {chat_history}
        ```
        Human: {Query}
    Chatbot:
    """
    )

    llm_chain = LLMChain(
        llm=chat,
        prompt=prompt,
        verbose=False,
        memory=memory,
    )
    return llm_chain.predict(Query=message)


def handler(event, context):
    try:
        # イベントデータの 'body' キーをJSONとしてパース
        result = chat_with_bot(session_id=event['queryStringParameters']['user_id'], message=event['queryStringParameters']['message'])
        print(result)
        return {'statusCode': 200, 'body': json.dumps({'message': result})}
    
    # エラーが起きた場合
    except Exception:
        traceback.print_exc()
        return {'statusCode': 500, 'body': json.dumps('Exception occurred.')}
