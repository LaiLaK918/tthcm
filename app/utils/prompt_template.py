from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    PromptTemplate
)

from .environment import SYSTEM_PROMPT

# 1. Define the system message
system_message = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=[], 
        template=SYSTEM_PROMPT
    )
)

# 2. Define the chat history placeholder (optional)
chat_history = MessagesPlaceholder(
    variable_name="chat_history", 
    optional=True
)

# 3. Define the human message template
human_message = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=["input"], 
        template="{input}"
    )
)

# 4. Define the agent scratchpad placeholder
agent_scratchpad = MessagesPlaceholder(
    variable_name="agent_scratchpad"
)

# Combine all components into a ChatPromptTemplate
chat_prompt_template = ChatPromptTemplate.from_messages([
    system_message,
    chat_history,
    human_message,
    agent_scratchpad
])