from mcp.server import FastMCP
import arcanna_mcp_input_server.tools.jobs
import arcanna_mcp_input_server.tools.events
import arcanna_mcp_input_server.tools.health_check


def attach_tools(mcp_server: FastMCP):
    modules = [
        arcanna_mcp_input_server.tools.jobs,
        arcanna_mcp_input_server.tools.events,
        arcanna_mcp_input_server.tools.health_check,
    ]
    for module in modules:
        for tool_fn in module.export_tools():
            mcp_server.add_tool(tool_fn)
