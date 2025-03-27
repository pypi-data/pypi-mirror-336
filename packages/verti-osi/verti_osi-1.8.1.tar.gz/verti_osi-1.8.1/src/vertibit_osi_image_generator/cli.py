import typer
import os
from vertibit_osi_image_generator.main.config_file_processor import load_and_validate_config
from vertibit_osi_image_generator.main.docker_file_generation import main_docker_file_generator
from vertibit_osi_image_generator.shared_aux.config_aux import format_params_to_schema
from vertibit_osi_image_generator.shared_aux.language_package_managers import extract_images
from vertibit_osi_image_generator.shared_aux.language_package_manager_scanner import main_language_scanner
from vertibit_osi_image_generator.image_build.generate_docker_image import build_docker_image
from vertibit_osi_image_generator.shared_aux.shared import generate_random_string
from vertibit_osi_image_generator.verti_file_config_aux.file_config import verify_config_file
from typing import List

app = typer.Typer()


@app.command()
def create(
    file_dir: str = typer.Option(
        "", help="Path to the verti-osi.yaml config file. e.g: /dir/path"),
    platforms: str = typer.Option(
        "", help="Platforms the built image should support. e.g: linux/amd64,linux/arm64"),
    repository_branch: str = typer.Option(
        "", help="Repository branch to be used. e.g. main, develop"),
    repository_url: str = typer.Option(
        "", help="Remote repository URL. e.g. https://github.com/owner/repo"),
    env_vars: List[str] = typer.Option(
        [], help="Application ENV vars. e.g. KEY=VALUE,KEY=VALUE"),
    env_vars_rt: List[str] = typer.Option(
        [], help="Runtime ENV vars. e.g. KEY=VALUE,KEY=VALUE"),
    env_vars_bt: List[str] = typer.Option(
        [], help="Build-time ENV vars. e.g. KEY=VALUE,KEY=VALUE"),
    build_commands: List[str] = typer.Option(
        [], help="Build commands to run. e.g. npm run build, npm run lint"),
    pre_build_commands: List[str] = typer.Option(
        [], help="Pre-build commands to run before the build process."),
    root_directory: str = typer.Option('.', help="Project's root directory."),
    source_directory: str = typer.Option('.', help="Source code directory."),
    image_name: str = typer.Option(
        "", help="Name for the generated container image."),
    daemon: str = typer.Option(
        'docker', help="Container daemon to use (e.g., docker, podman)."),
    output: str = typer.Option(
        "", help="Generated image output type. Options: tar, registry, standard"),
    delete_generated_dockerfile: bool = typer.Option(
        False, help="Delete the generated Dockerfile after build."),
    run_generated_image: bool = typer.Option(
        False, help="Run the generated Docker image after build."),
    port: int = typer.Option(
        8080, help="The port to be exposed.")
):
    """
    Generate a container image.
    """
    # Define the config file name
    verti_osi_config_file = 'verti-osi.yaml'
    # Config file object to be referenced
    config = {}

    # Check if the config file is used to provided the parameters
    if file_dir != "":
        config_file_exists = verify_config_file(
            file_dir, verti_osi_config_file)
        # Check if the config file exists
        if config_file_exists:
            config_path = os.path.join(file_dir, verti_osi_config_file)
            # Validate and load the config file
            config = load_and_validate_config(
                image_config_path=config_path, config_file='config.json')

    else:
        # Format the cli parameters to a schema
        config = format_params_to_schema(platforms=platforms, repository_branch=repository_branch, repository_url=repository_url, env_vars=env_vars,
                                         env_vars_bt=env_vars_bt, env_vars_rt=env_vars_rt, build_commands=build_commands, pre_build_commands=pre_build_commands, root_directory=root_directory, source_directory=source_directory, image_name=image_name, daemon=daemon, output=output, delete_generated_dockerfile=delete_generated_dockerfile, port=port)

    # Scan the directory for the language package manager
    language_info = main_language_scanner(root_directory)

    # Generate a random image name if not provided
    if config['image-name'] == "":
        random_key = generate_random_string()
        image_name_prefix = 'verti-osi'

        config['image-name'] = f'{image_name_prefix}-{language_info['language'].lower()}-{random_key}'

    # Extract the language images
    images = extract_images(language_info["language"])

    # Generating docker file content
    docker_file_content = main_docker_file_generator(
        language_info=language_info, images=images, source_directory=config['source-directory'], root_directory=config['root-directory'], env_vars=config['env-vars'],port=config['port'])

    # typer.echo(f"Identified language: {language_info['language']}")
    # typer.echo(f"Identified language images: {images}")

    # Ensure the 'tmp' directory exists
    os.makedirs("tmp", exist_ok=True)

    # Write the generated Dockerfile to a file
    with open("tmp/Dockerfile", "w") as f:
        f.write(docker_file_content)

    build_docker_image(daemon=daemon, image_name=config['image-name'], container_file='tmp/Dockerfile',
                       build_context=config['root-directory'], output=config['output-type'], delete_generated_dockerfile=config['delete-generated-dockerfile'], run_generated_image=run_generated_image)


if __name__ == "__main__":
    app()
