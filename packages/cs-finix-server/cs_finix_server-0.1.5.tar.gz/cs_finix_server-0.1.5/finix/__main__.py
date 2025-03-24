import yaml
import importlib.resources
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Creditsafe Finix App")


def load_yaml_config(file_name: str = "portfolios-api.yaml") -> dict:
    """Load configuration from a YAML file bundled with the package."""
    print(f"Loading configuration from {file_name}")
    try:
        # Access the YAML file within the package using importlib.resources
        package = "finix"  # The name of your package (e.g., "finix")
        
        # Read the file contents using importlib.resources
        file_path = importlib.resources.files(package) / file_name  # This gives you a Path object
        
        # Open and read the file content
        with file_path.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
            return config
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
    get_api_docs()
