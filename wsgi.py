from app import create_app
from waitress import serve
import logging
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = create_app()
CORS(app)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
    handlers=[
        logging.FileHandler("waitress.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('waitress')
#logger.setLevel(logger.DEBUG)


if __name__ == "__main__":
    logger.info("Starting the Waitress server...")
    serve(app, host="0.0.0.0", port=8331)
    #app.run(host='127.0.0.1', port=8000, debug=True)

