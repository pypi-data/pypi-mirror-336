# Trainwave CLI

A command-line interface for interacting with Trainwave's machine learning platform. This CLI tool provides functionality for managing training jobs, handling authentication, managing secrets, and configuring your Trainwave environment.

## Features

- Job Management: Create, monitor, and manage training jobs
- Authentication: Secure authentication with Trainwave's platform
- Secrets Management: Handle sensitive information for your jobs
- Configuration: Set up and manage your Trainwave environment

## Installation

### Using pip

```bash
pip install trainwave-cli
```

### From Source

1. Clone the repository
2. Install using Poetry:

```bash
poetry install
```

## Usage

The CLI provides several main commands:

```bash
wave jobs     # Manage training jobs
wave auth     # Authenticate with Trainwave
wave config   # Configure your Trainwave environment
wave secrets  # Manage job secrets
```

For detailed help on any command:

```bash
wave --help
wave <command> --help
```

## Development

This project uses Poetry for dependency management and packaging. Here's how to set up your development environment:

### Prerequisites

- Python 3.10 or higher
- Poetry
- Make (for development commands)

### Setting Up Development Environment

1. Clone the repository
2. Install development dependencies:

```bash
make install-dev
```

### Development Commands

The project includes several Make targets to help with development:

- `make install`: Install production dependencies
- `make install-dev`: Install development dependencies
- `make clean`: Remove temporary files and build artifacts
- `make ruff`: Run Ruff linter
- `make format`: Format code using Black and Ruff
- `make check`: Run all code quality checks
- `make test`: Run the test suite
- `make help`: Show available make commands

### Code Style

The project uses:

- Ruff for linting
- Black for code formatting
- Type hints are required for all functions

### Running Tests

```bash
make test
```

Or directly with pytest:

```bash
pytest tests/
```

## Project Structure

```
trainwave-cli/
├── trainwave_cli/     # Main package directory
├── tests/            # Test files
├── example/          # Example configurations and usage
├── pyproject.toml    # Project metadata and dependencies
└── Makefile         # Development automation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting: `make check`
5. Submit a pull request

## License

[License information here]
