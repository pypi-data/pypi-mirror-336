# Verti-OSI CLI Tool Documentation

## Overview
Verti-OSI is a command-line tool designed to generate OCI-compliant container images. It allows users to create container images from a specified project source directory while offering various customization options such as selecting the container runtime daemon, output type, and execution of the generated image.

### Supported Languages
Currently, `verti-osi` supports **Python** and **Node.js** projects. The CLI automatically detects the language package manager and generates the appropriate container image.

## Prerequisites
To use `verti-osi`, ensure the following:

- **Python 3.7+** installed. Check with:
  ```sh
  python --version
  ```
- **PIPX** installed. Check with:
  ```sh
  pipx --version
  ```
  If missing, install it via:
  ```sh
  python -m pip install --user pipx
  pipx ensurepath
  ```
- **A running container daemon (Docker or Podman).**
  - **Docker**: Ensure the daemon is running:
    ```sh
    docker info
    ```
  - **Podman**: Ensure Podman is installed and running:
    ```sh
    podman info
    ```

## Installation (via `pipx`)
To install `verti-osi` globally using `pipx`, run:

```sh
pipx install verti-osi
```

## Usage
After installation, invoke the CLI tool using `verti-osi`. Below is the command structure and available options:

```sh
verti-osi --root-directory <path> \
          --source-directory <path> \
          --image-name <name> \
          --daemon <daemon-type> \
          --output <output-type> \
          --delete-generated-dockerfile <True/False> \
          --run-generated-image <True/False>
```

### Command Parameters
- `--root-directory` (default: `.`) - The root directory of the project.
- `--source-directory` (default: `.`) - The directory containing the project’s source code.
- `--image-name` (required) - The name of the image to be generated.
- `--daemon` (default: `docker`) - The container runtime daemon to be used (`docker` or `podman`).
- `--output` (default: `''`) - The output type for the generated image. Supports `tar`, `registry` push, and standard image generation.
- `--delete-generated-dockerfile` (default: `False`) - If `True`, the generated Dockerfile will be deleted after image creation.
- `--run-generated-image` (default: `False`) - If `True`, the generated container image will be executed immediately.

### Automatic Language Detection
`verti-osi` automatically detects the programming language based on the project structure:

- **Python**: If `requirements.txt` or `pyproject.toml` is found, the CLI generates a Python-based image.
- **Node.js**: If `package.json` is detected, the CLI generates a Node.js-based image.

### Example Usage
#### 1. Generating a container image
```sh
verti-osi --root-directory . \
          --source-directory ./src \
          --image-name nodey-js-verti:v1-normal
```

#### 2. Generating and pushing an image to a registry
```sh
verti-osi --root-directory . \
          --source-directory ./src \
          --image-name my-repo/nodey-js-verti:v1 \
          --output registry
```

#### 3. Generating an image and deleting the Dockerfile
```sh
verti-osi --root-directory . \
          --source-directory ./src \
          --image-name nodey-js-verti:v1 \
          --delete-generated-dockerfile True
```

#### 4. Generating an image and running it immediately
```sh
verti-osi --root-directory . \
          --source-directory ./src \
          --image-name nodey-js-verti:v1 \
          --run-generated-image True
```

## Development
If you wish to contribute or modify the tool, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/verti-osi.git
   cd verti-osi
   ```

2. Install the package in development mode:
   ```sh
   pip install -e .
   ```

3. Run the CLI tool:
   ```sh
   verti-osi --help
   ```

## Uninstallation
To remove `verti-osi`, run:
```sh
pipx uninstall verti-osi
```

## License
Verti-OSI is licensed under the MIT License.

