import json
import traceback
from langchain.chat_models import AzureChatOpenAI
from langchain.memory.chat_message_histories import DynamoDBChatMessageHistory
from langchain.memory import ConversationBufferWindowMemory
from langchain import ConversationChain
from langchain.prompts import MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

chat = AzureChatOpenAI(openai_api_version="2023-05-15", deployment_name="takatsu")

def chat_with_bot(session_id: str, message: str, profile: str):
    chat_history = DynamoDBChatMessageHistory(table_name="qiita-ai", session_id=session_id)
    memory = ConversationBufferWindowMemory(
        memory_key="chat_history", chat_memory=chat_history, return_messages=True, k=3
    )
    system_template = f"""
    あなたはエンジニアマネージャーです。 駆け出しエンジニアと会話してください。
    # 駆け出しエンジニアのプロフィール
    {profile}
    """
    system_prompt = SystemMessagePromptTemplate.from_template(system_template)
    prompt = ChatPromptTemplate.from_messages([
        system_prompt,
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])

    llm_chain = ConversationChain(
        llm=chat,
        prompt=prompt,
        verbose=False,
        memory=memory,
    )
    return llm_chain.run(message)

def make_profile(username: str, note: str, proffesional_skill: str):
    profile =  f"""
    名前: {username} さん
    """
    if note is not None:
        profile += f"自己紹介: {note}\n"
    if proffesional_skill is not None:
        profile += f"職種(スキル): {proffesional_skill}\n"



    return profile


def handler(event, context):
    try:
        session_id = event.get('queryStringParameters', {}).get('user_id', None)
        if session_id is None:
            return {'statusCode': 400, 'body': json.dumps('user_id is required.')}
        message = event.get('queryStringParameters', {}).get('message', None)
        if message is None:
            return {'statusCode': 400, 'body': json.dumps('message is required.')}
        username = event.get('queryStringParameters', {}).get('username', None)
        if username is None:
            return {'statusCode': 400, 'body': json.dumps('username is required.')}
        note = event.get('queryStringParameters', {}).get('note', None)
        proffesional_skill = event.get('queryStringParameters', {}).get('proffesional_skill', None)
        profile = make_profile(username, note, proffesional_skill)
        
        result = chat_with_bot(session_id=session_id, message=message, profile=profile)
        return {'statusCode': 200, 'body': json.dumps({'message': result})}
    
    # エラーが起きた場合
    except Exception:
        traceback.print_exc()
        return {'statusCode': 500, 'body': json.dumps('Exception occurred.')}
