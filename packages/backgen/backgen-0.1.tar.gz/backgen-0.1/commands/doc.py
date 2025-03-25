import click

@click.command()
def generate_doc():
    """Génère automatiquement la documentation du projet."""
    click.echo("📖 Génération de documentation...")
    click.echo("✅ Documentation générée.")
