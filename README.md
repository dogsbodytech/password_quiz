# Password Quiz

A simple password quiz where the idea is to guess the most commonly used password but where the winner is the hughest unique guess.

## Setup
* Laptop plugged into external monitor/TV
* Stock Ubuntu Desktop 
* Install dependancies `sudo apt install git chromium-browser`
* Login and `git clone https://github.com/dogsbodytech/password_quiz.git`
* Start with `cd password_quiz && python server.py`
* Open up a guest session login
* Open Firefox on the laptop screen and browse to `localhost:8888/form`
* Open chromium on external screen and browse to `localhost:8888/display`
* F11 on both browsers to go full screen
* Zoom Firefox browser a couple of times to make the form clearer

## Afterwards
* Answers are in the entries.txt file, back it up!

## Notes
* Password lists from - https://github.com/danielmiessler/SecLists.git
* I would suggest using the biggest password file possible. Using a 100k list over a 10k list would have only found an extra 5 passwords but people are dissapointed when their password isn't found.

## Bugs
* /display on Firefox flashes with each update (see proposed fix below)
* /display on Chromium loads slowly the first time after a form submission

## ToDo
* I really wish that I could get /logo.png & /bootstrap.min.css to be cached by the browser.  This should also fix the flashing issue with /display on Firefox
* For some reson when running /display on Chromeum and there is a form submission then the page will take ~5 seconds to load!
* We tend to zoom the form in 2-3 times in the browser to make it more readable. I believe this is possible in CSS to save manually doing it.
* Perhaps higher contrast text to make the form more readable from standing up/further away.
* Have a file of anonomised guesses from previous times we used this script in anger so that we can improve it in the future
