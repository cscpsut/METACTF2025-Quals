import os
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, Response

app = FastAPI(title="SkyFail Flight Management System 3000")

FLAG = os.getenv("FLAG", "METACTF{testing_flag}")

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>✈️ SKYFAIL PILOT REGISTRATION SYSTEM 3000 ✈️</title>
    <style>
        body {
            background: linear-gradient(45deg, #ff00ff, #00ffff, #ffff00, #ff0000);
            animation: rainbow 2s infinite;
            font-family: Comic Sans MS, cursive;
            text-align: center;
            padding: 20px;
        }
        @keyframes rainbow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .container {
            background: rgba(255, 255, 255, 0.9);
            border: 10px solid gold;
            border-radius: 50px;
            padding: 30px;
            margin: 20px auto;
            max-width: 600px;
            box-shadow: 0 0 50px rgba(255, 0, 255, 0.8);
        }
        h1 {
            color: red;
            text-shadow: 5px 5px 10px blue;
            font-size: 3em;
            animation: blink 1s infinite;
        }
        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0; }
        }
        input, select {
            border: 5px solid purple;
            border-radius: 20px;
            padding: 10px;
            margin: 10px;
            font-size: 16px;
            background: yellow;
        }
        button {
            background: linear-gradient(45deg, red, blue, green);
            color: white;
            border: none;
            padding: 20px 40px;
            font-size: 20px;
            border-radius: 30px;
            cursor: pointer;
            animation: bounce 2s infinite;
        }
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-30px); }
            60% { transform: translateY(-15px); }
        }
        .marquee {
            background: black;
            color: lime;
            padding: 10px;
            font-size: 20px;
            animation: scroll 10s linear infinite;
            white-space: nowrap;
            overflow: hidden;
        }
        @keyframes scroll {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        .warning {
            color: red;
            font-size: 24px;
            animation: shake 0.5s infinite;
        }
        @keyframes shake {
            0% { transform: translate(0); }
            25% { transform: translate(-5px, 5px); }
            50% { transform: translate(5px, -5px); }
            75% { transform: translate(-5px, -5px); }
            100% { transform: translate(5px, 5px); }
        }
    </style>
</head>
<body>
    <div class="marquee">🛩️ ULTRA SECURE AVIATION SYSTEM - PROTECTED BY AIR TRAFFIC CONTROL ENCRYPTION 🛩️</div>
    
    <div class="container">
        <h1>✈️ PILOT REGISTRATION ✈️</h1>
        <p class="warning">⚠️ WARNING: THIS FORM IS PROTECTED BY 256-BIT RUNWAY BLOCKCHAIN ENCRYPTION ⚠️</p>
        
        <form method="post" action="/submit">
            <p><strong>Enter your FLIGHT CREDENTIALS:</strong></p>
            
            <p>✈️ Pilot License Number (must be EXACTLY 8 characters):
            <br><input type="text" name="username" required placeholder="PILOT001"></p>
            
            <p>🔐 Cockpit Access Code (must contain 47 special characters):
            <br><input type="password" name="password" required placeholder="mayday123"></p>
            
            <p>🎂 Years of Flight Experience (we need this for... safety):
            <br><input type="number" name="age" required placeholder="25"></p>
            
            <p>🍕 Preferred In-Flight Meal (CRITICAL SAFETY QUESTION):
            <br><select name="pizza" required>
                <option value="">Select...</option>
                <option value="peanuts">Peanuts (classic)</option>
                <option value="pretzels">Pretzels (basic)</option>
                <option value="chicken">Chicken or Fish (fancy)</option>
                <option value="nothing">Nothing (turbulence expected)</option>
            </select></p>
            
            <p>🤖 Are you afraid of flying? (Check if NO):
            <br><input type="checkbox" name="robot" value="no"> I am definitely not afraid of flying</p>
            
            <button type="submit">🛫 SUBMIT TO FLIGHT CONTROL 🛫</button>
        </form>
        
        <p style="font-size: 12px; color: gray;">
            By submitting this form, you agree to follow all FAA regulations and airport security protocols.
            <br>This website is 100% secure and definitely not vulnerable to any hijacking attempts.
            <br>We use the latest Aviation 3.0 Autopilot AI technology.
        </p>
    </div>
    
    <div class="marquee">✈️ POWERED BY BOEING 737 MAX SOFTWARE ✈️</div>
</body>
</html>
"""

LOADING_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Processing Flight Plan...</title>
    <style>
        body {
            background: black;
            color: lime;
            font-family: monospace;
            text-align: center;
            padding: 50px;
        }
        .loading {
            font-size: 24px;
            animation: blink 0.5s infinite;
        }
        .spinner {
            border: 8px solid #333;
            border-top: 8px solid lime;
            border-radius: 50%;
            width: 100px;
            height: 100px;
            animation: spin 1s linear infinite;
            margin: 50px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0; }
        }
        .progress {
            width: 80%;
            height: 30px;
            background: #333;
            margin: 30px auto;
            border-radius: 15px;
            overflow: hidden;
        }
        .progress-bar {
            height: 100%;
            background: lime;
            width: 0%;
            animation: progress 8s linear forwards;
        }
        @keyframes progress {
            0% { width: 0%; }
            10% { width: 15%; }
            30% { width: 45%; }
            60% { width: 72%; }
            90% { width: 96%; }
            95% { width: 98%; }
            100% { width: 99%; }
        }
        .logs {
            text-align: left;
            max-width: 800px;
            margin: 20px auto;
            background: #111;
            padding: 20px;
            border-radius: 10px;
            font-size: 14px;
        }
    </style>
    <script>
        setTimeout(function() {
            window.location.href = '/error';
        }, 8000);
    </script>
</head>
<body>
    <h1 class="loading">🔄 PROCESSING FLIGHT PLAN... 🔄</h1>
    <div class="spinner"></div>
    
    <div class="progress">
        <div class="progress-bar"></div>
    </div>
    
    <div class="logs">
        <div id="log-output">
            > Initializing flight control matrix...<br>
            > Connecting to air traffic control tower...<br>
            > Verifying pilot credentials through 17 different aviation databases...<br>
            > Running advanced background check with TSA...<br>
            > Consulting in-flight meal preference algorithms...<br>
            > Checking weather conditions for flight path...<br>
            > Performing fuel calculation analysis...<br>
            > Waiting for clearance from control tower...<br>
            > Almost ready for takeoff... just need to contact ground crew...<br>
            > ERROR: Flight delayed due to mechanical issues!<br>
        </div>
    </div>
    
    <p>Please wait while our flight control computers process your flight plan...</p>
</body>
</html>
"""

ERROR_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CRITICAL FLIGHT SYSTEM ERROR</title>
    <style>
        body {
            background: red;
            color: white;
            font-family: monospace;
            text-align: center;
            padding: 50px;
            animation: error-flash 0.5s infinite;
        }
        @keyframes error-flash {
            0%, 50% { background: red; }
            51%, 100% { background: darkred; }
        }
        .error-container {
            background: black;
            border: 5px dashed yellow;
            padding: 30px;
            margin: 20px auto;
            max-width: 600px;
            border-radius: 10px;
            box-shadow: 0 0 30px 10px yellow;
        }
        h1 {
            font-size: 3em;
            color: yellow;
            text-shadow: 3px 3px red, 0 0 10px lime;
            animation: shake 0.5s infinite;
        }
        @keyframes shake {
            0% { transform: translate(0, 0); }
            25% { transform: translate(-5px, 5px); }
            50% { transform: translate(5px, -5px); }
            75% { transform: translate(-5px, -5px); }
            100% { transform: translate(5px, 5px); }
        }
        .error-code {
            font-size: 24px;
            color: lime;
            font-family: 'Courier New', monospace;
            margin-bottom: 20px;
        }
        .skull {
            font-size: 100px;
            animation: rotate 2s infinite;
            filter: drop-shadow(0 0 10px yellow);
        }
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .try-again {
            background: blue;
            color: white;
            padding: 15px 30px;
            border: none;
            font-size: 18px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px 2px cyan;
            transition: background 0.2s;
        }
        .try-again:hover {
            background: purple;
        }
    </style>
</head>
<body>
    <div class="error-container">
        <div class="skull">💀✈️</div>
        <h1>FLIGHT CANCELLED</h1>
        <div class="error-code">
            ERROR CODE: 0x0000MAYDAY<br>
            RUNWAY_BLOCKCHAIN_OVERFLOW<br>
            INFLIGHT_MEAL_INVALID (Did you pick "Nothing" again?)<br>
            PILOT_LICENSE_VERIFICATION_FAILED<br>
            <span style="color:orange;">AUTOPILOT ENGAGED... IN PANIC MODE</span><br>
        </div>
        
        <p>Our ultra-advanced aviation AI has detected a catastrophic anomaly in your flight credentials.<br>
        (Or maybe you just typed "password" as your password?)</p>
        <p>The flight control servers are currently grounded due to a flock of rubber ducks on the runway.</p>
        <p>Please sacrifice a paper airplane at the nearest airport shrine.<br>
        Bonus points if it does a barrel roll.</p>
        
        <a href="/" class="try-again">🔄 TRY AGAIN (or just hit F5 furiously)</a>
        
        <p style="font-size: 12px; margin-top: 40px;">
            If this error persists, please contact our ground crew at totally-not-fake@airlinecorp.com<br>
            Or try unplugging the airplane and plugging it back in.<br>
            <span style="color:yellow;">Remember: All complaints must be submitted in Morse code.</span>
        </p>
    </div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content=INDEX_TEMPLATE)

@app.post("/submit")
async def submit_form(
    username: str = Form(...),
    password: str = Form(...),
    age: int = Form(...),
    pizza: str = Form(...),
    robot: str = Form(None)
):
    response = HTMLResponse(content="""
    <html>
    <head>
        <script>
            window.location.href = '/loading';
        </script>
    </head>
    <body>
        <p>Redirecting to loading page...</p>
    </body>
    </html>
    """)
    
    response.headers["X-Flag"] = FLAG
    
    # Troll headers
    response.headers["X-Secret-Flag"] = "nice_try_but_wrong_header_buddy"
    response.headers["Flag"] = "definitely_not_the_real_flag_here"
    response.headers["X-Definitely-Not-The-Flag"] = "this_is_a_decoy_keep_looking"
    response.headers["X-Super-Secret"] = "The flag is totally not here, try harder"
    response.headers["X-Debug-Info"] = "In-flight meal preference logged. No flag here though"
    response.headers["X-Real-Flag"] = "gotcha_this_is_fake_too_pilot"
    response.headers["X-Actual-Flag"] = "stop_checking_every_header_captain"
    response.headers["X-True-Flag"] = "im_running_out_of_aviation_puns"
    response.headers["X-Flight-Data"] = "altitude_secure_no_flags_at_this_level"
    
    return response

@app.get("/loading", response_class=HTMLResponse)
async def loading_page():
    return HTMLResponse(content=LOADING_TEMPLATE)

@app.get("/error", response_class=HTMLResponse)
async def error_page():
    # More troll messages in error page headers
    response = HTMLResponse(content=ERROR_TEMPLATE)
    response.headers["X-Error-Code"] = "error_404_flight_not_found"
    response.headers["X-Debug"] = "Error occurred while processing flight plan: system_crashed_no_flags_here"
    response.headers["X-Failure-Flag"] = "flight_cancelled_successfully"
    response.headers["X-Aviation-Status"] = "grounded_due_to_weather_conditions"
    return response

# Secret endpoint with more trolls
@app.get("/robots.txt")
async def robots_txt():
    response = Response(content="""
User-agent: *
Disallow: /cockpit
Disallow: /flight-deck
Disallow: /air-traffic-control

# Definitely don't look at these headers
# Flight Status: all_flights_delayed_indefinitely
# The real flag is definitely not here, check the control tower
""", media_type="text/plain")
    response.headers["X-Robots-Flag"] = "beep_boop_im_an_autopilot"
    response.headers["X-Disallow"] = "access_denied_restricted_airspace"
    response.headers["X-Flight-Control"] = "tower_to_base_no_clearance_granted"
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)