import asyncio
from llmstxt_architect.main import generate_llms_txt

async def main():
      await generate_llms_txt(
          urls=["https://langchain-ai.github.io/langgraph/concepts"],
          max_depth=1,
          llm_name="claude-3-7-sonnet-latest",
          llm_provider="anthropic",
          project_dir="test_script",
      )

if __name__ == "__main__":
      asyncio.run(main())