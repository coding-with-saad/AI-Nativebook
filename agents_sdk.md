# OpenAI Agents SDK

The OpenAI Agents SDK is a lightweight yet powerful Python framework for building multi-agent AI workflows. It provides a production-ready foundation for creating intelligent agents that can use tools, hand off tasks to specialized agents, enforce safety guardrails, and maintain conversation context across interactions. The SDK supports OpenAI's Responses and Chat Completions APIs, as well as 100+ other LLMs through LiteLLM integration.

The core architecture centers on Agents (LLMs configured with instructions, tools, and handoffs), a built-in agent loop that handles tool invocation and response processing, Sessions for automatic conversation history management, and comprehensive Tracing for debugging and monitoring. The framework is designed to be Python-first, allowing developers to use native language features for orchestration while providing sensible defaults that work out of the box.

## Installation

Install the OpenAI Agents SDK using pip or uv with optional dependency groups for additional features.

```bash
# Basic installation
pip install openai-agents

# With voice support
pip install 'openai-agents[voice]'

# With Redis session support
pip install 'openai-agents[redis]'

# With LiteLLM for non-OpenAI models
pip install 'openai-agents[litellm]'

# Using uv
uv add openai-agents
uv add 'openai-agents[voice,litellm]'
```

## Agent Creation and Configuration

Create agents by defining their name, instructions, model, and tools. Agents are the core building blocks that combine an LLM with configurable behavior.

```python
from agents import Agent, ModelSettings, function_tool

@function_tool
def get_weather(city: str) -> str:
    """Returns weather info for the specified city."""
    return f"The weather in {city} is sunny."

@function_tool
def get_stock_price(symbol: str) -> float:
    """Returns the current stock price for a symbol."""
    return 150.25

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant that can check weather and stock prices.",
    model="gpt-4.1",  # or "gpt-5.2" for higher quality
    model_settings=ModelSettings(temperature=0.7),
    tools=[get_weather, get_stock_price],
)

# Clone agents with modifications
specialized_agent = agent.clone(
    name="Weather Specialist",
    instructions="You only answer weather-related questions.",
    tools=[get_weather],
)
```

## Runner.run() - Running Agents

Execute agents using the Runner class which provides async, sync, and streaming modes. The runner manages the agent loop, handling tool calls and handoffs automatically.

```python
import asyncio
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
)

async def main():
    # Async execution
    result = await Runner.run(agent, "What is the capital of France?")
    print(result.final_output)
    # Output: Paris is the capital of France.

    # Access additional result information
    print(f"New items generated: {len(result.new_items)}")
    print(f"Last response ID: {result.last_response_id}")

# Synchronous execution
result = Runner.run_sync(agent, "What is 2 + 2?")
print(result.final_output)
# Output: 4

# With max_turns limit
result = Runner.run_sync(agent, "Complex task", max_turns=5)

if __name__ == "__main__":
    asyncio.run(main())
```

## Runner.run_streamed() - Streaming Responses

Stream agent responses token-by-token for real-time user feedback. The streaming API provides both raw LLM events and higher-level run item events.

```python
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, ItemHelpers

agent = Agent(
    name="Storyteller",
    instructions="You tell engaging stories.",
)

async def main():
    result = Runner.run_streamed(agent, "Tell me a short story about a robot.")

    async for event in result.stream_events():
        # Stream raw text deltas for immediate display
        if event.type == "raw_response_event":
            if isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)

        # Handle high-level events
        elif event.type == "agent_updated_stream_event":
            print(f"\n[Agent switched to: {event.new_agent.name}]")

        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print(f"\n[Tool called: {event.item.name}]")
            elif event.item.type == "tool_call_output_item":
                print(f"\n[Tool output: {event.item.output}]")
            elif event.item.type == "message_output_item":
                print(f"\n[Message: {ItemHelpers.text_message_output(event.item)}]")

    # Final result available after stream completes
    print(f"\n\nFinal output: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
```

## function_tool - Creating Function Tools

Transform Python functions into agent tools with automatic schema generation. The SDK extracts parameter types and descriptions from docstrings and type annotations.

```python
import json
from typing import Annotated
from pydantic import Field, BaseModel
from agents import Agent, Runner, function_tool, FunctionTool, RunContextWrapper

# Basic function tool with docstring
@function_tool
def search_database(query: str, limit: int = 10) -> str:
    """Search the database for matching records.

    Args:
        query: The search query string.
        limit: Maximum number of results to return.
    """
    return f"Found {limit} results for '{query}'"

# With Pydantic Field constraints
@function_tool
def rate_item(
    item_id: str,
    score: Annotated[int, Field(ge=1, le=5, description="Rating from 1 to 5")]
) -> str:
    """Rate an item with a score."""
    return f"Item {item_id} rated with score {score}"

# Async function tool with context access
@function_tool
async def fetch_user_data(ctx: RunContextWrapper, user_id: str) -> str:
    """Fetch data for a specific user.

    Args:
        user_id: The unique identifier of the user.
    """
    # Context is automatically injected as first argument
    return f"User data for {user_id}"

# Function tool with timeout
@function_tool(timeout=5.0)
async def slow_operation(data: str) -> str:
    """Process data with a timeout."""
    import asyncio
    await asyncio.sleep(2)
    return f"Processed: {data}"

# Custom error handling
def custom_error_handler(ctx: RunContextWrapper, error: Exception) -> str:
    return f"Tool failed: {str(error)}"

@function_tool(failure_error_function=custom_error_handler)
def risky_operation(value: int) -> str:
    """An operation that might fail."""
    if value < 0:
        raise ValueError("Value must be positive")
    return f"Result: {value * 2}"

# Create agent with tools
agent = Agent(
    name="Tool Demo",
    instructions="Use the available tools to help users.",
    tools=[search_database, rate_item, fetch_user_data, slow_operation],
)

result = Runner.run_sync(agent, "Search for 'python tutorials' and limit to 5 results")
print(result.final_output)
```

## Handoffs - Agent Delegation

Enable agents to delegate tasks to specialized agents. Handoffs transfer control of the conversation to another agent with optional input filtering and callbacks.

```python
import asyncio
from pydantic import BaseModel
from agents import Agent, Runner, handoff, RunContextWrapper
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

# Specialized agents
billing_agent = Agent(
    name="Billing Agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    You handle all billing-related questions. Be precise about amounts and dates.""",
    handoff_description="Handles billing inquiries, payment issues, and invoice questions",
)

technical_agent = Agent(
    name="Technical Support",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    You provide technical support. Ask clarifying questions about the issue.""",
)

# Handoff with input data
class EscalationData(BaseModel):
    reason: str
    priority: str

async def on_escalation(ctx: RunContextWrapper, data: EscalationData):
    print(f"Escalation: {data.reason} (Priority: {data.priority})")

escalation_agent = Agent(name="Escalation Handler", instructions="Handle escalated issues.")

# Triage agent with handoffs
triage_agent = Agent(
    name="Triage Agent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    You are the first point of contact. Determine the nature of the request and
    hand off to the appropriate specialist. For billing questions, use the billing agent.
    For technical issues, use technical support. For urgent matters, escalate.""",
    handoffs=[
        billing_agent,  # Simple handoff
        handoff(
            agent=technical_agent,
            tool_name_override="transfer_to_tech",
            tool_description_override="Transfer to technical support for software/hardware issues",
        ),
        handoff(
            agent=escalation_agent,
            on_handoff=on_escalation,
            input_type=EscalationData,
        ),
    ],
)

async def main():
    # Billing question - will handoff to billing agent
    result = await Runner.run(
        triage_agent,
        "I have a question about my last invoice. The amount seems wrong."
    )
    print(f"Response: {result.final_output}")
    print(f"Final agent: {result.last_agent.name}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Agents as Tools

Use agents as tools within an orchestrator pattern where a central agent maintains control while delegating specific tasks to specialized sub-agents.

```python
import asyncio
from pydantic import BaseModel, Field
from agents import Agent, Runner

# Specialized agents
spanish_translator = Agent(
    name="Spanish Translator",
    instructions="You translate text to Spanish accurately and naturally.",
)

french_translator = Agent(
    name="French Translator",
    instructions="You translate text to French accurately and naturally.",
)

summarizer = Agent(
    name="Summarizer",
    instructions="You create concise summaries of text while preserving key information.",
)

# Structured input for translation
class TranslationInput(BaseModel):
    text: str = Field(description="Text to translate")
    tone: str = Field(default="neutral", description="Desired tone: formal, casual, neutral")

# Orchestrator agent using sub-agents as tools
orchestrator = Agent(
    name="Language Assistant",
    instructions="""You are a multilingual assistant. Use the available tools to:
    - Translate text to Spanish or French
    - Summarize long texts
    Always use tools when the user requests these services.""",
    tools=[
        spanish_translator.as_tool(
            tool_name="translate_spanish",
            tool_description="Translate text to Spanish",
            parameters=TranslationInput,
        ),
        french_translator.as_tool(
            tool_name="translate_french",
            tool_description="Translate text to French",
        ),
        summarizer.as_tool(
            tool_name="summarize",
            tool_description="Create a summary of the provided text",
        ),
    ],
)

async def main():
    result = await Runner.run(
        orchestrator,
        "Translate 'Hello, how are you today?' to both Spanish and French."
    )
    print(result.final_output)
    # Output includes translations from both sub-agents

if __name__ == "__main__":
    asyncio.run(main())
```

## Sessions - Conversation Memory

Maintain conversation history across multiple agent runs using built-in session management. Sessions eliminate manual history handling between turns.

```python
import asyncio
from agents import Agent, Runner, SQLiteSession
from agents.extensions.memory import SQLAlchemySession, EncryptedSession

agent = Agent(
    name="Assistant",
    instructions="Reply concisely. Remember previous conversation context.",
)

async def sqlite_session_example():
    # In-memory SQLite session
    session = SQLiteSession("user_123")

    # First turn
    result = await Runner.run(
        agent,
        "My name is Alice and I live in Seattle.",
        session=session
    )
    print(f"Turn 1: {result.final_output}")

    # Second turn - agent remembers context
    result = await Runner.run(
        agent,
        "What's my name and where do I live?",
        session=session
    )
    print(f"Turn 2: {result.final_output}")
    # Output: Your name is Alice and you live in Seattle.

async def persistent_session_example():
    # File-based persistent session
    session = SQLiteSession("conversation_456", "conversations.db")

    result = await Runner.run(agent, "Remember that my favorite color is blue.", session=session)
    print(result.final_output)

async def sqlalchemy_session_example():
    # Production-ready PostgreSQL session
    session = SQLAlchemySession.from_url(
        "user_789",
        url="postgresql+asyncpg://user:pass@localhost/db",
        create_tables=True
    )

    result = await Runner.run(agent, "Hello!", session=session)
    print(result.final_output)

async def encrypted_session_example():
    # Encrypted session with TTL
    underlying = SQLiteSession("secure_session")
    session = EncryptedSession(
        session_id="secure_session",
        underlying_session=underlying,
        encryption_key="your-32-byte-secret-key-here!!!",
        ttl=600  # 10 minute expiration
    )

    result = await Runner.run(agent, "Store sensitive information.", session=session)
    print(result.final_output)

async def session_operations_example():
    session = SQLiteSession("ops_demo")

    # Add items manually
    await session.add_items([
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ])

    # Get all items
    items = await session.get_items()
    print(f"History has {len(items)} items")

    # Pop last item (useful for corrections)
    last = await session.pop_item()
    print(f"Removed: {last}")

    # Clear session
    await session.clear_session()

if __name__ == "__main__":
    asyncio.run(sqlite_session_example())
```

## Guardrails - Input/Output Validation

Implement safety checks that validate agent inputs and outputs. Guardrails can run in parallel with agent execution or block until validation completes.

```python
import asyncio
from pydantic import BaseModel
from agents import (
    Agent, Runner, GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered,
    RunContextWrapper, TResponseInputItem,
    input_guardrail, output_guardrail,
)

# Input guardrail to check for inappropriate content
class ContentCheck(BaseModel):
    is_appropriate: bool
    reason: str

content_checker = Agent(
    name="Content Checker",
    instructions="Check if the input is appropriate for a professional assistant.",
    output_type=ContentCheck,
)

@input_guardrail
async def content_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(content_checker, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_appropriate,
    )

# Output guardrail to check for sensitive data
class SensitivityCheck(BaseModel):
    contains_pii: bool
    details: str

sensitivity_checker = Agent(
    name="Sensitivity Checker",
    instructions="Check if the output contains personally identifiable information (PII).",
    output_type=SensitivityCheck,
)

class AssistantOutput(BaseModel):
    response: str

@output_guardrail
async def pii_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    output: AssistantOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(sensitivity_checker, output.response, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.contains_pii,
    )

# Agent with guardrails
guarded_agent = Agent(
    name="Secure Assistant",
    instructions="Help users with their questions professionally.",
    input_guardrails=[content_guardrail],
    output_guardrails=[pii_guardrail],
    output_type=AssistantOutput,
)

async def main():
    try:
        result = await Runner.run(guarded_agent, "What is the weather today?")
        print(result.final_output.response)
    except InputGuardrailTripwireTriggered as e:
        print(f"Input blocked: {e.guardrail_result.output.output_info}")
    except OutputGuardrailTripwireTriggered as e:
        print(f"Output blocked: {e.guardrail_result.output.output_info}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Tool Guardrails - Function Tool Validation

Apply input and output validation directly to function tools, allowing fine-grained control over tool execution.

```python
import json
from agents import (
    Agent, Runner, function_tool,
    ToolGuardrailFunctionOutput,
    tool_input_guardrail, tool_output_guardrail,
)

# Input guardrail to block sensitive data
@tool_input_guardrail
def block_secrets(data):
    args = json.loads(data.context.tool_arguments or "{}")
    if "password" in json.dumps(args).lower():
        return ToolGuardrailFunctionOutput.reject_content(
            "Cannot process requests containing password information."
        )
    return ToolGuardrailFunctionOutput.allow()

# Output guardrail to redact sensitive information
@tool_output_guardrail
def redact_sensitive(data):
    output = str(data.output or "")
    if "secret" in output.lower():
        return ToolGuardrailFunctionOutput.reject_content(
            "Output contained sensitive data and was redacted."
        )
    return ToolGuardrailFunctionOutput.allow()

# Tool with guardrails
@function_tool(
    tool_input_guardrails=[block_secrets],
    tool_output_guardrails=[redact_sensitive],
)
def process_data(user_input: str) -> str:
    """Process user data securely.

    Args:
        user_input: The data to process.
    """
    return f"Processed: {user_input}"

agent = Agent(
    name="Secure Processor",
    instructions="Process data using the available tool.",
    tools=[process_data],
)

result = Runner.run_sync(agent, "Process this text: Hello World")
print(result.final_output)
```

## Structured Output Types

Define structured output schemas using Pydantic models to ensure agents return data in specific formats using OpenAI's structured outputs feature.

```python
import asyncio
from pydantic import BaseModel
from agents import Agent, Runner

# Define structured output types
class CalendarEvent(BaseModel):
    name: str
    date: str
    time: str
    participants: list[str]
    location: str | None = None

class ExtractedEvents(BaseModel):
    events: list[CalendarEvent]
    summary: str

# Agent with structured output
calendar_extractor = Agent(
    name="Calendar Extractor",
    instructions="""Extract calendar events from text.
    Identify event names, dates, times, participants, and locations.
    Provide a brief summary of all events found.""",
    output_type=ExtractedEvents,
)

async def main():
    text = """
    Meeting with John and Sarah tomorrow at 2pm in Conference Room A.
    Then a project review on Friday at 10am with the whole team.
    Don't forget the lunch with clients next Monday at noon at Chez Pierre.
    """

    result = await Runner.run(calendar_extractor, text)

    # Result is typed as ExtractedEvents
    output: ExtractedEvents = result.final_output
    print(f"Found {len(output.events)} events:")
    for event in output.events:
        print(f"  - {event.name} on {event.date} at {event.time}")
        print(f"    Participants: {', '.join(event.participants)}")
        if event.location:
            print(f"    Location: {event.location}")
    print(f"\nSummary: {output.summary}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Human-in-the-Loop - Tool Approval

Pause agent execution for human approval before executing sensitive tool calls. The SDK provides state serialization for long-running approval workflows.

```python
import asyncio
from agents import Agent, Runner, RunState, function_tool

# Tool requiring approval
@function_tool(needs_approval=True)
async def delete_record(record_id: str) -> str:
    """Delete a record from the database.

    Args:
        record_id: The ID of the record to delete.
    """
    return f"Record {record_id} deleted successfully"

# Conditional approval based on parameters
async def needs_large_transfer_approval(ctx, params, call_id) -> bool:
    amount = params.get("amount", 0)
    return amount > 1000

@function_tool(needs_approval=needs_large_transfer_approval)
async def transfer_funds(from_account: str, to_account: str, amount: float) -> str:
    """Transfer funds between accounts.

    Args:
        from_account: Source account ID.
        to_account: Destination account ID.
        amount: Amount to transfer.
    """
    return f"Transferred ${amount} from {from_account} to {to_account}"

agent = Agent(
    name="Banking Assistant",
    instructions="Help users manage their accounts. Always confirm before deleting or large transfers.",
    tools=[delete_record, transfer_funds],
)

async def main():
    result = await Runner.run(agent, "Delete record ABC123 from my account")

    # Check for pending approvals
    while result.interruptions:
        print("Pending approvals:")

        # Convert to state for persistence (can serialize to JSON)
        state = result.to_state()

        for interruption in result.interruptions:
            print(f"  Tool: {interruption.name}")
            print(f"  Arguments: {interruption.arguments}")

            # Simulate user decision
            approved = input("Approve? (y/n): ").lower() == 'y'

            if approved:
                state.approve(interruption)
            else:
                state.reject(interruption)

        # Resume execution with decisions
        result = await Runner.run(agent, state)

    print(f"Final result: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
```

## MCP Server Integration

Connect to Model Context Protocol (MCP) servers to expose external tools to agents. The SDK supports stdio, HTTP with SSE, Streamable HTTP, and hosted MCP transports.

```python
import asyncio
from pathlib import Path
from agents import Agent, Runner, HostedMCPTool
from agents.mcp import MCPServerStdio, MCPServerStreamableHttp, MCPServerManager

# Hosted MCP server (runs on OpenAI infrastructure)
async def hosted_mcp_example():
    agent = Agent(
        name="Git Assistant",
        tools=[
            HostedMCPTool(
                tool_config={
                    "type": "mcp",
                    "server_label": "gitmcp",
                    "server_url": "https://gitmcp.io/openai/codex",
                    "require_approval": "never",
                }
            )
        ],
    )

    result = await Runner.run(agent, "What languages are used in this repository?")
    print(result.final_output)

# Local stdio MCP server
async def stdio_mcp_example():
    samples_dir = Path("./sample_files")

    async with MCPServerStdio(
        name="Filesystem Server",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", str(samples_dir)],
        },
    ) as server:
        agent = Agent(
            name="File Assistant",
            instructions="Use the filesystem tools to help users with their files.",
            mcp_servers=[server],
        )

        result = await Runner.run(agent, "List all files in the directory")
        print(result.final_output)

# HTTP Streamable MCP server
async def http_mcp_example():
    async with MCPServerStreamableHttp(
        name="Custom MCP Server",
        params={
            "url": "http://localhost:8000/mcp",
            "headers": {"Authorization": "Bearer token"},
            "timeout": 30,
        },
        cache_tools_list=True,
    ) as server:
        agent = Agent(
            name="API Assistant",
            mcp_servers=[server],
        )

        result = await Runner.run(agent, "Use the available tools")
        print(result.final_output)

# Multiple MCP servers with manager
async def multi_server_example():
    servers = [
        MCPServerStreamableHttp(name="calendar", params={"url": "http://localhost:8000/mcp"}),
        MCPServerStreamableHttp(name="email", params={"url": "http://localhost:8001/mcp"}),
    ]

    async with MCPServerManager(servers) as manager:
        agent = Agent(
            name="Productivity Assistant",
            mcp_servers=manager.active_servers,
        )

        # Check for failed connections
        if manager.failed_servers:
            print(f"Warning: {len(manager.failed_servers)} servers failed to connect")

        result = await Runner.run(agent, "Show my calendar and unread emails")
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(hosted_mcp_example())
```

## Tracing - Debugging and Monitoring

Use built-in tracing to visualize, debug, and monitor agent workflows. Traces capture LLM generations, tool calls, handoffs, and custom events.

```python
import asyncio
from agents import Agent, Runner, trace, set_tracing_export_api_key, RunConfig

agent = Agent(
    name="Traced Agent",
    instructions="You are a helpful assistant.",
)

async def basic_tracing():
    # Tracing is enabled by default
    result = await Runner.run(
        agent,
        "Hello!",
        run_config=RunConfig(
            workflow_name="Customer Support",
            trace_id="trace_abc123",  # Optional custom trace ID
            group_id="conversation_456",  # Group related traces
            trace_metadata={"user_id": "user_789"},
        ),
    )
    print(result.final_output)

async def grouped_traces():
    # Multiple runs under a single trace
    with trace("Multi-step Workflow") as workflow_trace:
        result1 = await Runner.run(agent, "First question")
        result2 = await Runner.run(agent, f"Follow up on: {result1.final_output}")

        print(f"Trace ID: {workflow_trace.trace_id}")
        print(f"Final: {result2.final_output}")

async def tracing_with_non_openai():
    # Enable tracing for non-OpenAI models
    set_tracing_export_api_key("sk-your-openai-key-for-tracing")

    # Or disable tracing entirely
    result = await Runner.run(
        agent,
        "Hello",
        run_config=RunConfig(tracing_disabled=True),
    )

async def sensitive_data_control():
    # Control sensitive data in traces
    result = await Runner.run(
        agent,
        "Process this sensitive request",
        run_config=RunConfig(
            trace_include_sensitive_data=False,  # Exclude inputs/outputs
        ),
    )

if __name__ == "__main__":
    asyncio.run(basic_tracing())
```

## Model Configuration

Configure different models and providers for agents. The SDK supports OpenAI models via Responses and Chat Completions APIs, plus 100+ other models through LiteLLM.

```python
import asyncio
from agents import Agent, Runner, RunConfig, ModelSettings, AsyncOpenAI
from agents.models import OpenAIChatCompletionsModel

# Different model configurations
high_quality_agent = Agent(
    name="Premium Agent",
    instructions="You provide detailed, thoughtful responses.",
    model="gpt-5.2",
    model_settings=ModelSettings(
        temperature=0.7,
        top_p=0.9,
    ),
)

fast_agent = Agent(
    name="Quick Agent",
    instructions="You provide fast, concise responses.",
    model="gpt-4.1-mini",
    model_settings=ModelSettings(temperature=0.3),
)

# Using Chat Completions API
chat_agent = Agent(
    name="Chat Agent",
    model=OpenAIChatCompletionsModel(
        model="gpt-4.1",
        openai_client=AsyncOpenAI(),
    ),
)

# Using LiteLLM for non-OpenAI models
# pip install 'openai-agents[litellm]'
claude_agent = Agent(
    name="Claude Agent",
    model="litellm/anthropic/claude-3-5-sonnet-20240620",
    instructions="You are Claude, an AI assistant.",
)

gemini_agent = Agent(
    name="Gemini Agent",
    model="litellm/gemini/gemini-2.0-flash",
)

async def main():
    # Override model at runtime via RunConfig
    result = await Runner.run(
        fast_agent,
        "Hello!",
        run_config=RunConfig(
            model="gpt-5.2",  # Override agent's model
            model_settings=ModelSettings(temperature=0.5),
        ),
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

## Hosted Tools - Web Search, File Search, Code Interpreter

Use OpenAI's hosted tools including web search, file search over vector stores, code interpreter, and image generation.

```python
import asyncio
from agents import (
    Agent, Runner,
    WebSearchTool, FileSearchTool,
    CodeInterpreterTool, ImageGenerationTool,
)

# Web search agent
web_agent = Agent(
    name="Research Assistant",
    instructions="Search the web to answer questions with current information.",
    tools=[
        WebSearchTool(
            search_context_size="medium",  # low, medium, high
        ),
    ],
)

# File search over vector stores
file_agent = Agent(
    name="Document Assistant",
    instructions="Search through documents to find relevant information.",
    tools=[
        FileSearchTool(
            vector_store_ids=["vs_abc123"],
            max_num_results=5,
        ),
    ],
)

# Code interpreter for data analysis
code_agent = Agent(
    name="Data Analyst",
    instructions="Use code to analyze data and create visualizations.",
    tools=[CodeInterpreterTool()],
)

# Image generation
image_agent = Agent(
    name="Artist",
    instructions="Generate images based on user descriptions.",
    tools=[ImageGenerationTool()],
)

# Combined tools
research_agent = Agent(
    name="Full Research Assistant",
    instructions="""You are a research assistant that can:
    - Search the web for current information
    - Search through uploaded documents
    - Run code for data analysis
    Use the appropriate tool based on the user's request.""",
    tools=[
        WebSearchTool(),
        FileSearchTool(vector_store_ids=["vs_documents"]),
        CodeInterpreterTool(),
    ],
)

async def main():
    result = await Runner.run(
        web_agent,
        "What are the latest developments in AI agents?"
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

## Dynamic Instructions

Generate agent instructions dynamically based on context. Instructions can be static strings or functions that receive the agent and context.

```python
import asyncio
from dataclasses import dataclass
from agents import Agent, Runner, RunContextWrapper

@dataclass
class UserContext:
    user_id: str
    name: str
    subscription_tier: str
    preferences: dict

def dynamic_instructions(
    context: RunContextWrapper[UserContext],
    agent: Agent[UserContext]
) -> str:
    user = context.context
    tier_instructions = {
        "free": "Provide basic assistance. Suggest premium features when relevant.",
        "premium": "Provide detailed, comprehensive assistance.",
        "enterprise": "Provide priority support with full access to all features.",
    }

    return f"""You are a personalized assistant for {user.name}.
    User ID: {user.user_id}
    Subscription: {user.subscription_tier}

    {tier_instructions.get(user.subscription_tier, tier_instructions['free'])}

    User preferences: {user.preferences}
    """

# Async dynamic instructions
async def async_instructions(
    context: RunContextWrapper[UserContext],
    agent: Agent[UserContext]
) -> str:
    # Can perform async operations like database lookups
    user = context.context
    return f"Welcome back, {user.name}! How can I help you today?"

agent = Agent[UserContext](
    name="Personalized Assistant",
    instructions=dynamic_instructions,
)

async def main():
    user_context = UserContext(
        user_id="user_123",
        name="Alice",
        subscription_tier="premium",
        preferences={"language": "English", "tone": "professional"},
    )

    result = await Runner.run(
        agent,
        "What can you help me with?",
        context=user_context,
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

## RunConfig - Advanced Run Configuration

Configure agent runs with detailed options for models, tracing, guardrails, and conversation management.

```python
import asyncio
from agents import Agent, Runner, RunConfig, ModelSettings
from agents.run import CallModelData, ModelInputData

agent = Agent(
    name="Configurable Agent",
    instructions="You are a helpful assistant.",
)

# Input filter to modify model input before each call
def trim_history(data: CallModelData) -> ModelInputData:
    # Keep only the last 10 messages
    trimmed = data.model_data.input[-10:]
    return ModelInputData(
        input=trimmed,
        instructions=data.model_data.instructions,
    )

# Error handler for max turns exceeded
def handle_max_turns(data) -> dict:
    return {
        "final_output": "I couldn't complete this task in the allowed turns. Please try a simpler request.",
        "include_in_history": False,
    }

async def main():
    result = await Runner.run(
        agent,
        "Help me with a complex task",
        max_turns=10,
        run_config=RunConfig(
            # Model overrides
            model="gpt-4.1",
            model_settings=ModelSettings(temperature=0.7),

            # Tracing configuration
            workflow_name="Support Chat",
            trace_id="trace_custom_123",
            group_id="session_456",
            trace_metadata={"environment": "production"},
            trace_include_sensitive_data=False,

            # Input processing
            call_model_input_filter=trim_history,
        ),
        error_handlers={"max_turns": handle_max_turns},
    )

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

## Summary

The OpenAI Agents SDK provides a complete framework for building sophisticated multi-agent AI applications. Its core strengths lie in the seamless integration of tools, handoffs, and guardrails within a Python-first design philosophy. Developers can create agents that range from simple single-turn assistants to complex multi-agent systems with specialized roles, human approval workflows, and persistent conversation memory. The SDK's built-in tracing capabilities enable comprehensive debugging and monitoring in both development and production environments.

Key integration patterns include: orchestrator agents that delegate to specialized sub-agents via tools, triage systems using handoffs for dynamic conversation routing, guardrails for safety-critical applications, MCP servers for external tool integration, and sessions for stateful conversations. The SDK's flexibility in supporting multiple LLM providers through LiteLLM, combined with its extensible session and tracing systems, makes it suitable for enterprise deployments while maintaining simplicity for rapid prototyping. Whether building customer support bots, research assistants, or complex workflow automation, the Agents SDK provides the primitives needed to create reliable, observable, and maintainable AI agent systems.
