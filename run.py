# the main Flask application
from site_client import create_site_app

app = create_site_app()

if __name__ == "__main__":
	app.run(**app.config['INIT'])
