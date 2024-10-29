from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from utils.prompt_template import create_chat_prompt_template
from utils.settings import LLMConfig


def create_agent_executor(model_name="gpt-4o-mini", temperature=0.7, streaming=True, tools: list = [], system_prompt: str = None):
    llm = ChatOpenAI(model=model_name, temperature=temperature, streaming=streaming)
    prompt = create_chat_prompt_template(system_prompt=system_prompt)
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=LLMConfig.verbose).with_config(
        {"run_name": "Agent"}
    )
    return agent_executor
