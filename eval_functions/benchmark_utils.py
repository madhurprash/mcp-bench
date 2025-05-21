# eval/benchmark_utils.py

import time
import json
import math
from langchain_core.messages import ToolMessage
from langgraph.errors import GraphRecursionError
from botocore.exceptions import BotoCoreError, ClientError  # for Bedrock errors

async def run_single(task, agent, system_prompt, recursion_limit=None):
    """
    Run one task through the agent, print logs, and return a result dict.
    Catches and logs any ModelErrorException or other invocation errors.
    """
    print(f"▶ Task {task['id']}: {task['question']}")
    start = time.perf_counter()
    try:
        # pass recursion_limit if provided
        invoke_kwargs = {"messages": [
                             {"role": "system", "content": system_prompt},
                             {"role": "user",   "content": task["question"]}
                         ]}
        config = {}
        if recursion_limit is not None:
            config["recursion_limit"] = recursion_limit

        resp = await agent.ainvoke(invoke_kwargs, config or None)

    except (ClientError, BotoCoreError) as e:
        # catches ModelErrorException and other AWS/Bedrock errors
        elapsed = time.perf_counter() - start
        err_text = f"{type(e).__name__}: {str(e)}"
        print(f"--> ⛔ Model/Tool error after {elapsed:.3f}s: {err_text}")
        print("-" * 60)
        return {
            "id":                      task["id"],
            "question":                task["question"],
            "used_tool":               None,
            "tool_ground_truth":       task["tool"],
            "tool_selection_accuracy": False,
            "args":                    None,
            "result":                  None,
            "expected":                task["expected"],
            "correct_ans":             False,
            "latency":                 round(elapsed, 3),
            "input_tokens":            None,
            "output_tokens":           None,
            "total_tokens":            None,
            "error":                   err_text
        }

    except GraphRecursionError as e:
        # recursion limit hit
        elapsed = time.perf_counter() - start
        err_text = f"GraphRecursionError: {str(e)}"
        print(f"--> ⛔ Recursion error after {elapsed:.3f}s: {err_text}")
        print("-" * 60)
        return {
            "id":                      task["id"],
            "question":                task["question"],
            "used_tool":               None,
            "tool_ground_truth":       task["tool"],
            "tool_selection_accuracy": False,
            "args":                    None,
            "result":                  None,
            "expected":                task["expected"],
            "correct_ans":             False,
            "latency":                 round(elapsed, 3),
            "input_tokens":            None,
            "output_tokens":           None,
            "total_tokens":            None,
            "error":                   err_text
        }

    # normal path
    latency = time.perf_counter() - start
    print(f"--> Latency: {latency:.3f}s")

    # 1) extract tool call
    tool_calls = resp.get("tool_calls") if isinstance(resp, dict) else None
    if not tool_calls:
        for msg in resp["messages"]:
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                tool_calls = msg.tool_calls
                break

    if tool_calls:
        last = tool_calls[-1]
        used_tool, args = last["name"], last["args"]
        print(f"--> Tool call: {used_tool}({args})")
    else:
        used_tool, args = None, None
        print("--> No tool call detected")

    # 2) extract the tool’s output
    result = None
    for msg in resp["messages"]:
        if isinstance(msg, ToolMessage):
            text = msg.content.strip()
            try:
                result = json.loads(text)
            except json.JSONDecodeError:
                result = text
            break
    print(f"--> Raw tool result: {result}")

    # 3) get LLM usage
    usage    = resp.get("usage_metadata", {})
    input_t  = usage.get("input_tokens")
    output_t = usage.get("output_tokens")
    total_t  = usage.get("total_tokens")
    print(f"--> Tokens: input={input_t}, output={output_t}, total={total_t}")

    # 4) correctness
    expected = task["expected"]
    if isinstance(expected, float) and isinstance(result, (int, float)):
        correct_ans = math.isclose(result, expected, rel_tol=1e-6, abs_tol=1e-6)
    else:
        correct_ans = (result == expected)

    status = "✅ PASS" if correct_ans else "❌ FAIL"
    print(f"--> Expected: {expected} → {status}\n" + "-"*60)

    return {
        "id":                      task["id"],
        "question":                task["question"],
        "used_tool":               used_tool,
        "tool_ground_truth":       task["tool"],
        "tool_selection_accuracy": (used_tool == task["tool"]),
        "args":                    args,
        "result":                  result,
        "expected":                expected,
        "correct_ans":             correct_ans,
        "latency":                 round(latency, 3),
        "input_tokens":            input_t,
        "output_tokens":           output_t,
        "total_tokens":            total_t,
        "error":                   ""   # no error
    }

def write_summary(results, summary_path="benchmark_summary.txt"):
    """
    Compute averages & accuracies across all results
    and write a simple human‐readable summary file.
    """
    n = len(results)
    latencies = [r["latency"] for r in results if r["latency"] is not None]
    in_toks    = [r["input_tokens"] for r in results if isinstance(r.get("input_tokens"), (int, float))]
    out_toks   = [r["output_tokens"] for r in results if isinstance(r.get("output_tokens"), (int, float))]
    tot_toks   = [r["total_tokens"] for r in results if isinstance(r.get("total_tokens"), (int, float))]
    tool_accs  = [1 if r["tool_selection_accuracy"] else 0 for r in results]
    ans_accs   = [1 if r["correct_ans"]             else 0 for r in results]

    summary = {
        "total_tasks":               n,
        "avg_latency_s":             (sum(latencies)/len(latencies)) if latencies else None,
        "avg_input_tokens":          (sum(in_toks)/len(in_toks))       if in_toks    else None,
        "avg_output_tokens":         (sum(out_toks)/len(out_toks))     if out_toks   else None,
        "avg_total_tokens":          (sum(tot_toks)/len(tot_toks))     if tot_toks   else None,
        "tool_selection_accuracy":   (sum(tool_accs)/n)                if n           else None,
        "answer_accuracy":           (sum(ans_accs)/n)                 if n           else None,
    }

    with open(summary_path, "w") as sf:
        sf.write("MCPBench Summary\n")
        sf.write("----------------\n")
        for key, val in summary.items():
            label = key.replace("_", " ").title()
            sf.write(f"{label:25}: {val}\n")

    return summary
