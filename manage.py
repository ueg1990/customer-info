from flask_script import Manager

from app.app import create_app
from app.config import DevConfig


app = create_app(config_object=DevConfig)

@app.route('/')
def hello_world():
    return 'Hello World!'

manager = Manager(app)


if __name__ == "__main__":
    manager.run()
