#!/usr/bin/env python
"""
Test script for the LLMsTxt Architect Python API.
"""

import asyncio
import os
from llmstxt_architect.main import generate_llms_txt

async def test_api():
    """Test the LLMsTxt Architect Python API."""
    # For testing purposes, using fake provider to avoid API calls
    urls = [
        "https://langchain-ai.github.io/langgraph/concepts/",
    ]
    
    project_dir = "api_test"
    
    print(f"Testing LLMsTxt Architect API with project directory: {project_dir}")
    print(f"URLs: {urls}")
    
    try:
        await generate_llms_txt(
            urls=urls,
            max_depth=1,
            llm_name="fake-model",
            llm_provider="fake", 
            project_dir=project_dir,
            output_dir="summaries",
            output_file="llms.txt"
        )
        print("API call completed")
    except Exception as e:
        print(f"Error (expected if using fake provider): {e}")
        # This is expected to fail with fake provider
    
    # Check if the project directory was created
    if os.path.exists(project_dir):
        print(f"Project directory '{project_dir}' was created successfully!")
    else:
        print(f"Project directory '{project_dir}' was not created.")

if __name__ == "__main__":
    asyncio.run(test_api())