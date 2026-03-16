from systems.react_agent import ReActAgents

agent = ReActAgents(
    model_name="llama-3.1-8b-instant",
    api_key="COMPLETE_RUN"
)

# test with one math question first
result = agent.run(
    "An employee earning $52,400 receives a 10% pay cut. "
    "The following year they get a 10% raise. "
    "What is their final salary?"
)

print("=== FINAL ANSWER ===")
print(result["final_answer"])
print("\n=== TRACE ===")
for i, entry in enumerate(result["trace"]):
    print(f"\nStep {i+1}")
    print(f"Thought: {entry['thought']}")
    print(f"Tool calls: {entry['tool_calls']}")