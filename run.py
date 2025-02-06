import signal
import sys
from src.main.server.config import create_app

def signal_handler(sig, frame):
    print('\nEncerrando a aplicação graciosamente...')
    sys.exit(0)

app = create_app()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    try:
        app.run(
            host="0.0.0.0",
            port=3000,
            debug=True
        )
    except KeyboardInterrupt:
        print('\nEncerrando a aplicação graciosamente...')
        sys.exit(0)
