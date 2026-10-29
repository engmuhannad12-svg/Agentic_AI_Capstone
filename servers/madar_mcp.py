"""Madar MCP server for the Rafeeq demo."""
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Madar Municipal Services")


@mcp.tool()
def permit_requirements(permit_type: str) -> dict:
    """Return demo requirements for a municipal permit."""
    return {
        "permit_type": permit_type,
        "required_documents": [
            "Applicant ID",
            "Property ownership or lease proof",
            "Site plan",
        ],
        "notice": "Demo data only. Verify actual requirements with the municipality.",
    }


@mcp.tool()
def service_information() -> dict:
    """Describe the bilingual municipal assistant."""
    return {
        "service": "Rafeeq",
        "languages": ["Arabic", "English"],
        "scope": "Demonstration municipal permit assistance",
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
