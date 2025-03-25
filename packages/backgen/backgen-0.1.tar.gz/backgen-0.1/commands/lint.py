import click
import os

@click.command()
@click.argument("project_path", required=False, default=".")
def lint_code(project_path):
    """Vérifie la qualité du code avec flake8."""
    click.echo("🔍 Analyse de code en cours...")
    os.system(f"flake8 {project_path}")
    click.echo("✅ Analyse terminée.")
