# Cylestio Monitor

A comprehensive security and monitoring solution for AI agents. Cylestio Monitor provides lightweight, drop-in security monitoring for various frameworks, including Model Context Protocol (MCP) and popular LLM providers.

[![PyPI version](https://badge.fury.io/py/cylestio-monitor.svg)](https://badge.fury.io/py/cylestio-monitor)
[![CI](https://github.com/cylestio/cylestio-monitor/actions/workflows/ci.yml/badge.svg)](https://github.com/cylestio/cylestio-monitor/actions/workflows/ci.yml)
[![Security](https://github.com/cylestio/cylestio-monitor/actions/workflows/security.yml/badge.svg)](https://github.com/cylestio/cylestio-monitor/actions/workflows/security.yml)

## Overview

Cylestio Monitor is a Python SDK that provides security and monitoring capabilities for AI agents. While it works as a standalone solution, it integrates seamlessly with the Cylestio UI and smart dashboards for enhanced user experience and additional security and monitoring capabilities across your entire agentic workforce.

**For full documentation, visit [https://docs.cylestio.com](https://docs.cylestio.com)**

## Installation

```bash
pip install cylestio-monitor
```

### Installation for Example Projects

If you're using one of the example projects in a subdirectory with its own virtual environment:

```bash
# Navigate to the example directory 
cd examples/agents/your_agent_dir

# Activate your virtual environment
source venv/bin/activate  # (or venv\Scripts\activate on Windows)

# Install the Cylestio Monitor from the parent directory in development mode
pip install -e ../../..
```

## Quick Start

```python
from cylestio_monitor import start_monitoring
from anthropic import Anthropic

# Create your LLM client
client = Anthropic()

# Enable monitoring with a remote API endpoint
start_monitoring(
    agent_id="my_agent",
    config={
        "api_endpoint": "https://your-api-endpoint.com/events"
    }
)

# Use your client as normal
response = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=1000,
    messages=[{"role": "user", "content": "Hello, Claude!"}]
)

# When finished, stop monitoring
from cylestio_monitor import stop_monitoring
stop_monitoring()
```

## Key Features

- **Zero-configuration setup**: Import and enable with just two lines of code
- **Multi-framework support**: Works with popular LLM clients and frameworks including Model Context Protocol (MCP)
- **Complete request-response tracking**: Captures both outgoing LLM requests and incoming responses 
- **Security monitoring**: Detects and blocks dangerous prompts
- **Performance tracking**: Monitors call durations and response times
- **Flexible storage options**: Events can be sent to a remote API endpoint or stored locally in JSON files

## Security Features

- **Prompt injection detection**: Identify and block malicious prompt injection attempts
- **PII detection**: Detect and redact personally identifiable information
- **Content filtering**: Filter out harmful or inappropriate content
- **Security rules**: Define custom security rules for your specific use case

## Framework Support

Cylestio Monitor supports:

- **Direct API calls**: Anthropic, Claude models (all versions)
- **LangChain**: Chains, agents, and callbacks
- **LangGraph**: Graph-based agents and workflows 
- **MCP (Model Context Protocol)**: Tool calls and responses

See [docs/compatibility.md](docs/compatibility.md) for the full compatibility matrix.

## Repository Structure

The Cylestio Monitor repository is organized as follows:

```
cylestio-monitor/
├── src/                       # Source code for the Cylestio Monitor package
│   └── cylestio_monitor/      # Main package
│       ├── patchers/          # Framework-specific patchers (Anthropic, MCP, etc.)
│       ├── events/            # Event definitions and processing
│       ├── config/            # Configuration management
│       └── utils/             # Utility functions
├── examples/                  # Example implementations
│   └── agents/                # Various agent examples demonstrating integration
├── tests/                     # Test suite
│   ├── integration/           # Integration tests
│   └── fixtures/              # Test fixtures
└── docs/                      # Documentation
    ├── compatibility.md       # Framework compatibility information
    ├── getting-started/       # Getting started guides
    ├── advanced-topics/       # Advanced usage documentation
    └── sdk-reference/         # API reference documentation
```

## Testing

Cylestio Monitor uses a comprehensive testing approach with custom tooling to ensure consistent test execution across different environments. 

### Running Tests

We recommend using our custom test runner which handles dependency mocking and environment setup:

```bash
# Run all tests
python tests/run_tests.py

# Run with coverage
python tests/run_tests.py --cov=src --cov-report=term-missing

# Run specific tests
python tests/run_tests.py tests/test_api_client.py

# Run tests with specific markers
python tests/run_tests.py -m "integration"
```

This approach ensures that tests run consistently regardless of the environment or installed dependencies. See [docs/TESTING.md](docs/TESTING.md) for detailed information about our testing approach.

## API Client

The Cylestio Monitor now uses a lightweight REST API client to send telemetry events to a remote endpoint instead of storing them in a local database. This approach offers several advantages:

- **Centralized Event Storage**: All events from different agents can be collected in a central location
- **Real-time Monitoring**: Events are sent in real-time to the API for immediate analysis
- **Minimal Storage Requirements**: No local database maintenance required
- **Scalability**: Easily scale monitoring across multiple agents and applications

The API client can be configured by providing an endpoint URL either through the `api_endpoint` configuration parameter or by setting the `CYLESTIO_API_ENDPOINT` environment variable.

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to get started.

## Documentation

For complete documentation, including detailed guides, API reference, and best practices, visit:

**[https://docs.cylestio.com](https://docs.cylestio.com)**

## License

MIT
