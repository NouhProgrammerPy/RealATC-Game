# RealATC-Game
This game, made using python, is a game where your objective is to manage the air traffic (hence, Air Traffic Control; ATC). It is a simple game with simple graphics, made to mimic real ATC's radar scope.

<b>This is still a very, very early release.</b> Many more features will be added to make this game better and better.

<h1>Setup:</h1>
<ol>
  <li>Download python: https://python.org/download</li>
  <li>Install dependencies:<br />
  `pip install pygame-ce` or `pip3 install pygame-ce`</li>
  <li>Go to releases: https://github.com/NouhProgrammerPy/RealATC-Game/releases and pick the newest version and download the 'ATC-Game.zip' file from the assets</li>
  <li>Extract the files</li>
  <li>Run the extracted 'main.py'</li>
  <li>Enjoy :)</li>
</ol>

<h1>Instructions and Logic:</h1>
Make sure that there is enough seperation between aircraft (minimum 1,000 ft or 3 nm).

For now, you will only get landing traffic (takeoff traffic will be added later).

Click on an aircraft to change its:
<ul>
  <li>Heading</li>
  <li>Altitude</li>
  <li>Speed</li>
  <li>Waypoint</li>
  <li>Landing Clearance</li>
</ul>
Please note the landing logic is still very early development, and may cause weird stuff to happen, just make sure the aircraft is in a realistic enough place to land, and it should be fine.

<h3>Landing Criteria</h3>
<ol>
  <li>Heading +-60 degrees from runway heading</li>
  <li>Aircraft less than or equal to 3,000 ft</li>
  <li>Aircraft speed less than or equal to 250 kts. <b>(Also applies for holding)</b></li>
</ol>

<h3>Holding</h3>
Criterion: Aircraft speed less than or equal to 250 kts.
<h4>Instructions:</h4>
<ol>
  <li>Click on aircraft you want to hold</li>
  <li>Press 'D' on your keyboard</li>
  <li>Type in this format (no spaces): <br />
  "(DIR)/(WYPT)"</li>
</ol>
Example Format:<br />
<br />
Left holding pattern at MOGAV:<br />
L/MOGAV<br />
Right holding pattern at RAGSO:<br />
R/RAGSO<br />

<h3>Aircraft Icons</h3>
The aircraft has a little text block above it to show information, it is in this format:<br />
CALLSIGN<br />
HEADING / TARGET<br />
SIGN ALT / SPEED KT<br />

<img width="57" height="33" alt="image" src="https://github.com/user-attachments/assets/b83bf56a-c74d-446d-9e18-36b88efe139f" /><br />
For example, in the above aircraft,<br />
Callsign is: ETD6802<br />
It is heading at 115 degrees towards TOSBO<br />
It is level at 4,000ft and its speed is 284 kts.<br />


<h2>Have fun!</h2>
