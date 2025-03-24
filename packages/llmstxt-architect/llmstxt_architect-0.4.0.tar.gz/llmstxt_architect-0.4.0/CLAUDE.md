# LLMSTXT ARCHITECT DEVELOPMENT GUIDE

## Commands
- **Setup (pip)**: `python -m venv venv && source venv/bin/activate && pip install -e ".[dev]"`
- **Setup (uv)**: `uv venv && source .venv/bin/activate && uv pip install -e ".[dev]"`
- **Run with uvx**: `uvx --with-editable . llmstxt-architect --urls https://example.com`
- **Format**: `black . && isort .`
- **Lint**: `ruff check .`
- **Type Check**: `mypy llmstxt_architect`
- **Test All**: `pytest`
- **Test Single**: `pytest tests/test_file.py::test_function -v`

## Code Style
- **Imports**: Group standard lib, third-party, local imports separated by lines
- **Naming**: snake_case for variables/functions, PascalCase for classes
- **Types**: All functions require type annotations (enforced by mypy)
- **Docstrings**: Required for all functions with descriptions, args, returns
- **Error Handling**: Use try/except blocks with specific exceptions
- **Async**: Utilize async/await for network operations when possible
- **Max Line Length**: 88 characters (enforced by black)
- **File Structure**: Keep modules focused, maintain separation of concerns
- **Log Format**: Use structured logging with appropriate levels