#!/usr/bin/env python3
import json
import os
import sys
import argparse
import asyncio
import time
import csv
import math

# interactive imports
from langchain_aws import ChatBedrock
from mcp.client.stdio import stdio_client
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from langchain_mcp_adapters.tools import load_mcp_tools
# your globals
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir  = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from globals import *
# for benchmark mode
from math_env import load_tasks
from eval_functions.benchmark_utils import run_single, write_summary

def parse_args():
    p = argparse.ArgumentParser(description="Math MCP Client + Benchmark")
    p.add_argument("--model-id",
                   default=os.getenv("BEDROCK_MODEL_ID", BEDROCK_AMAZON_NOVA_LITE),
                   help="Bedrock model ID")
    p.add_argument("--python-path",
                   default=sys.executable,
                   help="Python executable for launching MCP server")
    p.add_argument("--benchmark",
                   action="store_true",
                   help="Run in batch benchmark mode (no interactive)")
    p.add_argument("--output",
                   default="results.csv",
                   help="CSV file to write benchmark results")
    p.add_argument("--recursions", type=int, default=25,
                   help="Maximum agent recursion depth before aborting")
    return p.parse_args()

async def main():
    args = parse_args()

    # build few-shot prefix + system_prompt
    SYS_PROMPT_RESPONSE_FORMAT: str = """
    You are an analytical agent who answers user questions directly. Always 
    answer the user question directly, without any pre-filler words. Use the few
    shot examples in the prompt as reference for the response format.
    """
    combined_system_prompt: str = ""
    few_shot = json.load(open(os.path.join(parent_dir, FEW_SHOT_FPATH)))
    fewshot_prefix = "\n\n".join(ex["messages_display"] for ex in few_shot)
    # 3. Prepend this to your system prompt
    combined_system_prompt = fewshot_prefix + "\n" + combined_system_prompt
    system_prompt = fewshot_prefix + "\n\n" + combined_system_prompt

    # prepare MCP stdio transport
    params = StdioServerParameters(
        command=args.python_path,
        args=[os.path.join(parent_dir, MATH_MCP_SERVER_FPATH)]
    )

    # single async-with for both stdio_client and ClientSession
    async with stdio_client(params) as (reader, writer), \
               ClientSession(reader, writer) as session:

        await session.initialize()
        tools = await load_mcp_tools(session)

        # agent setup
        llm   = ChatBedrock(model_id=args.model_id)
        agent = create_react_agent(llm, 
                                   tools, 
                                   prompt=system_prompt)
        if args.benchmark:
            tasks   = load_tasks()
            results = []

            for task in tasks:
                row = await run_single(task, agent, system_prompt)
                results.append(row)
                print(f"[{task['id']}] {task['question']} → {row['result']} ({'OK' if row['correct_ans'] else 'ERR'})")

            # write CSV
            with open(args.output, "w", newline="") as f:
                writer_csv = csv.DictWriter(f, fieldnames=list(results[0].keys()))
                writer_csv.writeheader()
                writer_csv.writerows(results)

            print(f"\nBenchmark complete: wrote {len(results)} rows to {args.output}")

            # also write a summary
            summary = write_summary(results, summary_path="benchmark_summary.txt")
            print("Summary written to benchmark_summary.txt")

        else:
            # --- INTERACTIVE MODE ---
            print("Entering interactive REPL (type quit or exit to stop)\n" + "-"*50)
            while True:
                q = input(">>> ").strip()
                if q.lower() in ("quit", "exit"):
                    print("Goodbye!")
                    break
                resp = await agent.ainvoke({"messages":[{"role":"user","content":q}]})
                msgs = resp["messages"]
                if not msgs:
                    print("[no content returned]")
                else:
                    print(msgs[-1].content)

if __name__ == "__main__":
    asyncio.run(main())
