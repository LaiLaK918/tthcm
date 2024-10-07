from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from utils.prompt_template import chat_prompt_template as prompt


def create_agent_executor(model_name="gpt-4o-mini", temperature=0.7, streaming=True, tools: list = []):
    llm = ChatOpenAI(model=model_name, temperature=temperature, streaming=streaming)
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True).with_config(
        {"run_name": "Agent"}
    )
    return agent_executor
