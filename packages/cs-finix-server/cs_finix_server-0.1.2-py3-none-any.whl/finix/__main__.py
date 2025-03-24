import yaml
import importlib.resources as resources
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Creditsafe Finix App")

def load_yaml_config(file_name: str = "portfolios-api.yaml") -> dict:
    """Load configuration from a YAML file bundled with the package."""
    print(f"Loading configuration from {file_name}")
    try:
        with resources.open_text("finix", file_name) as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
        return {}
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return {}

@mcp.tool()
def get_api_docs(name: str) -> str:
    print(f"Getting API docs for {name}")
    return load_yaml_config("portfolios-api.yaml")

def main():
    """Start the Creditsafe Finix MCP server"""
    print("Starting Creditsafe Finix MCP Server...")
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
