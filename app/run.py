# Application Entrypoint
import os
from src import create_app
from src.seed_data import seed_database

env_mode = os.getenv("FLASK_ENV", "development")
app = create_app(env_mode)

with app.app_context():
    # Automatically seed base data on initial startup
    seed_database()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "true").lower() in ["true", "1", "t"]
    print(f"Starting Smart Accident Detection & Emergency Response System on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=debug)
