# MCPBench: Benchmarking Math MCP Tool Selection

MCPBench is a lightweight framework to benchmark AI agents’ tool-selection accuracy and end-to-end performance on a local MCP math server. It leverages:

- A simple **MCP** math server (`math_mcp_server.py`) exposing basic arithmetic tools.  
- A **LangGraph**-based React-style agent (`langgraph_local_mcp_client.py`) using Bedrock or any Chat LLM.  
- A **benchmark mode** that runs a suite of math tasks, logs detailed metrics, and outputs a CSV summary.  

---

## 🛠 Prerequisites

1. **Install UV** (Astral’s CLI) and create a Python venv:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   export PATH="$HOME/.local/bin:$PATH"
   uv venv && source .venv/bin/activate && uv pip sync pyproject.toml
   export UV_PROJECT_ENVIRONMENT=.venv
   uv add zmq
   python -m ipykernel install --user --name=.venv --display-name="Python (uv env)"
   ```

2. **Set up AWS credentials** (if you plan to use Bedrock as your LLM):

   ```bash
   export AWS_PROFILE=your-aws-profile
   export AWS_REGION=us-west-2
   export BEDROCK_MODEL_ID=us.amazon.nova-lite-v1:0
   ```

## 📁 Project Structure

```text
mcp-bench/
├── agents/
│   ├── langgraph_local_mcp_client.py   # React-style client + benchmark driver
│   └── math_results.csv                # (auto-generated) benchmark output
├── servers/
│   └── math_mcp_server.py              # MCP math tool server
├── math_env/
│   └── tasks.json                      # Benchmark task definitions
├── few_shot_data/                      # Optional few-shot few-shot examples
├── globals.py                          # Paths & constants (e.g. server FPATHs)
├── pyproject.toml                      # Project dependencies
└── README.md                           # This file
```

## 🚀 Running the MCP Server

1. Open a terminal and navigate to the servers folder:

```bash
cd servers
```

2. Launch the math MCP server:

```bash
python math_mcp_server.py
```

The server will expose all @mcp.tool() functions (add, subtract, multiply, divide, etc.) over `stdio`.

## 🤖 Interactive Client Mode

1. In a new terminal, activate your `UV` `venv` and navigate to agents:

```bash
cd agents
```

2. Run the client in `REPL` mode:

```bash
uv run langgraph_local_mcp_client.py
```

3. Ask questions interactively:

```bash
>>> What is 7 + 8?
15
>>> Calculate 6 * 9
54
>>> quit
Goodbye!
```

## 📊 Benchmark Mode

To execute the full task suite and generate a CSV report:

```bash
uv run langgraph_local_mcp_client.py \
  --benchmark \
  --output math_results.csv \
  --model-id $BEDROCK_MODEL_ID \
  --recursions 30
```

- `--benchmark` → run in batch mode

- `--output` → path to write the CSV

- `--model-id` → specify any supported ChatLLM model

- `--recursions`→ adjust the agent’s graph recursion limit

Once done, open `agents/math_results.csv` to review:

### 📝 CSV Output Columns

| Column                    | Description                                                         |
|---------------------------|---------------------------------------------------------------------|
| `id`                      | Task identifier                                                     |
| `question`                | The natural-language math problem                                    |
| `used_tool`               | Name of the tool the agent invoked                                  |
| `tool_ground_truth`       | The correct tool that should have been called                       |
| `tool_selection_accuracy` | `true` if `used_tool == tool_ground_truth`, else `false`            |
| `args`                    | Dictionary of arguments passed to the tool                          |
| `result`                  | Raw output returned by the tool                                     |
| `expected`                | Gold-standard answer                                                |
| `correct_ans`             | `true` if `result == expected` (with float tolerance)               |
| `latency`                 | Round-trip time in seconds                                          |
| `input_tokens`            | Number of tokens in the prompt sent to the LLM                      |
| `output_tokens`           | Number of tokens in the LLM’s response                              |
| `total_tokens`            | Sum of input + output tokens                                        |
| `error`                   | Any error message if a call failed                                  |

---

### 🔧 Extending MCPBench

- **Add new tasks**: edit `math_env/tasks.json` (each entry needs `id`, `question`, `expected`, `tool`).  
- **Few-shot data**: place JSON examples in `few_shot_data/` and update `globals.py` to point `FEW_SHOT_FPATH`.  
- **Custom tools**: in `servers/math_mcp_server.py`, decorate new functions with `@mcp.tool()` and restart the server.  
- **Swap LLMs**: pass any `--model-id` supported by your provider (e.g. `gpt-4o`, `claude-3-7-sonnet`, `mistral-large-2407`).  

---

### 📄 License

This project is released under the **MIT License**. See [LICENSE](LICENSE) for details.
# mcp-bench
