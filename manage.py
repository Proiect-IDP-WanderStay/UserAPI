from flask.cli import FlaskGroup
from user import app, db 
from user.users import bp_user

cli = FlaskGroup(app)

# blueprints
app.register_blueprint(bp_user)

@cli.command("start_auth")
def create_db():
    # destroy all tables and creat new ones
    # this is good for testing, you can delete it if you want full persistency
    print("here we go again")


@cli.command("seed_db")
def seed_db():
    db.session.commit()


if __name__ == "__main__":
    cli()