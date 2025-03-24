import yaml
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Creditsafe Finix App")


URL = "https://finix-dev.s3.eu-central-1.amazonaws.com/portfolios-api.yaml?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEID%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDGV1LWNlbnRyYWwtMSJHMEUCID28InhYnzK8ZuuRbaMZ58wRG6rVIMpvEt25sqMPoyJyAiEAyN7wRih1Dc72WgvKs9wmE%2Ff55LBAfr0E%2B13FMOLBjfcqpAQI2f%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARACGgw2MDU1MDk1MDk1MjAiDODxyqE0OMvyAFXDNyr4Azv%2FtQZyQFoYcQGTl62DoDZCUQxnHQsjAcCJHSimUL8ldTs0H9wNmBBIsVYaGXDRyraBWB%2B9wCKHB0P5U%2BFT1xhTtKi4u4c0uPvi%2Bwlk0mmcNlJRIko2MAFJPgv7auxk%2B72W0moO5WH50iuns8v%2BVWhofypIPm8j3w07xPHeKM22cveVtP7HQT91p%2FaqVMGfpEPrBbwmOu%2FD8Czl3ZluNcrmqGx0b61KU9hjmVqzKV1XfemktZv82D7wh8oEu7m4Watq1yLNvh5nS32Sj0wofcJq9Z1RapiKWV4uSZIPmtxWSfF4lPn5gIijwnq27wETIGghsFaFsb%2BtDbxRQlmlcg%2FFtiMqfmEg33bxngPdUfC6AIhlxql6potDyxa1T5bbYnoGDKIzw7S278bXtyIT0T5ydmiu0jtzQCuQKtgFihSFO8NqcuwD1pvxmuhfL8q8rseY4zXrbMvR8ZoxuxLWXO7CXWYZRqfV4zTEK65OajL5lclXDB5XfIbh3A6bj4rHmKMEFGH39UQIHz932M4kKBIXaqBTa5fEZcwhpqXN85ZekH8MuQDbheDSaDovgvXK9uFYGfhd9sVpRYH7gnQR31t6JMpYSK0HBRKdLFspYUjzhslo0jZ0F2gTVOzKXzmlXlMsz0cf8ZkkC1Zy3T3HOWRBYoDDWn9N0TDk6IC%2FBjq9AkD%2BkrpleN%2FPsdt82xzp%2FnnbN5sxjAlT4KgATjwhB%2BBTI%2FKuHy2pmg70N4OP3%2F3RR%2FR87q72gbdzk6vTJTlQLofAHLnHJyaLHC%2F1wr%2FEGOR8MCy0z7zsMfUgg07w7xj17sbdRxXhVlqg3mDhUdG59bJ1LWx6k9i%2B2SbRGocC%2BUJvLL%2Fu8j6Gt9HaCcFP7LTgx%2FK3Z5Yx2SLneGtiqGcr9sUPj6QXR23VvdNmOzzqMQNcUXOH416DMMyKUGu8PT45CYvI%2FxkW%2BEiWdkQWzw2VIsCfdrEUjiJ3eQpzeZ8k7bItwq7ixdJ7%2FyODmTK1INQ9lq0g1zBd0IpkXqpgPqpduQLbqXZhVFpZiV%2FcEIqz4iA3R2gV7ROwxswxI2Mt2x10K%2FUDbjWGXIPVA36ltWIVx%2F1pFx7UiCtMuhchJToM&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAYZ6ZN4GIN5O2CVPF%2F20250323%2Feu-central-1%2Fs3%2Faws4_request&X-Amz-Date=20250323T161945Z&X-Amz-Expires=7200&X-Amz-SignedHeaders=host&X-Amz-Signature=0d3739c82d813b9beb41890e94bf1216081ed59e7e28d87531e95b88b50775e8"

def load_yaml_config(url: str = URL) -> dict:
    """Load configuration from a YAML file hosted on a URL."""
    print(f"Fetching configuration from {url}")
    try:
        response = requests.get(url, timeout=30)  # Set timeout for reliability
        response.raise_for_status()  # Raise error for HTTP issues
        return yaml.safe_load(response.text)  # Parse YAML content
    except requests.RequestException as e:
        print(f"Error fetching YAML: {e}")
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
