import click

@click.group()
def cli():
    """GCS Command Line Tool"""
    pass

@cli.command()
def info():
    """Show information about GCS CLI"""
    click.echo("By JDCloud AIDC Team")

if __name__ == '__main__':
    cli()
