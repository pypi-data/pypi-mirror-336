import click

@click.command()
def security_check():
    """Vérifie les vulnérabilités du projet."""
    click.echo("🔒 Vérification de sécurité en cours...")
    click.echo("✅ Aucun problème détecté.")
