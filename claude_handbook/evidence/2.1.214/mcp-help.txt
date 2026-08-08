Usage: claude mcp [options] [command]

Configure and manage MCP servers

Options:
  -h, --help                            Display help for command

Commands:
  add [options] <name> <commandOrUrl> [args...]  Add an MCP server to Claude Code.

  Examples:
    # Add HTTP server:
    claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

    # Add HTTP server with headers:
    claude mcp add --transport http corridor https://app.corridor.dev/api/mcp --header "Authorization: Bearer ..."

    # Add stdio server with environment variables:
    claude mcp add my-server -e API_KEY=xxx -- npx my-mcp-server

    # Add stdio server with subprocess flags:
    claude mcp add my-server -- my-command --some-flag arg1
  add-from-claude-desktop [options]     Import MCP servers from Claude Desktop
                                        (Mac and WSL only)
  add-json [options] <name> <json>      Add an MCP server (stdio or SSE) with a
                                        JSON string
  get <name>                            Get details about an MCP server.
                                        Unapproved .mcp.json servers are shown
                                        as ⏸ Pending approval and not connected
                                        to; approved servers are health-checked.
  help [command]                        display help for command
  list                                  List configured MCP servers. Unapproved
                                        .mcp.json servers are shown as ⏸ Pending
                                        approval and not connected to; approved
                                        servers are health-checked.
  login [options] <name>                Authenticate with an MCP server (HTTP,
                                        SSE, or claude.ai connector)
  logout <name>                         Clear stored OAuth credentials for an
                                        MCP server
  remove [options] <name>               Remove an MCP server
  reset-project-choices                 Reset all approved and rejected
                                        project-scoped (.mcp.json) servers
                                        within this project
  serve [options]                       Start the Claude Code MCP server
