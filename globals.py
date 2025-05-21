# Represents the global variables that will be used across the files for benchmarking agents
import os

# Represents the path where the historical trajectories of the agent resides
HISTORICAL_TRAJECTORY_DIRNAME: str = "historical_trajectories"
# Represents the file names that contain the trajectory data
SONNET_TRAJECTORY_FNAME: str = "sonnet-35-new-math.json"
# Represents the full path to the trajectory data
HISTORICAL_TRAJECTORY_FPATH: str = os.path.join(HISTORICAL_TRAJECTORY_DIRNAME, SONNET_TRAJECTORY_FNAME)

# Represents the path where the few shot data of the agent resides that will be used in the
# prompt that is sent to the agent in the client code
HISTORICAL_FEW_SHOT_DIRNAME: str = "few_shot_data"
# Represents the file names that contain the few shot examples
SONNET_FEW_SHOT_FNAME: str = "mock_math_server_messages.jsonl"
# Represents the full path to the few shot messages that will be inserted into the agent
# system prompt to better understand which tool to call from the MCP server
FEW_SHOT_FPATH: str = os.path.join(HISTORICAL_FEW_SHOT_DIRNAME, SONNET_FEW_SHOT_FNAME)

# Represents the server directory
SERVER_DIR: str = "servers"
# Represents the local math MCP server
MATH_MCP_SERVER_FNAME: str = "math_mcp_server.py"
# Represents the math MCP server fpath
MATH_MCP_SERVER_FPATH: str = os.path.join(SERVER_DIR, MATH_MCP_SERVER_FNAME)


# ----------------------------
# MODEL ID GLOBAL VARS
# ----------------------------
# Represents the model ids that are used within the different agents as default
# Using the cross region inference model id 

# Anthropic's most advanced hybrid reasoning model, offering both standard 
# and extended thinking modes for complex problem-solving. 
BEDROCK_CLAUDE_3_7_SONNET: str = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
# A fast and efficient model, ideal for tasks requiring quick responses with improved reasoning capabilities.
BEDROCK_CLAUDE_3_5_HAIKU: str = "us.anthropic.claude-3-5-haiku-20241022-v1:0"
# A low-cost, multimodal model capable of processing text, images, and videos, 
# suitable for real-time customer interactions and document analysis.
BEDROCK_AMAZON_NOVA_LITE: str = "us.amazon.nova-lite-v1:0"
# text-only model optimized for speed and cost, delivering low-latency 
# responses for tasks like text summarization and translation.
BEDROCK_AMAZON_NOVA_MICRO: str = "us.amazon.nova-micro-v1:0"

# ----------------------------
# Results files
# ----------------------------
RESULTS_DIR: str = "results"
# LangGraph local math MCP results
RESULTS_RAW_FNAME_LANGGRAPH_MATH_MCP: str = "math_results_raw.csv"
LANGGRAPH_MATH_MCP_RESULTS_FPATH: str = os.path.join(RESULTS_DIR, RESULTS_RAW_FNAME_LANGGRAPH_MATH_MCP)
