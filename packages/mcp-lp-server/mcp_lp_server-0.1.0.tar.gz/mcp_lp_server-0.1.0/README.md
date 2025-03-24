## Generate protobuf python code
protoc --python_out=codegens \
    --pyi_out=codegens \
    --proto_path=/Users/keren/Gravity/GSProtoBuf/Proto \
    --proto_path=/Users/keren/Gravity/mcp-lp-server/proto \
    /Users/keren/Gravity/mcp-lp-server/proto/gs-options.proto \
    $(find /Users/keren/Gravity/GSProtoBuf/Proto -name "*.proto")

## Find virtual environment source code path
`python -c "import site; print(site.getsitepackages())"`

## Setup MCP server pointing to the src folder directly
`{
  "mcpServers": {
    "gsweb": {
        "command": "uv",
        "args": [
            "--directory",
            "/Users/keren/Gravity/mcp-lp-server",
            "run",
            "main.py"
        ]
    }
  }
}
`

## CI/CD
Build: `uv build`
Publish: `uv pip install .`
Validate: `uv pip list | grep mcp-lp-server`