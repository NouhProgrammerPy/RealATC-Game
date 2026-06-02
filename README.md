# RealATC-Game
This game, made using python, is a game where your objective is to manage the air traffic (hence, Air Traffic Control; ATC). It is a simple game with simple graphics, made to mimic real ATC's radar scope.

<b>This is still a very, very early release.</b> Many more features will be added to make this game better and better.

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

<h2>Have fun!</h2>
