#!/usr/bin/env python
"""
Example from the README for LLMsTxt Architect.
"""

import asyncio
from llmstxt_architect.main import generate_llms_txt

async def run_example():
    """Run the example from the README."""
    # For testing purposes, use fake provider to avoid API calls
    urls = [
        "https://langchain-ai.github.io/langgraph/concepts/",
        "https://langchain-ai.github.io/langgraph/how-tos/"
    ]
    
    project_dir = "langgraph_docs"
    
    print(f"Running example with:\n- URLs: {urls}\n- Project dir: {project_dir}")
    
    try:
        await generate_llms_txt(
            urls=urls,
            max_depth=1,
            llm_name="fake-model",  # Use fake model to avoid real API calls
            llm_provider="fake",  # Use fake provider to avoid real API calls
            project_dir=project_dir,
            output_dir="summaries",
            output_file="llms.txt"
        )
        print("Example completed successfully!")
    except Exception as e:
        print(f"Error (expected if using fake provider): {e}")
        # This is expected to fail with fake provider
    
    # Check if the project directory was created
    import os
    if os.path.exists(project_dir):
        print(f"Project directory '{project_dir}' was created successfully!")
        print(f"Directory structure:")
        os.system(f"find {project_dir} -type d | sort")
    else:
        print(f"Project directory '{project_dir}' was not created.")

if __name__ == "__main__":
    asyncio.run(run_example())