
import click
import bisi.interface

from bisi.__version__ import __version__


@click.group(name='bisi')
def cli():
    """bisi cli for building, deploying, and running docker workloads"""
    pass


@cli.command()
def version():
    """Prints the current version of bisi"""
    print(__version__)


@cli.command()
def build():
    """Builds any resources locally"""
    bisi.interface.build()


@cli.command()
def deploy():
    """Deploys resources to cloud providers"""
    bisi.interface.deploy()


@cli.command()
@click.argument('name', type=str)
@click.option('--provider', type=str, default='Local')
@click.argument('arguments', type=str, nargs=-1)
def run(name, provider, arguments):
    """Run NAME with ARGUMENTS """
    bisi.interface.run(name, arguments, provider=provider)


if __name__ == '__main__':
    cli()
