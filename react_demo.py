import asyncio
import json
import os

import agentscope
from agentscope.agent import ReActAgent, UserAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.model import AnthropicChatModel, DashScopeChatModel, OpenAIChatModel
from agentscope.tool import Toolkit, execute_python_code, execute_shell_command
from prompt import SYSTEM_PROMPT
from tool import auto_search, qa_bot


async def init_model(model_type):
    if model_type == "qwen":
        return DashScopeChatModel(
            model_name="qwen3-max",  # qwen3-max | qwen3-235b-a22b | qwen3-235b-a22b-thinking-2507 | qwen3-235b-a22b-instruct-2507
            api_key=os.environ["DASHSCOPE_API_KEY"],
            stream=True,
            enable_thinking=True,
        )
    elif model_type == "gpt":
        return OpenAIChatModel(
            model_name="azure-gpt-5_2",  # azure-gpt-5_2 | azure-gpt-4o
            api_key=os.environ["API_HUB_TOKEN"],
            stream=False,
            client_kwargs={"base_url": "https://llm-gateway-proxy.inner.chj.cloud/llm-gateway/v1"},
        )
    elif model_type == "claude":  # 暂时没调通
        return AnthropicChatModel(
            model_name="aws-claude-sonnet-4-5",  # aws-claude-3_5-sonnet | aws-claude-sonnet-4 | aws-claude-sonnet-4-5
            api_key=os.environ["API_HUB_TOKEN"],
            max_tokens=16000,
            stream=False,
            client_kwargs={"base_url": "https://llm-gateway-proxy.inner.chj.cloud/llm-gateway"},
        )
    raise ValueError(f"Unsupported model_type: {model_type}")


async def main():
    # 注册工具
    toolkit = Toolkit()
    toolkit.register_tool_function(execute_python_code)
    toolkit.register_tool_function(execute_shell_command)
    toolkit.register_tool_function(qa_bot)
    toolkit.register_tool_function(auto_search)
    # print("[tool_schemas]", json.dumps(toolkit.get_json_schemas(), ensure_ascii=False, indent=2))

    # 注册技能
    # toolkit.register_agent_skill("skill")
    # print("[skill_prompt]", toolkit.get_agent_skill_prompt())

    # 初始化ReAct代理
    model = await init_model("claude")  # qwen | gpt | claude
    agent = ReActAgent(
        name="服务专家",
        sys_prompt=SYSTEM_PROMPT,
        model=model,
        memory=InMemoryMemory(),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit,
        parallel_tool_calls=True,  # 启用并行工具调用
    )
    # print("[sys_prompt]", agent.sys_prompt)

    # 初始化用户代理
    user = UserAgent(name="车主")

    # 执行对话交互
    msg = None
    while True:
        msg = await user(msg)
        msg = await agent(msg)
        if msg.get_text_content() == "exit":
            break


# 初始化AgentScope Studio，用于追踪Agent的执行过程
agentscope.init(studio_url="http://localhost:3000", project="demo", name="20260122")
# 执行对话主程序
asyncio.run(main())

# python react_demo.py
