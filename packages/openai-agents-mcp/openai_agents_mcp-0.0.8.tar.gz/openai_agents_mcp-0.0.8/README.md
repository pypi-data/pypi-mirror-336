# OpenAI Agents SDK - MCP Extension

This package extends the [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) to add support for Model Context Protocol (MCP) servers. With this extension, you can seamlessly use MCP servers and their tools with the OpenAI Agents SDK.

The project is built using the [mcp-agent](https://github.com/lastmile-ai/mcp-agent) library.

<p align="center">
<a href="https://pypi.org/project/openai-agents-mcp/"><img src="https://img.shields.io/pypi/v/openai-agents-mcp?color=%2334D058&label=pypi" /></a>
<a href="https://github.com/lastmile-ai/openai-agents-mcp/issues"><img src="https://img.shields.io/github/issues-raw/lastmile-ai/openai-agents-mcp" /></a>
<a href="https://lmai.link/discord/mcp-agent"><img src="https://shields.io/discord/1089284610329952357" alt="discord" /></a>
<img alt="Pepy Total Downloads" src="https://img.shields.io/pepy/dt/openai-agents-mcp?label=pypi%20%7C%20downloads"/>
<a href="https://github.com/lastmile-ai/openai-agents-mcp/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/openai-agents-mcp" /></a>
</p>

## Features

- Connect OpenAI Agents to MCP servers
- Access tools from MCP servers alongside native OpenAI Agent SDK tools
- Configure MCP servers via standard configuration files
- Automatic tool discovery and conversion from MCP to Agent SDK format

## Installation

```bash
uv add openai-agents-mcp
```

```bash
pip install openai-agents-mcp
```

## Quick Start

> [!TIP]
> The [`examples`](/examples) directory has several example applications to get started with.
> To run an example, clone this repo, then:
>
> ```bash
> cd examples
> cp mcp_agent.secrets.yaml.example mcp_agent.secrets.yaml # Update API keys if needed
> uv run hello_world_mcp.py # Or any other example
> ```


In order to use Agents SDK with MCP, simply replace the following import:

```diff
- from agents import Agent
+ from agents_mcp import Agent
```

With that you can instantiate an Agent with `mcp_servers` in addition to `tools` (which continue to work like before).

```python
    from agents_mcp import Agent

    # Create an agent with specific MCP servers you want to use
    # These must be defined in your mcp_agent.config.yaml file
    agent = Agent(
        name="MCP Agent",
        instructions="""You are a helpful assistant with access to both local/OpenAI tools and tools from MCP servers. Use these tools to help the user.""",
        # Local/OpenAI tools
        tools=[get_current_weather],
        # Specify which MCP servers to use
        # These must be defined in your mcp_agent config
        mcp_servers=["fetch", "filesystem"],
    )
```

Then define an `mcp_agent.config.yaml`, with the MCP server configuration:

```yaml
mcp:
  servers:
    fetch:
      command: npx
      args: ["-y", "@modelcontextprotocol/server-fetch"]
    filesystem:
      command: npx
      args: ["-y", "@modelcontextprotocol/server-filesystem", "."]
```

**That's it**! The rest of the Agents SDK works exactly as before.

Head over to the [examples](./examples) directory to see MCP servers in action with Agents SDK.

### Demo

https://github.com/user-attachments/assets/1d2a843d-2f99-41f2-8671-4c7940ec48f5

More details and nuances below.

## Using MCP servers in Agents SDK

#### `mcp_servers` property on Agent

You can specify the names of MCP servers to give an Agent access to by
setting its `mcp_servers` property.

The Agent will then automatically aggregate tools from the servers, as well as 
any `tools` specified, and create a single extended list of tools. This means you can seamlessly 
use local tools, MCP servers, and other kinds of Agent SDK tools through a single unified syntax.

```python

agent = Agent(
    name="MCP Assistant",
    instructions="You are a helpful assistant with access to MCP tools.",
    tools=[your_other_tools], # Regular tool use for Agent SDK
    mcp_servers=["fetch", "filesystem"]  # Names of MCP servers from your config file (see below)
)
```

#### MCP Configuration File

Configure MCP servers by creating an `mcp_agent.config.yaml` file. You can place this file in your project directory or any parent directory. 

Here's an example configuration file that defines three MCP servers:

```yaml
$schema: "https://raw.githubusercontent.com/lastmile-ai/mcp-agent/main/schema/mcp-agent.config.schema.json"

mcp:
  servers:
    fetch:
      command: "uvx"
      args: ["mcp-server-fetch"]
    filesystem:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-filesystem", "."]
    slack:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-slack"]
```

For servers that require sensitive information like API keys, you can:
1. Define them directly in the config file (not recommended for production)
2. Use a separate `mcp_agent.secrets.yaml` file (more secure)
3. Set them as environment variables

### Methods for Configuring MCP

This extension supports several ways to configure MCP servers:

#### 1. Automatic Discovery (Recommended)

The simplest approach lets the SDK automatically find your configuration file if it's named `mcp_agent.config.yaml` and `mcp_agent.secrets.yaml`:

```python
from agents_mcp import Agent, RunnerContext

# Create an agent that references MCP servers
agent = Agent(
    name="MCP Assistant",
    instructions="You are a helpful assistant with access to MCP tools.",
    mcp_servers=["fetch", "filesystem"]  # Names of servers from your config file
)

result = await Runner.run(agent, input="Hello world", context=RunnerContext())
```

#### 2. Explicit Config Path

You can explicitly specify the path to your config file:

```python
from agents_mcp import RunnerContext

context = RunnerContext(mcp_config_path="/path/to/mcp_agent.config.yaml")
```

#### 3. Programmatic Configuration

You can programmatically define your MCP settings:

```python
from mcp_agent.config import MCPSettings, MCPServerSettings
from agents_mcp import RunnerContext

# Define MCP config programmatically
mcp_config = MCPSettings(
    servers={
        "fetch": MCPServerSettings(
            command="uvx",
            args=["mcp-server-fetch"]
        ),
        "filesystem": MCPServerSettings(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", "."]
        )
    }
)

context = RunnerContext(mcp_config=mcp_config)
```

#### 4. Custom Server Registry

You can create and configure your own MCP server registry:

```python
from mcp_agent.mcp_server_registry import ServerRegistry
from mcp_agent.config import get_settings

from agents_mcp import Agent

# Create a custom server registry
settings = get_settings("/path/to/config.yaml")
server_registry = ServerRegistry(config=settings)

# Create an agent with this registry
agent = Agent(
    name="Custom Registry Agent",
    instructions="You have access to custom MCP servers.",
    mcp_servers=["fetch", "filesystem"],
    mcp_server_registry=server_registry  # Use custom registry
)
```

### Examples

#### Basic Hello World

A simple example demonstrating how to create an agent that uses MCP tools:

```python
from agents_mcp import Agent, RunnerContext

# Create an agent with MCP servers
agent = Agent(
    name="MCP Assistant",
    instructions="You are a helpful assistant with access to tools.",
    tools=[get_current_weather],  # Local tools
    mcp_servers=["fetch", "filesystem"],  # MCP servers
)

# Run the agent
result = await Runner.run(
    agent,
    input="What's the weather in Miami? Also, can you fetch the OpenAI website?",
    context=RunnerContext(),
)

print(result.response.value)
```

See [hello_world_mcp.py](examples/hello_world_mcp.py) for the complete example.

#### Streaming Responses

To stream responses instead of waiting for the complete result:

```python
result = Runner.run_streamed(  # Note: No await here
    agent,
    input="Print the first paragraph of https://openai.github.io/openai-agents-python/",
    context=context,
)

# Stream the events
async for event in result.stream_events():
    if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
        print(event.data.delta, end="", flush=True)
```

See [hello_world_mcp_streamed.py](examples/hello_world_mcp_streamed.py) for the complete example.

## Acknowledgements

This project is made possible thanks to the following projects:

-   [uv](https://github.com/astral-sh/uv) and [ruff](https://github.com/astral-sh/ruff)
-   [MCP](https://modelcontextprotocol.io/introduction) (Model Context Protocol)
-   [mcp-agent](https://github.com/lastmile-ai/mcp-agent)

## License

MIT