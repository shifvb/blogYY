import os
import sys
from web_content import app
sys.path.insert(0, os.path.abspath(".."))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="80")
