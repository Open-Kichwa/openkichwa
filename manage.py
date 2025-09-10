from flask.cli import FlaskGroup
from dotenv import load_dotenv
load_dotenv()

from src import app

cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()