"""Posto MCP Server - Social Media Tools for LLM AI."""

# Import compiled module
try:
    from posto_mcp import main
except ImportError:
    # Fallback for development or when compiled module is not available
    def main():
        """Main entry point for the package."""
        print("Warning: Using development version without compiled module.")
        # Import the original module for development
        try:
            from posto_sdk.posto_mcp import run_server
            import asyncio
            asyncio.run(run_server())
        except ImportError:
            print("Error: Could not import posto_sdk.posto_mcp. Please install posto-sdk.")
            return 1
        return 0

__version__ = "0.1.0"

if __name__ == "__main__":
    main() 