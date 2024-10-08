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
from langchain.agents import AgentExecutor

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
            name="Kiến thức tại giáo trình",
            markdown_description="Kiến thực được thu thập trong giáo trình **Tư tuởng Hồ Chí Minh**",
            icon="https://png.pngtree.com/element_pic/17/03/30/d60a84b9aa3a7552ecef9bb5e4ada727.jpg",
        ), 
        cl.ChatProfile(
            name="Kiến thức mở rộng",
            markdown_description="Trong giai đoạn phát triển.",
            icon="https://png.pngtree.com/element_pic/17/03/30/d60a84b9aa3a7552ecef9bb5e4ada727.jpg",
        ),
    ]
            
@cl.on_chat_start
async def on_chat_start():
    app_user: cl.User = cl.user_session.get("user") # type: ignore
    cl.user_session.set("runnable", create_agent_executor(tools=[search_similarity]))
    msg = cl.Message(f"Chào bạn học {app_user.display_name}! Bạn đã sẵn sàng để tìm hiểu về tư tưởng và sự nghiệp vĩ đại của Chủ tịch Hồ Chí Minh chưa? Hãy bắt đầu ngay với những câu hỏi trắc nghiệm thú vị nhé!\n")
    cl.user_session.set("message_history", [{"role": "assistant", "content": msg.content}], )
    await msg.send()

@cl.on_message
async def on_message(message: cl.Message):
    # await toolcall()
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
                # Empty content in the context of OpenAI means
                # that the model is asking for a tool to be invoked.
                # So we only print non-empty content
                # print('***')
                await msg.stream_token(content)
    
    

    # stream = await client.chat.completions.create(
    #     messages=message_history, stream=True, **llm_settings
    # )

    # async for part in stream:
    #     if token := part.choices[0].delta.content or "":
    #         await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
