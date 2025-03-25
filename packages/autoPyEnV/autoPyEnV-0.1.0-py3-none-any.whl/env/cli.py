import os
import shutil
import click

# Define the directory where virtual environments will be stored
ENV_DIR = os.path.expanduser("~/.envs")  # Linux/macOS
if os.name == "nt":  # Windows
    ENV_DIR = os.path.join(os.getenv("USERPROFILE"), ".envs")


# Ensure ENV_DIR exists
os.makedirs(ENV_DIR, exist_ok=True)


@click.group()
def cli():
    """Environment Management CLI"""
    pass


@click.command()
@click.argument("name")
def create(name):
    """Create a new virtual environment"""
    env_path = os.path.join(ENV_DIR, name)

    if os.path.exists(env_path):
        click.echo(f"Environment '{name}' already exists!")
        return

    os.system(f"python -m venv {env_path}")
    click.echo(f"Environment '{name}' created at {env_path}")


@click.command()
@click.argument("name")
def activate(name):
    """Print activation command for an environment"""
    env_path = os.path.join(ENV_DIR, name)
    
    if not os.path.exists(env_path):
        click.echo(f"Environment '{name}' not found!")
        return

    if os.name == "nt":  # Windows
        activate_command = f"{env_path}\\Scripts\\activate"
    else:  # Linux/macOS
        activate_command = f"source {env_path}/bin/activate"

    click.echo(f"Run the following command to activate the environment:\n{activate_command}")


@click.command()
def list():
    """List all environments"""
    envs = os.listdir(ENV_DIR)
    if not envs:
        click.echo("No environments found.")
    else:
        click.echo("Available Environments:")
        for env in envs:
            click.echo(f"  - {env}")


@click.command()
@click.argument("name")
def delete(name):
    """Delete a virtual environment"""
    env_path = os.path.join(ENV_DIR, name)

    if os.path.exists(env_path):
        try:
            shutil.rmtree(env_path)  # Deletes the environment folder
            click.echo(f"Environment '{name}' deleted successfully.")
        except Exception as e:
            click.echo(f"Error deleting environment '{name}': {e}")
    else:
        click.echo(f"Environment '{name}' not found.")


# Add commands to the CLI
cli.add_command(create)
cli.add_command(activate)
cli.add_command(list)
cli.add_command(delete)

if __name__ == "__main__":
    cli()
