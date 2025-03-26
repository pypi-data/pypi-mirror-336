from flask import Response, request, session, redirect, Flask, render_template_string, jsonify
import hashlib
import random
import string

class JSRedirectionBackend:
    """
    Simply implements a js redirect - Not recommended for security purposes, but significantly faster than PoW
    """
    def __init__(self):
        self.html = """
        

<!DOCTYPE html>
<html>
<head>
    <title>Making sure you're not a bot...</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap">
    <link rel="stylesheet" href="/July.x/style.css">

</head>
<body class="anti-bot">
    <script>
    async function submitSolution(nonce, attempt, difficulty) {
        const response = await fetch("/July.x/validate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: '{"nonce": 0, "difficulty": 3}'
        });
        const result = await response.json();
        if (result.status === "failure") {
            console.error("Failed to solve challenge. Bye bye!");
            location.href = "/July.x/failed";
        }
        else {
            location.href = result.next;
            }
    }
    setTimeout(() => submitSolution(0,0,0), 3000)
    </script>
    <h1>You are being redirected</h1>
    <p>Verifying you are human. This might take a few seconds.</p>
    <span class="loader"></span>
    <p>If you're not redirected, <a href="#" onclick="submitSolution(); return false;">click here</a> to try again.</p>
    <p>Scraper-Protection by <a href="/July.x">July</a> from Within</p>
</body>
</html>

"""

    
    def generate_token(self):
        return hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()
           
    def generate_challenge(self, difficulty=4):
        return None, None
    
    def valid_solution(self, *a):
        print("[JS Redirection] No Security Checks")
        return True

    def valid_token(self, *a):
        return True

class CryptoBackend:
    """
    Proof-of-Work Based Backend, as opposed to JSRedirectionBackend
    """
    def __init__(self):
        self.html = """

<!DOCTYPE html>
<html>
<head>
    <title>Making sure you're not a bot...</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap">
    <link rel="stylesheet" href="/July.x/style.css">

</head>
<body class="anti-bot">
    <script>
    let attempt = 0;
    async function getChallenge() {
        const response = await fetch("/July.x/challenge.json");
        const data = await response.json();
        return data;
    }

    async function solveChallenge(nonce, difficulty) {
    let attempt = 0;
    while (true) {
        attempt++;
        const testStr = nonce + attempt;
        
        // Compute SHA-256 hash
        const hashBuffer = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(testStr));
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, "0")).join("");
        if (attempt % 1000 === 0) {
            //console.log(`Attempt ${attempt}: ${hashHex}`);
        }

        // Check if hash meets the difficulty condition
        if (hashHex.startsWith("0".repeat(difficulty))) {
            return attempt;
        }
    }
}

    async function submitSolution(nonce, attempt, difficulty) {
        console.log(`Submitting solution: nonce=${nonce}, attempt=${attempt}`);
        console.log(JSON.stringify({ nonce, attempt, difficulty }))
        const response = await fetch("/July.x/validate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nonce, attempt, difficulty })
        });
        const result = await response.json();
        if (result.status === "failure") {
            console.error("Failed to solve PoW challenge. Bye bye!");
            location.href = "/July.x/failed";
        }
        else {
            location.href = result.next;
            }
    }

    async function runPoW() {
        console.log("Fetching challenge...");
        const { nonce, difficulty } = await getChallenge();
        console.log(`Solving PoW: nonce=${nonce}, difficulty=${difficulty}`);

        const attempt = await solveChallenge(nonce, difficulty);
        console.log(`Solution found: attempt=${attempt}`);

        await submitSolution(nonce, attempt, difficulty);
    }



    runPoW();
    </script>
    <h1>Prove you're not a bot!</h1>
    <p>Just a moment...</p>
    <span class="loader"></span>
    <p>If you're not redirected, <a href="#" onclick="runPoW(); return false;">click here</a> to try again.</p>
    <p>Scraper-Protection by <a href="/July.x">July</a> from Within</p>
</body>
</html>
"""
    def generate_token(self):
        return hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()
            
    def generate_challenge(self, difficulty=4):
        nonce = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        return nonce, difficulty
    
    def valid_solution(self, nonce, attempt, difficulty):
        test_str = f"{nonce}{attempt}"
        hash_result = hashlib.sha256(test_str.encode()).hexdigest()
        print(f"Validating: {test_str} -> {hash_result}")
        return hash_result.startswith("0" * difficulty)

    def valid_token(self, token):
        return True # TODO implement token validation

class Flask_July:
    """
    July is a Proof-of-Work-Based Flask Helper to migitate Scrapers and Bots -- Sadly (or not) it blocks even the "good" bots, such as Archive.org, Google, Bing, etc.

    :param app: Flask App
    :type app: Flask

    
    By default, *all* routes are checked. You can specify that only certain routes should be checked by using the `validate` decorator.
    Sample Usage:

    ```python
    from flask import Flask
    from July import Flask_July

    app = Flask(__name__)
    July = Flask_July(app)

    @app.route('/')
    def index():
        return 'Hello World!'
    ```

    You can also specify that all but certain routes should be checked:

    ```python
    @July.validate
    def is_safe():
        return request.path != '/dont_check_me'
    ```
    """

    def __init__(self, app = None, backend=CryptoBackend()):
        self.validate_func = lambda: True
        self.backend = backend
        self.init_app(app)

    def init_app(self, app: "Flask"):
        if not app.secret_key and not app.config.get("SECRET_KEY"): raise Exception("July cannot start because no SECRET_KEY was present")
        self.app = app
        if self.app:
            self.app.before_request(self.check)

            @self.app.route("/July.x/style.css")
            def style_css():
                return Response(__JULY_CSS__, mimetype="text/css")

            @self.app.route("/July.x/challenge")
            def challenge():
                return render_template_string(self.backend.html)

            @self.app.route("/July.x/challenge.json")
            def challenge_json():
                nonce, difficulty = self.backend.generate_challenge()
                return jsonify({"nonce": nonce, "difficulty": difficulty})

            @self.app.route("/July.x")
            def what_is_july():
                return render_template_string(__WHAT_IS_JULY__)
            
            @self.app.route("/July.x/failed")
            def failed():
                return render_template_string(__JULY_FAILED_HTML__)
            
            @self.app.route("/July.x/validate", methods=["POST"])
            def validate():
                print(request.get_json())
                
                nonce = request.json.get("nonce")
                solution = request.json.get("attempt")
                difficulty = request.json.get("difficulty")
                print(nonce, solution, difficulty)
                if self.backend.valid_solution(nonce, solution, difficulty):
                    session["X-July-Token"] = self.backend.generate_token()
                    return jsonify({"status": "success", "next": request.args.get("next", "/")})
                return jsonify({"status": "failure"}), 400
    
    
    def validate(self, func):
        self.validate_func = func
        return func
    
    def check(self):
        if self.validate_func():
            if request.path.startswith("/July.x") or request.path.startswith("/static"):
                return None
            
            if "X-July-Token" not in session or not self.backend.valid_token(session.get("X-July-Token")):
                return redirect("/July.x/challenge?next=" + request.path)
            return None
        


__JULY_HTML__ = CryptoBackend().html

__JULY_CSS__ = """
.loader {
  width: 48px;
  height: 48px;
  border: 2px solid #FFF;
  border-radius: 50%;
  display: inline-block;
  position: relative;
  box-sizing: border-box;
  animation: rotation 1s linear infinite;
}
.loader::after,
.loader::before {
  content: '';  
  box-sizing: border-box;
  position: absolute;
  left: 0;
  top: 0;
  background: #FF3D00;
  width: 6px;
  height: 6px;
  transform: translate(150%, 150%);
  border-radius: 50%;
}
.loader::before {
  left: auto;
  top: auto;
  right: 0;
  bottom: 0;
  transform: translate(-150%, -150%);
}

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
} 


body.anti-bot {
    font-family: 'Roboto', sans-serif;
    align-items: center;
    text-align: center;
    background: #333;
    color: #FFF;
    pointer-events: none;
}


"""

__WHAT_IS_JULY__ = """
<html>
<head>
    <title>What is July?</title>
    <link rel="stylesheet" href="/July.x/style.css">
</head>
<body>
    <h1>What is July?</h1>
    <p>July is a Proof-of-Work-Based Flask Helper to migitate Scrapers and Bots -- Sadly (or not) it blocks even the "good" bots, such as Archive.org, Google, Bing, etc.</p>
    <p>It is a simple, yet effective, way to stop bots from scraping your website.</p>
    <p>It is not perfect, but it is a good start.</p>
</body>
</html>
"""

__JULY_FAILED_HTML__ = """

<!DOCTYPE html>
<head>
    <title>Failed to Solve PoW Challenge</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap">
    <link rel="stylesheet" href="/July.x/style.css">
</head>
<body>
    <img src="https://ih1.redbubble.net/image.4555068436.6304/bg,f8f8f8-flat,750x,075,f-pad,750x1000,f8f8f8.jpg" width="200">
    <h1>Failed to Solve PoW Challenge</h1>
    <p>Oopsy daisy! You failed to solve the Proof-of-Work challenge. You are probably a bot.</p>
    <hr>
    <p>If we got that wrong, we're sorry - July is specifically designed to block A.I. (and other) Scrapers from scraping data off this website using a Proof-of-Work challenge - which you failed to solve.</p>
    <hr>
    <p>If you are, in fact, a human, please try again by <button onclick="location.back()">clicking here</button>. If that doesn't help, please contact the website administrator.</p>
</body>
    
""" 