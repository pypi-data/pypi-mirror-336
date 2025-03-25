import click
from .core import fetch_dependencies

@click.command()
@click.option('--dir', default='.', help='Project directory to scan for dependencies')
@click.option('--interactive', is_flag=True, help='Enable interactive mode')
@click.option('--fix-missing', is_flag=True, help='Auto-fix missing dependencies')
def cli(dir, interactive, fix_missing):
    """CLI entry point for Dency"""
    fetch_dependencies(dir, interactive, fix_missing)

def main():
    cli()

if __name__ == "__main__":
    main()
