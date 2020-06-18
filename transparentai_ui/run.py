import click
from .app import app


@click.command()
@click.option('--port', default=5000, help='Port of the application')
def main():
    """Run the transparentai-ui program that launch a
    Flask Webapp
    """
    app.run(port=port)


if __name__ == '__main__':
    main()
