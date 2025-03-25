import click
from backgen.utils.file import create_project_structure

@click.command()
@click.argument("project_name")
def create_project(project_name):
    """Créer un projet backend (FastAPI)"""
    click.echo(f"📂 Création du projet : {project_name}")
    create_project_structure(project_name)
    click.echo("✅ Projet créé avec succès ! 🚀")
