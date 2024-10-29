import chainlit as cl
import chainlit.data as cl_data
from chainlit.input_widget import Select

from utils.models import CustomSQLAlchemyDataLayer
from utils.environment import POSTGRES_DATABASE_URL

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy.future import select

from utils.client import AsyncSessionLocal
from utils.models import User
from utils.agent_executor import create_agent_executor
from utils.tools.query import search_similarity
from utils.tools.update import update_score, get_total_score
from langchain.agents import AgentExecutor
from utils.settings import RuntimeConfig, SystemPromptConfig
from typing import Dict, Optional


cl_data._data_layer = CustomSQLAlchemyDataLayer(POSTGRES_DATABASE_URL) # type: ignore

@cl.oauth_callback
def oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: Dict[str, str],
    default_user: cl.User,
) -> Optional[cl.User]:
    print("raw_user_data", raw_user_data)
    print("default_user", default_user)
    default_user.display_name = raw_user_data.get("name")
    return default_user

@cl.password_auth_callback # type: ignore
async def auth_callback(username: str, password: str):
    # Initialize the password hasher
    ph = PasswordHasher()
    
    async with AsyncSessionLocal() as session: # type: ignore
        async with session.begin():
            # Query the user asynchronously
            stmt = select(User).where(User.identifier == username)
            result = await session.execute(stmt)
            user: User = result.scalars().first()
        
            if not user:
                return None
            
            # Verify the password
            try:
                ph.verify(user.password, password) # type: ignore
                # Create and return the user object if authentication is successful
                cl_user = cl.User(
                    identifier=user.identifier, # type: ignore
                    metadata=user.metadata_, # type: ignore
                    display_name=user.display_name # type: ignore
                )
                return cl_user
            except VerifyMismatchError:
                # Password mismatch
                return None
            
@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name=RuntimeConfig.study_mode_name,
            markdown_description="Kiến thực được thu thập trong giáo trình **Tư tuởng Hồ Chí Minh**",
            icon="https://png.pngtree.com/element_pic/17/03/30/d60a84b9aa3a7552ecef9bb5e4ada727.jpg",
        ), 
        cl.ChatProfile(
            name=RuntimeConfig.exam_mode_name,
            markdown_description="Trong giai đoạn phát triển.",
            icon="https://png.pngtree.com/element_pic/17/03/30/d60a84b9aa3a7552ecef9bb5e4ada727.jpg",
        ),
    ]
            
@cl.on_chat_start
async def on_chat_start():
    app_user = cl.user_session.get("user") # type: cl.User
    chat_profile = cl.user_session.get("chat_profile")
    print(chat_profile, type(chat_profile))
    if chat_profile == RuntimeConfig.study_mode_name:
        msg = cl.Message(f"Chào bạn học {app_user.display_name}! Bạn đã sẵn sàng để tìm hiểu về tư tưởng và sự nghiệp vĩ đại của Chủ tịch Hồ Chí Minh chưa? Hãy bắt đầu ngay với những câu hỏi trắc nghiệm thú vị nhé!\n")
        tools = [search_similarity]
    elif chat_profile == RuntimeConfig.exam_mode_name:
        tools = [search_similarity, update_score, get_total_score]
        cl.user_session.set("score", 0)
        msg = cl.Message(f"Chào mừng bạn {app_user.display_name} đến với bài kiểm tra kiến thức về tư tưởng và sự nghiệp của Chủ tịch Hồ Chí Minh! Bài kiểm tra này gồm {RuntimeConfig.n_question} câu hỏi nhằm đánh giá mức độ hiểu biết của bạn. Hãy tập trung và trả lời từng câu hỏi thật chính xác nhé. Chúc bạn hoàn thành bài kiểm tra với kết quả xuất sắc!")
    cl.user_session.set("message_history", [{"role": "assistant", "content": msg.content}], )
    cl.user_session.set("runnable", create_agent_executor(tools=tools, 
                                                          system_prompt=SystemPromptConfig.get_system_prompt(chat_profile)))
    await msg.send()

@cl.on_message
async def on_message(message: cl.Message):
    message_history = cl.user_session.get("message_history") # type: list
    print("message_history", message_history)
    message_history.append({"role": "user", "content": message.content})
    
    agent_executor = cl.user_session.get("runnable") # type: AgentExecutor

    msg = cl.Message(content="")
    await msg.send()
    
    async for event in agent_executor.astream_events(
    {
        "chat_history": message_history,
        "input": msg.content,
    }, version="v1",):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                await msg.stream_token(content)
    
    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
