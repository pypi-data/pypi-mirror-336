# Agentrix

A powerful framework for creating AI agents, agent managers, and memory stores with LLM backends.

## Installation

```bash
pip install agentrix
```

## Features

### 🤖 Flexible Agent System
Create specialized agents with different capabilities:
- Single-purpose agents for specific tasks
- Multi-tool agents for complex operations
- Configurable system prompts and model settings
- Support for both OpenAI and Azure OpenAI endpoints

### 🧠 Memory Management
Built-in chat memory and Redis persistence options:
```python
# In-memory chat storage
memory = ChatMemory(max_messages=20)

# Redis-backed persistent storage
redis_memory = RedisMemory(
    redis_client=redis.Redis(),
    max_messages=50,
    ttl=86400  # 24-hour retention
)
```

### 🔄 Agent Orchestration
Manager agents to coordinate specialized sub-agents:
```python
# Create specialized agents
researcher = Agent("Researcher", "Research facts thoroughly", client)
analyst = Agent("Analyst", "Analyze data and insights", client)

# Create manager to coordinate them
manager = ManagerAgent(
    name="Manager",
    system_prompt="Coordinate agents to solve complex problems",
    llm=client,
    agents=[(researcher, "Research"), (analyst, "Analysis")],
    parallel=True  # Enable parallel execution
)
```

### 📄 JSON Parsing
Tools for structured data validation and extraction:
```python
class UserProfile(JsonModel):
    name = Field(str, required=True)
    age = Field(int, required=True)
    email = Field(str, required=False)

parser = JsonOutputParser(UserProfile)
validated_data = parser.parse(json_string)
```

### 🌐 Web Scraping
Integrated web browsing capabilities for research:
```python
# Create a web-enabled research agent
researcher = Agent(
    name="WebResearcher",
    system_prompt="Research assistant with web access",
    llm=client,
    tools=web_scraper_tools,
    memory=ChatMemory()
)

# Research with automatic web browsing
result = researcher.go("Latest developments in quantum computing")
```

## Key Benefits

- **Modular Design**: Mix and match components as needed
- **Persistent Memory**: Keep conversation context across sessions
- **Parallel Processing**: Run multiple agents simultaneously
- **Structured Output**: Validate and parse JSON responses
- **Web Integration**: Built-in tools for web research

## Usage 

```python
from agentrix import Tool, Agent, ManagerAgent
import openai

# Initialize OpenAI client
client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

# Create a simple tool
calculator_tool = Tool(
    name="calculator",
    description="Calculate a mathematical expression",
    function=lambda expression: eval(expression),
    inputs={"expression": ["string", "The math expression to evaluate"]}
)

# Create an agent with the tool
math_agent = Agent(
    name="MathAgent",
    system_prompt="You are a helpful mathematical assistant.",
    llm=client,
    tools=[calculator_tool],
    verbose=True
)

# Use the agent
result = math_agent.go("What is 25 squared plus 13?")
print(result)
```

## Creating a Manager Agent

```python
# Create specialized agents
researcher = Agent("Researcher", "You research facts thoroughly.", client)
analyst = Agent("Analyst", "You analyze data and provide insights.", client)

# Create a manager agent
manager = ManagerAgent(
    name="Manager",
    system_prompt="You coordinate multiple agents to solve complex problems.",
    llm=client,
    agents=[(researcher, "Use for researching facts"), (analyst, "Use for data analysis")],
    parallel=True,
    verbose=True
)

# Use the manager agent
result = manager.go("Research the population of France and analyze its growth trend.")
print(result)
```
Web Scraping Capabilities

```python
from agentrix import Agent, web_scraper_tools

# Create a research agent with web browsing capabilities
researcher = Agent(
    name="WebResearcher",
    system_prompt="""You are a research assistant that can browse the web.
Use the web browsing tools to find information and answer questions.
Always cite your sources with the URL.""",
    llm=client,
    tools=web_scraper_tools,
    verbose=True,
    memory=ChatMemory()
)

# Research a topic using web browsing
result = researcher.go("What are the latest developments in quantum computing?")
print(result)
```
Using Redis for Persistent Memory

```python 
import redis
from agentrix import Agent, RedisMemory

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Create Redis-backed memory
persistent_memory = RedisMemory(
    redis_client=redis_client,
    agent_id="unique-agent-id",  # Optional, will be auto-generated if not provided
    max_messages=50,
    ttl=86400  # 24 hour time-to-live
)

# Create agent with persistent memory
agent = Agent(
    name="PersistentAgent",
    system_prompt="You remember conversations even after restarts.",
    llm=client,
    verbose=True,
    memory=persistent_memory
)

# Conversations will persist across application restarts
```
JSON Structure Validation

```python
from agentrix import JsonModel, Field, JsonOutputParser

# Define a structured data model
class ProductInfo(JsonModel):
    name = Field(str, required=True)
    price = Field(float, required=True)
    description = Field(str, required=False, default="No description provided")
    in_stock = Field(bool, required=True)

# Create a parser for this model
parser = JsonOutputParser(ProductInfo)

# Use with an agent
def extract_product_info(text):
    try:
        # This will validate the data against the model
        product = parser.parse(text)
        return product.to_dict()
    except Exception as e:
        return f"Error parsing product info: {str(e)}"

# Create a tool for the agent
product_extractor_tool = Tool(
    name="extract_product",
    description="Extract structured product information from text",
    function=extract_product_info,
    inputs={"text": ["string", "Text containing product information"]}
)
```
Advanced: Creating Custom Tools

```python
from agentrix import Tool

# Define a function for the tool
def weather_lookup(location):
    # In a real app, this would call a weather API
    return f"The weather in {location} is currently sunny and 72°F"

# Create a tool from the function
weather_tool = Tool(
    name="weather_lookup",
    description="Look up the current weather for a location",
    function=weather_lookup,
    inputs={
        "location": ["string", "The city and state/country to get weather for"]
    }
)

# Add the tool to an agent
agent = Agent(
    name="WeatherAssistant",
    system_prompt="You provide weather information.",
    llm=client,
    tools=[weather_tool],
    memory=ChatMemory()
)
```
Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

License
This project is licensed under the MIT License - see the LICENSE file for details.