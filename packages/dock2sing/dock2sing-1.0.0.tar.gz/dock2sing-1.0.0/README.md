# Dock2Sing

A Python-based tool for converting Docker Compose configurations to Singularity Compose format, with built-in validation and guidance.

## Overview

This tool helps users migrate their Docker Compose configurations to Singularity Compose format, which is particularly useful in HPC (High-Performance Computing) environments where Singularity is the preferred container runtime. The tool includes a validation component that helps identify potential issues and provides guidance for the conversion process.

## Features

- Converts Docker Compose services to Singularity instances
- Handles key Docker Compose features:
  - Container images
  - Volume mounts
  - Environment variables
  - Port mappings
  - Working directories
  - Service dependencies
- Provides detailed validation of converted configurations
- Offers guidance for handling unsupported features
- Includes colored terminal output for better readability
- Supports comparison with original Docker Compose file

## Requirements

- Python 3.12 or higher
- Poetry for dependency management
- Singularity installed on the target system

## Installation

1. Clone the repository:
```bash
git clone https://github.com/labadorf/dock2sing.git
cd dock2sing
```

2. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install the project and its dependencies:
```bash
poetry install
```

## Usage

### Converting Docker Compose to Singularity Compose

```bash
poetry run dock2sing docker-compose.yml [-o singularity-compose.yml]
```

Options:
- `docker-compose.yml`: Path to your Docker Compose file (required)
- `-o, --output`: Path for the output Singularity Compose file (optional, defaults to `singularity-compose.yml`)

### Validating Singularity Compose Configuration

```bash
poetry run validate-singularity singularity-compose.yml [-d docker-compose.yml]
```

Options:
- `singularity-compose.yml`: Path to your Singularity Compose file (required)
- `-d, --docker`: Path to the original Docker Compose file for comparison (optional)

## Development

This project uses several development tools to maintain code quality:

- `pytest` for testing
- `black` for code formatting
- `isort` for import sorting
- `flake8` for linting

To set up the development environment:

```bash
poetry install --with dev
```

To run tests:
```bash
poetry run pytest
```

To format code:
```bash
poetry run black .
poetry run isort .
```

## Important Notes

### Feature Compatibility

Some Docker features have different implementations or limitations in Singularity:

1. **Networking**:
   - Singularity networking works differently from Docker
   - Custom networks need manual configuration
   - Port mappings may require additional setup

2. **Volumes**:
   - Named volumes need manual configuration
   - Volume paths should be absolute
   - Bind mounts work differently in Singularity

3. **User Permissions**:
   - Singularity containers run with user permissions by default
   - Root access requires special configuration
   - User namespace handling differs from Docker

4. **Unsupported Features**:
   - Healthchecks
   - Secrets
   - Configs
   - Deploy configurations

### Best Practices

1. Always validate your converted configuration
2. Test each container individually before running the full setup
3. Review the validation warnings and address them appropriately
4. Consider using Singularity definition files for custom container builds
5. Use absolute paths for volume mounts
6. Test thoroughly in your target environment

## Example

### Input Docker Compose File
```yaml
version: '3'
services:
  web:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./data:/usr/share/nginx/html
    environment:
      - DEBUG=1
```

### Output Singularity Compose File
```yaml
version: '1.0'
instances:
  web:
    container: docker://nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./data:/usr/share/nginx/html
    environment:
      DEBUG: "1"
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Docker Compose team for the original specification
- Singularity team for the container runtime
- Contributors and users of this tool 