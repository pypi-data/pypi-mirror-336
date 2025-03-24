import yaml
import pkg_resources
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Creditsafe Finix App")

def load_yaml_config(file_name: str = "portfolios-api.yaml") -> dict:
    """Load configuration from a YAML file bundled with the package."""
    print(f"Loading configuration from {file_name}")
    try:
        # Access the YAML file within the package using pkg_resources
        resource_package = __name__  # Use the current package name
        resource_path = pkg_resources.resource_filename(resource_package, file_name)
        
        with open(resource_path, "r", encoding="utf-8") as file:
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
    main()
