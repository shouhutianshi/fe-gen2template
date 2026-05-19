# MCP 安装

```bash
# YApi 接口文档
claude mcp add yapi --transport http \
  https://mcp-gateway.zuoyebang.cc/mcp/yapi \
  --header 'Cookie: ZYBIPSCAS=${ANTHROPIC_AUTH_TOKEN}'

# 自动部署
claude mcp add inf-autodeploy --transport http \
  https://mcp-gateway.zuoyebang.cc/mcp/inf-autodeploy \
  --header 'Cookie: ZYBIPSCAS=${ANTHROPIC_AUTH_TOKEN}'
```
