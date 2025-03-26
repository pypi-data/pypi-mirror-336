import click
from deploy import run_deploy

@click.group()
def cli():
    """FlaskAir - Simple Flask Deployment Tool"""
    pass

@cli.command()
@click.argument("app_path")
@click.option("--domain", help="Domain name for the Flask app")
@click.option("--db", is_flag=True, help="Set up MySQL for the app")
def deploy(app_path, domain, db):
    """Deploy a Flask app with Nginx, Gunicorn, and MySQL (optional)."""
    from .deploy import run_deploy
    run_deploy(app_path, domain, db)

if __name__ == "__main__":
    cli()

