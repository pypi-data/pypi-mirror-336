from mcp.server import FastMCP

from arcanna_mcp_input_server.tools import attach_tools

from arcanna_mcp_input_server.environment import TRANSPORT_MODE

mcp = FastMCP("arcanna_mcp_input_server")

attach_tools(mcp)


def main():
    # Initialize and run the server
    mcp.run(transport=TRANSPORT_MODE)


if __name__ == '__main__':
    main()
