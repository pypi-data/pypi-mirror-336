# July

Proof-of-Work (PoW) Security Measure to protect your flask apps from Bots and Scrapers

## Setup

Simply set up July in a Flask App by typing

```python
from flask import Flask
from flask_july import Flask_July

app = Flask(__name__)
app.config["SECRET_KEY"] = "Super Secret!"
july = Flask_July(app)
```

By default, once your app runs, it will show something like
![this](/img/1.png)

(Don't worry! Anything under /static is always allowed to be accessed)


But what if you don't wanna include *every* Path? Well, using the below code, you can set up exclusions

```py
july = Flask_July(app)


@july.validate
def validate_fn():
    if request.path.startswith("/no-bots-pls"): return True
```