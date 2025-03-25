import click

def log_info(message):
    click.echo(click.style(message, fg="blue"))

def log_success(message):
    click.echo(click.style(message, fg="green"))

def log_error(message):
    click.echo(click.style(message, fg="red"))
