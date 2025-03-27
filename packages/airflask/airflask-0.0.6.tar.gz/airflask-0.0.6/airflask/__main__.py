import click
from airflask.deploy import run_deploy

@click.group()
def cli():
    """FlaskAir"""
    pass

@cli.command()
@click.argument("app_path")
@click.option("--domain", help="Domain name for the Flask app")
@click.option("--db", is_flag=True, help="Set up MySQL for the app")
def deploy(app_path, domain, db):
   
    run_deploy(app_path)

if __name__ == "__main__":
    cli()

