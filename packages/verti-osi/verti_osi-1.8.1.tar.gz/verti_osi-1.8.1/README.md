# Verti-OSI CLI Tool Documentation

## Overview

Verti-OSI is a command-line tool designed to generate OCI-compliant container images. It allows users to create container images from a specified project source directory while offering various customization options such as selecting the container runtime daemon, output type, and execution of the generated image.

## Supported Languages

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

- **A running container daemon (Docker or Podman)**  
  - **Docker**: Ensure the daemon is running:
    ```sh
    docker info
    ```
  - **Podman**: Ensure Podman is installed and running:
    ```sh
    podman info
    ```

## Installation (via pipx)

To install `verti-osi` globally using pipx, run:

```sh
pipx install verti-osi
```

## Usage

After installation, invoke the CLI tool using `verti-osi`. Below is the command structure and available options.

### Command Parameters

```sh
verti-osi --root-directory <path> \
          --source-directory <path> \
          --image-name <name> \
          --daemon <daemon-type> \
          --output <output-type> \
          --delete-generated-dockerfile <True/False> \
          --run-generated-image <True/False> \
          --file-dir <path> \
          --platforms <comma-separated-platforms> \
          --repository-branch <branch> \
          --repository-url <url> \
          --env-vars <KEY=VALUE,...> \
          --env-vars-rt <KEY=VALUE,...> \
          --env-vars-bt <KEY=VALUE,...> \
          --pre-build-commands <commands> \
          --build-commands <commands> \
          --port <port-number>
```

### Explanation of Parameters

- `--root-directory` - Root directory of the project. Default: `.`
- `--source-directory` - Directory containing source code. Default: `.`
- `--image-name` - Name for the generated image. If empty, auto-generated.
- `--daemon` - Container daemon to use: `docker` or `podman`. Default: `docker`
- `--output` - Output type: `tar`, `registry`, or `standard`. Default: `standard`
- `--delete-generated-dockerfile` - Deletes Dockerfile after build. Default: `False`
- `--run-generated-image` - Runs image after build. Default: `False`
- `--file-dir` - Directory path containing `verti-osi.yaml` config
- `--platforms` - Supported platforms. e.g., `linux/amd64,linux/arm64`
- `--repository-branch` - Branch name for remote repo
- `--repository-url` - Git URL for remote repo
- `--env-vars` - List of env vars for all stages. Format: `KEY=VALUE`
- `--env-vars-rt` - Runtime-specific env vars
- `--env-vars-bt` - Build-time-specific env vars
- `--pre-build-commands` - Commands to run before build
- `--build-commands` - Commands to run during build
- `--port` - Port to be exposed. Default: `8080`

---

## Configuration via YAML

You can also configure your build using a YAML file named `verti-osi.yaml`.

Use it with the `--file-dir` flag:

```sh
verti-osi --file-dir <path-to-directory>
```

### YAML File Example

```yaml
image-name: verti-node-app:v1
source-directory: ./src
root-directory: .
delete-generated-dockerfile: true
daemon: docker
output-type: tar
platform:
  - linux/amd64
  - linux/arm64
pre-build:
  - echo "Running pre-build steps"
build:
  - npm run build
env-vars:
  - name: API_KEY
    value: abc123
    type: both
  - name: DEBUG
    value: true
    type: runtime
port: 8080
remote-source-repository:
  git:
    url: https://github.com/example/project
    branch: main
```

---

## Automatic Language Detection

`verti-osi` detects the language based on project files:

- **Python**: Detected if `requirements.txt` or `pyproject.toml` exists.
- **Node.js**: Detected if `package.json` is present.

---

## Example Usages

### Generate a container image

```sh
verti-osi --root-directory . \
          --source-directory ./src \
          --image-name nodey-js-verti:v1-normal
```

### Generate and push to a registry

```sh
verti-osi --root-directory . \
          --source-directory ./src \
          --image-name my-repo/nodey-js-verti:v1 \
          --output registry
```

### Generate and delete Dockerfile

```sh
verti-osi --root-directory . \
          --source-directory ./src \
          --image-name nodey-js-verti:v1 \
          --delete-generated-dockerfile True
```

### Generate and run image

```sh
verti-osi --root-directory . \
          --source-directory ./src \
          --image-name nodey-js-verti:v1 \
          --run-generated-image True
```

### Generate using YAML config

```sh
verti-osi --file-dir ./configs
```

---

## License

Verti-OSI is licensed under the MIT License.
