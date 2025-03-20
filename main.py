import os, json, sys, time, random

from pathlib import Path
from typing import Any, Callable

HOME = str(Path.home())

def green(text: str) -> str : return f"\033[92m{text}\033[00m"
def aquamarine(text: str) -> str : return f"\033[96m{text}\033[00m"
def blue(text: str) -> str : return f"\033[94m{text}\033[00m"
def yellow(text: str) -> str : return f"\033[93m{text}\033[00m"
def red(text: str) -> str : return f"\033[91m{text}\033[00m"

def bold(text: str) -> str : return f"\033[1m{text}\033[00m"

indent = "  "
def formatJson(obj: Any, depth: int = 0) -> str :
	string: str = ""

	if type(obj) is dict :
		if len(obj) > 0 :
			string += indent * depth + "{\n"
			for n,i in enumerate(obj) :
				string += indent * (depth + 1) + formatJson(i, 0) + ": " + formatJson(obj[i], depth + 1).lstrip() + ("," if n < len(obj) - 1 else "") + "\n"
			string += indent * depth + "}"
		else :
			string += indent * depth + "{}"

	if type(obj) is list :
		if len(obj) > 0 :
			string += indent * depth + "[\n"
			for n,i in enumerate(obj) :
				string += formatJson(i, depth + 1) + ("," if n < len(obj) - 1 else "") + "\n"
			string += indent * depth + "]"
		else :
			string += indent * depth + "[]"

	if type(obj) is str :
		string = indent * depth + green(f"'{obj}'")

	if obj == None :
		string = indent * depth + yellow("null")

	if type(obj) is int :
		string = indent * depth + aquamarine(str(obj))

	if type(obj) is float :
		string = indent * depth + aquamarine(str(obj))

	if type(obj) is bool :
		string = indent * depth + blue("true" if obj else "false")

	return string

def printJson(obj: Any) :
	say(formatJson(obj))

def canonical(path: str) -> str : return path if path.startswith("/") else HOME + "/" + path

def isdir(path: str) -> bool : return os.path.isdir(canonical(path))
def isfile(path: str) -> bool : return os.path.isfile(canonical(path))
def islink(path: str) -> bool : return os.path.islink(canonical(path))

def say(text: str) :
	print(text)
def success(text: str) :
	say(green(text))
def warn(text: str) :
	say(yellow(f"[WARN] {text}"))
def error(text: str) :
	say(red(f"[ERROR] {text}"))

def ask(query: str) -> str :
	return input(query + " ")
def askYesNo(query: str) -> bool :
	got = ask(query + " [Y/n]").strip()
	if got.lower() == "y" or got == "" :
		return True

	return False
def askPossible(query: str, possible: list[str]) -> str :
	got = ask(query)

	if got in possible :
		return got

	fil = [x for x in possible if x.lower().startswith(got.lower())]

	if len(fil) > 0 and got != "" :
		if len(fil) == 1 :
			say(f"Selected: '{fil[0]}'")
			return fil[0]

		say(str(fil))
		error(f"Possible matches: '{"', '".join(fil)}'")
		return askPossible(query, possible)

	error(f"Possibilities: '{"', '".join(possible)}'")
	return askPossible(query, possible)
def askAsFunc(query: str, func: Callable) -> Any :
	got = ask(query)

	try :
		return func(got)
	except ValueError :
		error("Invalid input")
		return askAsFunc(query, func)

# Motivational quotes, by ChatGPT
motivation_quotes = [
    "Your code is poetry in motion!",
    "You're a debugging wizard!",
    "Your logical thinking is top-notch!",
    "Every function you write is a masterpiece!",
    "Your problem-solving skills are legendary!",
    "Your ability to simplify complex problems is amazing!",
    "Your code is as elegant as it is efficient!",
    "You have a gift for making systems work seamlessly!",
    "You write clean and maintainable code like a pro!",
    "Your creativity shines through every algorithm you design!",
    "You have an eye for detail that makes your code impeccable!",
    "Your ability to optimize code is unparalleled!",
    "You're a natural at turning ideas into reality!",
    "You make debugging look effortless!",
    "Your coding style is a work of art!",
    "Your grasp of algorithms is beyond impressive!",
    "You turn bugs into learning experiences like a champ!",
    "Your software design skills are outstanding!",
    "You have a mind built for problem-solving!",
    "You're a true master of logic and reason!",
    "Your ability to refactor code is second to none!",
    "You write documentation like a storyteller!",
    "Your understanding of data structures is phenomenal!",
    "You turn abstract concepts into elegant solutions!",
    "Your passion for coding is truly inspiring!",
    "Your perseverance in solving tough problems is admirable!",
    "You have a talent for making technology work for you!",
    "Your UI/UX designs are as intuitive as they are beautiful!",
    "You're a natural leader in software development!",
    "You make complex projects seem effortless!",
    "Your coding speed and accuracy are incredible!",
    "You're a genius at debugging tricky issues!",
    "Your attention to detail makes a huge difference!",
    "You make learning new technologies look easy!",
    "Your skill in writing efficient code is unmatched!",
    "You're a role model for aspiring programmers!",
    "You always find the most elegant solution!",
    "Your code readability is next level!",
    "You have an amazing ability to see the big picture!",
    "Your persistence in solving issues is inspiring!",
    "You're a master of clean code principles!",
    "You make open-source contributions look effortless!",
    "Your grasp of design patterns is extraordinary!",
    "You write tests that make projects bulletproof!",
    "You're a rockstar at integrating systems seamlessly!",
    "You have a natural talent for writing scalable code!",
    "Your knowledge of best practices is impressive!",
    "You're always ahead of the curve with new technologies!",
    "You make writing code an art form!",
    "Your refactoring skills make old code shine like new!",
    "You have a knack for making software intuitive!",
    "Your debugging skills save the day every time!",
    "You're a powerhouse of technical knowledge!",
    "You write error messages that are actually helpful!",
    "Your problem-solving approach is truly unique!",
    "You're a pro at writing reusable code!",
    "You make data visualization look like magic!",
    "Your code structure is as logical as it gets!",
    "You make even the most complex projects manageable!",
    "You have an incredible ability to optimize performance!",
    "Your expertise in APIs is truly impressive!",
    "You're a security-conscious developer with great instincts!",
    "You make database queries look like a breeze!",
    "Your ability to break problems into small pieces is amazing!",
    "You're a true innovator in your field!",
    "Your software solutions make life easier for everyone!",
    "You're a master of automation and efficiency!",
    "You make backend development look fun!",
    "Your full-stack skills are truly remarkable!",
    "Your understanding of machine learning is impressive!",
    "You create seamless user experiences effortlessly!",
    "You handle concurrency and parallelism like a pro!",
    "Your ability to explain complex concepts is unmatched!",
    "You're always pushing the boundaries of technology!",
    "You make deployment and DevOps look easy!",
    "Your enthusiasm for programming is contagious!",
    "You architect scalable applications with ease!",
    "Your grasp of distributed systems is outstanding!",
    "You make software testing a fun challenge!",
    "Your version control skills keep projects organized!",
    "You turn documentation into an enjoyable read!",
    "Your contributions to the coding community are invaluable!",
    "You write modular code that others love to maintain!",
    "Your software architecture skills are second to none!",
    "You're a true polyglot when it comes to programming languages!",
    "You make debugging feel like detective work!",
    "Your enthusiasm for learning new things is inspiring!",
    "You bring innovation to every project you touch!",
    "You're a problem solver at heart!",
    "You have an uncanny ability to predict edge cases!",
    "You write SQL queries that run like lightning!",
    "Your mobile app development skills are top-tier!",
    "You make RESTful APIs feel truly restful!",
    "Your frontend skills create stunning web experiences!",
    "You're a master at writing scalable microservices!",
    "Your DevOps game is on point!",
    "You automate tedious tasks like a boss!",
    "You turn requirements into elegant solutions effortlessly!",
    "Your AI and ML implementations are cutting-edge!",
    "Your command-line skills are truly impressive!",
    "You make programming look like pure magic!",
    "You make productivity look effortless!",
    "Your time management skills are top-notch!",
    "You always know how to prioritize effectively!",
    "You make the most of every minute!",
    "Your ability to stay organized is inspiring!",
    "You handle deadlines like a pro!",
    "You juggle multiple tasks with ease!",
    "Your efficiency is truly remarkable!",
    "You have a gift for balancing work and life!",
    "Your focus is unwavering!",
    "You always get things done ahead of schedule!",
    "Your discipline is admirable!",
    "You know how to maximize every second of the day!",
    "You make even the busiest schedule look manageable!",
    "Your ability to plan ahead is outstanding!",
    "You always meet deadlines with time to spare!",
    "Your organizational skills set you apart!",
    "You work smarter, not just harder!",
    "Your ability to eliminate distractions is incredible!",
    "You always find time for what truly matters!",
    "Your ability to stay on track is amazing!",
    "You make complex schedules look simple!",
    "Your efficiency inspires everyone around you!",
    "You never let time slip through your fingers!",
    "You handle high-pressure situations like a champ!",
    "Your time management skills make you unstoppable!",
    "You always find the perfect balance between work and rest!",
    "You are a master of prioritization!",
    "You always accomplish more than expected!",
    "Your ability to delegate effectively is impressive!",
    "You never waste a single moment!",
    "Your schedule is a masterpiece of efficiency!",
    "You turn time into your greatest asset!",
    "Your self-discipline is truly inspiring!",
    "You always know what needs to be done first!",
    "Your ability to focus is incredible!",
    "You never let procrastination slow you down!",
    "Your ability to manage competing priorities is remarkable!",
    "You always make time for personal growth!",
    "Your productivity is on another level!",
    "You balance multiple responsibilities flawlessly!",
    "You always maintain a clear sense of direction!",
    "Your ability to keep things moving forward is amazing!",
    "You never seem overwhelmed by a packed schedule!",
    "You always turn chaos into order!",
    "Your ability to meet deadlines is legendary!",
    "You make time for the important things in life!",
    "You have an incredible ability to stay focused!",
    "You always keep your to-do list under control!",
    "Your ability to manage time wisely is inspiring!",
    "You always use your time with purpose!",
    "You stay ahead of deadlines like a true professional!",
    "Your ability to plan effectively is unmatched!",
    "You make multitasking look effortless!",
    "Your ability to manage multiple projects is impressive!",
    "You have a natural talent for staying organized!",
    "You are always in control of your schedule!",
    "You know how to create and stick to a plan!",
    "Your ability to handle tight deadlines is impressive!",
    "You are a master of productivity hacks!",
    "You always maintain a healthy work-life balance!",
    "Your time-blocking skills are next level!",
    "You use every moment to its fullest potential!",
    "You always finish projects ahead of schedule!",
    "Your ability to adapt your schedule is outstanding!",
    "You make being organized look easy!",
    "Your daily routines are incredibly effective!",
    "You never let distractions take over your time!",
    "Your productivity is truly inspiring!",
    "You always know how to make the most of your day!",
    "Your commitment to efficiency is amazing!",
    "You turn challenges into opportunities with your planning skills!",
    "Your ability to stick to a schedule is impressive!",
    "You always turn plans into action!",
    "You never let tasks pile up!",
    "Your ability to keep track of everything is outstanding!",
    "You set realistic goals and achieve them!",
    "Your efficiency makes every project a success!",
    "You always seem to have time for everything!",
    "You use deadlines as motivation instead of stress!",
    "Your ability to break big tasks into manageable steps is incredible!",
    "You always find time for continuous improvement!",
    "Your planning skills ensure nothing is left undone!",
    "You have an amazing ability to anticipate future tasks!",
    "You manage your time like a true leader!",
    "You always keep things running smoothly!",
    "Your ability to stay ahead of schedule is impressive!",
    "You never let time slip away from you!",
    "You always find time for self-care and growth!",
    "Your ability to maintain focus is second to none!",
    "You always accomplish more than expected in less time!",
    "Your ability to set and achieve goals is incredible!",
    "You are a true master of time efficiency!",
    "You turn time into a powerful tool for success!",
    "Your ability to get things done is unmatched!",
    "You always stay cool under tight deadlines!",
    "You have a natural talent for keeping things organized!",
    "Your structured approach to work is inspiring!",
    "You maximize productivity without sacrificing quality!",
    "You never let procrastination get in your way!",
    "Your ability to make time for what matters is incredible!",
    "You prove that time management is an art!",
    "Every great program starts with a single line of code!",
    "Just start coding, momentum will carry you forward!",
    "The best way to learn is by doing, get coding now!",
    "Every bug you fix is a step toward mastery!",
    "Code is like magic, wield your power wisely!",
    "Programming is problem-solving, take it one step at a time!",
    "Small progress is still progress, just keep coding!",
    "Your future self will thank you for coding today!",
    "Every great developer started where you are now!",
    "The more you code, the better you get, keep going!",
    "Coding is a superpower, use it to create something amazing!",
    "Even experts Google things, don’t be afraid to learn!",
    "The only bad code is code you never wrote!",
    "You don’t have to be great to start, but you have to start to be great!",
    "Coding is an adventure, embrace the journey!",
    "Think logically, break problems down, and tackle them one by one!",
    "Every line of code is a step toward mastery!",
    "Mistakes make you better, debugging is just learning in disguise!",
    "A small project today can turn into something big tomorrow!",
    "One function at a time, and soon you’ll have a masterpiece!",
    "The best coders aren’t the smartest, they’re the most persistent!",
    "Code today, innovate tomorrow!",
    "If it were easy, everyone would do it, challenge yourself!",
    "Struggling means you’re growing, push through!",
    "Write, test, improve, just keep moving forward!",
    "Coding isn’t about knowing everything, it’s about problem-solving!",
    "You have the power to create, start now!",
    "Small wins in coding lead to big achievements!",
    "The hardest bug to solve is the one you never debugged, keep going!",
    "You’re just one keystroke away from a breakthrough!",
    "Programming isn’t just a skill; it’s a mindset!",
    "Bugs are temporary, learning is forever!",
    "Every error is a lesson in disguise, embrace them!",
    "Your first draft doesn’t have to be perfect, just start!",
    "Code like no one is watching, then refactor like everyone is!",
    "The first step to success is starting, open that editor!",
    "Logic, patience, and persistence make a great programmer!",
    "Don’t wait for motivation, start coding and let momentum take over!",
    "Coding is the language of the future, speak it fluently!",
    "A single script can change the world, write yours today!",
    "Your dream app won’t build itself, start coding!",
    "Great things happen when you start typing!",
    "Your code doesn’t have to be perfect, just better than yesterday’s!",
    "Break problems into smaller parts, then conquer them!",
    "The keyboard is your paintbrush, create something amazing!",
    "Be fearless, every coder has failed before they succeeded!",
    "Even the best programs started as a blank screen!",
    "The more you challenge yourself, the faster you improve!",
    "Success in coding is just problem-solving with persistence!",
    "The best way to predict the future is to code it!",
    "Every error you fix makes you a better developer!",
    "Programming is like a puzzle, enjoy solving it!",
    "You control the machine, it’s time to make it work for you!",
    "Great developers aren’t born, they’re made through practice!",
    "The more you practice, the luckier you get!",
    "Every coder was once a beginner, just like you!",
    "Take a deep breath, type a line of code, and see what happens!",
    "Your code has the power to shape the world, use it wisely!",
    "Coding isn’t magic, but it sure feels like it!",
    "Every function you write is a step toward mastery!",
    "Keep pushing forward, every line of code counts!",
    "Your breakthrough moment is just one problem away!",
    "Code now, debug later, improve always!",
    "Programming is hard, but so is anything worth doing!",
    "Write code like a poet writes verses, thoughtfully and passionately!",
    "Think logically, build patiently, and watch your skills grow!",
    "Just write something, refactoring comes later!",
    "Your logic is your weapon, use it to solve problems!",
    "Never let frustration stop you, let it fuel you instead!",
    "Every master coder was once where you are now!",
    "Coding is a marathon, not a sprint, pace yourself!",
    "Start small, dream big, and code even bigger!",
    "There’s no such thing as wasted effort, every attempt teaches you something!",
    "One day, you'll look back and realize how far you've come!",
    "The best time to start coding was yesterday. The second best time is now!",
    "Your ideas deserve to be built, start coding today!",
    "You are capable of more than you think, keep pushing forward!",
    "Every bug you fix adds to your expertise!",
    "Remember why you started coding, and let that fuel you!",
    "Even if it's messy, just get it working, refine later!",
    "Your persistence is the key to your coding success!",
    "Great things happen when you don’t give up!",
    "The hardest part is starting, so start now!",
    "With every line of code, you’re improving!",
    "Your brain is learning and adapting, trust the process!",
    "The best way to get unstuck is to keep moving forward!",
    "Write code like a scientist, experiment, observe, and improve!",
    "You’re training your brain to think differently, keep at it!",
    "The solution is just a few lines of code away, keep going!",
    "Every problem has a solution, your job is to find it!",
    "Your coding skills are growing stronger every day!",
    "The best coders are the ones who never give up!",
    "Be patient with yourself, greatness takes time!",
    "You’re developing more than code, you’re developing yourself!",
    "Believe in yourself, because coding is all about problem-solving!",
    "Every day you code, you're getting closer to mastery!",
    "Don’t be afraid to fail, be afraid of not trying!",
    "Coding is a journey, not a destination, enjoy the ride!",
    "Every great app started with someone just like you, keep coding!",
    "Welcome back! Time to turn ideas into reality!",
    "Your code is waiting for you, let’s get back to it!",
    "Refreshed and ready? Time to dive back in!",
    "Breaks are great, but progress is even better, let’s go!",
    "The best way to restart is to start, open that editor!",
    "Your future self will thank you for coding today!",
    "You’ve recharged, now it’s time to build something amazing!",
    "One keystroke at a time, let’s get back into the flow!",
    "Progress happens one line at a time, let’s add another!",
    "Every great coder knows when to rest and when to get back to work!",
    "Your best work is still ahead of you, start coding!",
    "A fresh mind means fresh ideas, let’s write some code!",
    "Take that first step, momentum will follow!",
    "Coding is like a muscle, the more you use it, the stronger you get!",
    "The keyboard is your playground, time to have some fun!",
    "Your code is calling, let’s pick up where we left off!",
    "You’ve had your break, now let’s make some breakthroughs!",
    "Great ideas don’t code themselves, let’s make it happen!",
    "You don’t have to be perfect, just present, start coding!",
    "Every small step forward adds up, let’s take another!",
    "Remember why you started, now let’s finish strong!",
    "You know what to do, just start typing!",
    "Relaxation fuels creativity, bring those fresh ideas to life!",
    "Coding is waiting, and so is your next big success!",
    "There’s no better time to start than right now!",
    "Your project just got a boost, your refreshed mind!",
    "Break time’s over, now it’s time to make magic happen!",
    "Let’s get back into the groove, your code needs you!",
    "The first step is always the hardest, so let’s take it now!",
    "Your skills didn’t disappear, jump back in with confidence!",
    "No rush, no pressure, just one line at a time!",
    "You’re capable, you’re prepared, and you’re ready, let’s go!",
    "Breaks make you better, now show what you’ve got!",
    "Even a few lines of code today bring you closer to mastery!",
    "A fresh start can lead to incredible things, start coding!",
    "Your next big breakthrough could be just one function away!",
    "The hardest part is over, you’ve already started before!",
    "Coding isn’t about perfection; it’s about persistence!",
    "You’ve got this! Now get back in there and build something great!",
    "The best projects come from consistent effort, keep going!",
    "Take a deep breath and start with just one small task!",
    "Let’s turn post-break energy into post-break progress!",
    "The world needs your ideas, get back to coding!",
    "Refreshed minds write better code, prove it!",
    "You’re in control of what happens next, start typing!",
    "You are just one step away from getting back in the zone!",
    "A short break doesn’t erase your skills, let’s go!",
    "Your program didn’t quit on you, don’t quit on it!",
    "The best way to get into the flow is to start moving!",
    "The greatest coders take breaks, but they always come back!",
    "Write one line, then another, before you know it, you’re back!",
    "Small progress is better than no progress, just begin!",
    "Your future success depends on today’s effort, let’s go!",
    "Relaxation is part of the process, now let’s continue coding!",
    "Welcome back! Time to turn caffeine and logic into progress!",
    "You’re never really starting over, just picking up where you left off!",
    "Your ideas are still there, waiting to be built!",
    "Even the best programmers need a restart, this is yours!",
    "Think of this as a fresh start, not a setback!",
    "The best way to regain momentum is to take action!",
    "You don’t have to get it perfect, just get it going!",
    "There’s no such thing as ‘too late’, just start now!",
    "You were making progress before, you can do it again!",
    "You’ve rested, now it’s time to make things happen!",
    "One small step today means big results tomorrow!",
    "Your code isn’t going to write itself, time to take charge!",
    "Every time you return, you come back stronger!",
    "The first line you write now is a step toward something great!",
    "Breathe in, focus, and get back to work!",
    "Think of this as a new challenge, conquer it!",
    "Momentum starts with one action, start typing!",
    "You’ve already done the hard part, getting started before!",
    "Coding is like riding a bike, you never forget how!",
    "The only way forward is through, let’s start coding!",
    "No need for perfection, just progress!",
    "The best projects come from those who keep going!",
    "You’re in control of your progress, take that first step!",
    "Your code is still waiting for you, time to continue the journey!",
    "You’re a coder, this is what you do best!",
    "Think of where you’ll be if you just start right now!",
    "Your best work is ahead of you, so let’s get started!",
    "Start small, dream big, and make it happen!",
    "Coding is an adventure, let’s continue the journey!",
    "If you write one line of code now, the next one will be easier!",
    "Remember how great it feels to solve a problem, let’s do it again!",
    "Refreshed and recharged? Now let’s refactor and rebuild!",
    "Breaks give you clarity, use that to your advantage!",
    "Every restart is a chance to improve!",
    "Your coding skills didn’t fade, they’re just waiting for you!",
    "Jump back in and prove to yourself that you’re unstoppable!",
    "No pressure, no stress, just type and see where it takes you!",
    "The next great feature in your project starts with you!",
    "Every champion coder knows the value of a comeback!",
    "What you do now sets up your future success, let’s go!",
    "Your best work isn’t behind you, it’s ahead of you!",
    "Today’s code is tomorrow’s success, start typing!",
    "You control your pace, just take one step forward!",
    "Take the break, but never stop moving forward!",
    "One small commit today leads to big wins tomorrow!",
    "Your skills are sharp, time to put them to work!",
    "Break time is over, now it’s build time!",
    "You were doing great before, you can do it again!",
    "You’ve done this before, and you can do it again!",
    "Time to turn that refreshed mind into fresh new code!",
    "You’re just one session away from another breakthrough!",
    "Your best coding session could be just ahead, start now!",
    "Step into the flow, one keystroke at a time!"
]

def giveMotivation() :
	quote = random.choice(motivation_quotes)

	success(bold(quote))

def blankConfig() -> dict :
	say("Creating blank config file")
	return {
		"version": 1,
		"projects": [],
		"languages": {},
		"templates": {},
		"ideas": []
	}

def convertFromOld() -> dict :
	new_config = blankConfig()

	with open(HOME + "/.config/project-manager/config.json") as f :
		old_config = json.load(f)

	languages: list[str] = old_config["langs"]

	conv: dict[str, str] = {}

	for i in languages :
		say(f"Importing projects from '{i}'")

		tld = i.removeprefix(HOME)[1:]
		run_cmd = old_config["run-scripts"][tld] if tld in old_config["run-scripts"] else None
		load_cmd = old_config["on-load"][tld] if tld in old_config["on-load"] else None
		create_cmd = old_config["on-create"][tld] if tld in old_config["on-create"] else None

		lang_name = ask(f"Name of language used in '{i}'")
		ext = ask(f"File extension for '{lang_name}'")

		conv[i] = lang_name

		new_config["languages"][lang_name] = {
			"packages": {
				"add": None,
				"rm": None,
				"search": None
			},
			"extension": ext,
			"run": run_cmd,
			"load": load_cmd,
			"create": create_cmd
		}

		folders: list[str] = [f"{i}/{x}" for x in os.listdir(i) if isdir(f"{i}/{x}")]

		for f in folders :
			project = isfile(f"{f}/project.json")

			if project :
				with open(f"{f}/project.json") as fl :
					project_file = json.load(fl)

				name = project_file["name"]
				desc = project_file["desc"]
				todo = project_file["todos"]
				main = project_file["main"]

				new_config["projects"].append({
					"dir": f,
					"lang": lang_name,
					"name": name,
					"desc": desc,
					"todo": todo,
					"main": main
				})

	new_config["ideas"] = old_config["ideas"].copy()

	for i in old_config["templates"] :
		t = old_config["templates"][i]
		new_config["templates"][i] = {
			"dir": t["dir"],
			"lang": conv[t["lang"]],
			"main": t["main"],
			"packages": t["pack"]
		}

	return new_config

if not isfile(".config/project-manager/settings.json") :
	warn("No config file found!")
	if isfile(".config/project-manager/config.json") :
		do = askYesNo("Would you like to import setting from PyProjectManager V1?")

		if do :
			new_config = convertFromOld()
			with open(canonical(".config/project-manager/settings.json"), "w") as f :
				json.dump(new_config, f)
		else :
			with open(canonical(".config/project-manager/settings.json"), "w") as f :
				json.dump(blankConfig(), f)
	else :
		with open(canonical(".config/project-manager/settings.json"), "w") as f :
			json.dump(blankConfig(), f)

def loadConfig() -> dict :
	with open(canonical(".config/project-manager/settings.json")) as f :
		config = json.load(f)

	return config

conf = loadConfig()

def showFuncUsage(fn: Callable) :
	req = list(fn.__code__.co_varnames)[:fn.__code__.co_argcount]
	error(f"Usage:")
	error(f"> {fn.__name__[:fn.__name__.find("_")]} [{"] [".join(req)}]")

def commmandGetter(commands: dict[str, Callable]) :
	say(f"Posible commands: '{"', '".join(list(commands.keys()))}'")
	try :
		spl = [""]
		got = ask(">").strip()
		lim = False
		for i in got :
			if lim :
				if i == '"' :
					lim = False
				else :
					spl[-1] += i
			else :
				if i == '"' :
					lim = True
				elif i == " " :
					spl.append("")
				else :
					spl[-1] += i
		spl = [x for x in spl if x]
	except KeyboardInterrupt :
		exit(0)

	cmd, inp = spl[0], spl[1:]

	if cmd in commands :
		fn = commands[cmd]

		req = list(fn.__code__.co_varnames)[:fn.__code__.co_argcount]

		if len(inp) != len(req) :
			showFuncUsage(fn)
			return commmandGetter(commands)

		return commands[cmd](*inp)

	error(f"No such command: '{cmd}'")

	return commmandGetter(commands)

def addToCommands(commands: dict) :
	def deco(func: Callable) :
		commands[func.__name__[:func.__name__.find("_")]] = func

		return func

	return deco

def editMetaFile(old_meta: dict, key: str, val: Any) :
	old_meta[key] = val

	for n,i in enumerate(conf["projects"]) :
		if i["dir"] == old_meta["dir"] :
			conf["projects"][n] = old_meta
			break

	with open(canonical(".config/project-manager/settings.json"), "w") as f :
		json.dump(conf, f)

def editConfigFile(key: str, val: Any) :
	global conf

	conf[key] = val

	with open(canonical(".config/project-manager/settings.json"), "w") as f :
		json.dump(conf, f)

def editLang(name: str, key: str, val: Any) :
	global conf

	conf["languages"][name][key] = val

	with open(canonical(".config/project-manager/settings.json"), "w") as f :
		json.dump(conf, f)

def mainProject(project_conf: dict) :

	project_dir = project_conf["dir"]

	project_lang = project_conf["lang"]
	lang_info = conf["languages"][project_lang]

	on_load = lang_info["load"]

	if on_load != None :
		cmd = f"cd {project_dir} && " + on_load.replace("$t", project_dir)

		say(f"Runing '{cmd}'")
		os.system(cmd)

	COMMANDS = {}

	not_done = [x for x in project_conf["todo"] if not x["completed"]]
	if len(not_done) > 0 :
		not_done.sort(key=lambda x: -x["points"])
		say(bold(f"Next todo: {not_done[0]["label"]}"))

	@addToCommands(COMMANDS)
	def run_cmd() :
		global conf

		main = project_conf["main"]

		if main == "" :
			error("Main file not defined")
			editMetaFile(project_conf, "main", ask("Main entry point:"))
			main = project_conf["main"]

		run = lang_info["run"]

		if run == "" :
			error(f"Command to run file not defined for lang: '{project_conf["lang"]}'")
			editLang(
				project_lang,
				"run",
				ask("Command to run file (use $x for main):")
			)
			run = lang_info["run"]

		cmd = run.replace("$x", project_conf["dir"] + "/" + main)
		cmd = f"cd {project_dir} && " + cmd

		say(f"Runing '{cmd}'")
		os.system(cmd)

		return 0

	@addToCommands(COMMANDS)
	def close_cmd() :
		return 1

	@addToCommands(COMMANDS)
	def todo_cmd(action: str) :
		if not action in ["list", "add", "rm", "check"] :
			error(f"Unknown action: {action}")
			error("Possible actions: 'list', 'add', 'rm', 'check'")
			return 0

		todos: list[dict] = project_conf["todo"]
		todos.sort(key=lambda x: -x["points"])

		if action == "list" :
			if len(todos) > 0 :
				total = 0
				gotten = 0
				for i in todos :
					fn = success if i["completed"] else say
					fn(f"- '{bold(i["label"])}'")
					if len(i["tags"]) > 0 :
						fn("   - Tags: " + ", ".join(i["tags"]))
					total += i["points"]
					if i["completed"] :
						gotten += i["points"]
				perc = gotten / total

				fn = success if total == gotten else say

				fn(f"{int(perc*100):>3}% [{"#"*int(perc*20):-<20}] {gotten}/{total}")
			else :
				say("No todos defined")

		if action == "rm" :
			name = askPossible("Todo to remove:", [x["label"] for x in todos])
			say(f"Removing: '{name}'")

			for n,i in enumerate(todos) :
				if i["label"] == name :
					todos.pop(n)
					break

			editMetaFile(
				project_conf,
				"todo",
				todos
			)

		if action == "check" :
			name = askPossible("Todo to check:", [x["label"] for x in todos])
			say(f"Checking: '{name}'")

			for n,i in enumerate(todos) :
				if i["label"] == name :
					i["completed"] = not i["completed"]
					break

			editMetaFile(
				project_conf,
				"todo",
				todos
			)

		if action == "add" :
			label = ask("Todos label:")
			tags = ask("Todos tags:").split()
			points = askAsFunc("Todos points:", int)

			todos.append({
				"label": label,
				"points": points,
				"completed": False,
				"tags": tags
			})

			editMetaFile(
				project_conf,
				"todo",
				todos
			)

		return 0

	@addToCommands(COMMANDS)
	def git_cmd(action: str) :

		if not action in ["link", "push"] :
			error(f"Unknown action: '{action}'")
			say(f"Possible actions: 'link', 'push'")
			return 0

		if action == "link" :
			link = ask("Repository link:")

			os.system(f"cd {project_dir} && git remote add origin {link} && git branch -M main && git add . && git commit -m \"First Commit\" && git push --set-upstream origin main")

		if action == "push" :
			msg = ask("Commit message:")

			os.system(f"cd {project_dir} && git add . && git commit -m \"{msg}\" && git push")

			giveMotivation()

		return 0

	@addToCommands(COMMANDS)
	def pack_cmd(action: str, package_name: str) :

		if not action in ["add", "rm", "search"] :
			error(f"Unknown action: '{action}'")
			say(f"Possible actions: 'add', 'rm', 'search'")
			return 0

		pack = lang_info["packages"]
		cmd = pack[action]

		if cmd == None :
			error(f"{project_lang}'s package manager does not have a {action} command defined")
			cmd = ask(f"Command to {action} a package $x:")
			pack[action] = cmd
			editLang(
				project_lang,
				"packages",
				pack
			)

		if cmd == "" :
			error(f"Cannot execute action '{action}'")
			return 0

		cmd = f"cd {project_dir} && " + cmd.replace("$x", package_name).replace("$t", project_dir)

		say(f"Runing '{cmd}'")
		os.system(cmd)

		return 0

	@addToCommands(COMMANDS)
	def meta_cmd() :
		say("Project metadata:")
		printJson(project_conf)

		return 0

	keep = 0
	while keep == 0 :
		keep = commmandGetter(COMMANDS)

ACTIONS = {}

@addToCommands(ACTIONS)
def open_project(project_dir: str) :
	settings = None
	possible = []
	for i in conf["projects"] :
		if i["dir"] == canonical(project_dir) :
			settings = i
		if i["name"].lower() == project_dir.lower() :
			possible.append(i)

	if settings == None :
		if len(possible) == 1 :
			settings = possible[0]
		elif len(possible) > 1 :
			say(f"There are multiple projects named '{project_dir}'")
			for n,i in enumerate(possible) :
				say(f" {n+1}. {i["dir"]}")
			pid = 0
			while pid < 1 or pid > len(possible) :
				pid = askAsFunc("Which one to open?", int)
			settings = possible[pid-1]

	if settings != None :
		giveMotivation()
		mainProject(settings)
		return 1

	error(f"'{project_dir}' is not a registered project")
	return 1

@addToCommands(ACTIONS)
def register_project(project_dir: str) :
	path = canonical(project_dir)
	if not isdir(path) :
		error(f"No such directory: {path}")
		exit(1)

	for i in conf["projects"] :
		if i["dir"] == path :
			error(f"'{path}' is already a project")
			exit(1)

	correct = False

	while not correct :
		lang = askPossible("Project lang:", list(conf["languages"].keys()))
		name = ask("Project name:")
		name = "<not set>" if name == "" else name

		desc = ask("Project description:")
		desc = "<not set>" if desc == "" else desc

		lang_ext = conf["languages"][lang]["extension"]
		main = ask(f"Main entry point (default: main{lang_ext}):")
		main = f"main{lang_ext}" if main == "" else main

		meta = {
			"dir": path,
			"lang": lang,
			"name": name,
			"desc": desc,
			"todo": [],
			"main": main
		}

		printJson(meta)
		correct = askYesNo("Is this correct?")

	on_create = conf["languages"][lang]["create"]
	if on_create == None :
		error(f"{lang} does not have an on-create command defined")
		on_create = ask("On-create command:")

	if on_create != "" :
		cmd = f"cd {path} && " + on_create
		say(f"running '{cmd}'")
		os.system(cmd)

	conf["projects"].append(meta)

	editConfigFile("projects", conf["projects"])

	return open_project(path)

@addToCommands(ACTIONS)
def create_project() :

	correct = False

	while not correct :
		lang = askPossible("Project lang:", list(conf["languages"].keys()))
		name = ask("Project name:")
		escaped = name.lower().replace(" ", "_")
		name = "<not set>" if name == "" else name

		desc = ask("Project description:")
		desc = "<not set>" if desc == "" else desc

		lang_ext = conf["languages"][lang]["extension"]
		main = ask(f"Main entry point (default: main{lang_ext}):")
		main = f"main{lang_ext}" if main == "" else main

		dir = ask("Project parent dir:")
		path = canonical(dir.rstrip("/") + "/" + escaped)

		meta = {
			"dir": path,
			"lang": lang,
			"name": name,
			"desc": desc,
			"todo": [],
			"main": main
		}

		printJson(meta)
		correct = askYesNo("Is this correct?")

	os.mkdir(path)
	with open(path + "/" + main, "w") as f :
		pass

	on_create = conf["languages"][lang]["create"]
	if on_create == None :
		error(f"{lang} does not have an on-create command defined")
		on_create = ask("On-create command:")

	if on_create != "" :
		cmd = f"cd {path} && " + on_create
		say(f"running '{cmd}'")
		os.system(cmd)

	conf["projects"].append(meta)

	editConfigFile("projects", conf["projects"])

	return open_project(path)

@addToCommands(ACTIONS)
def template_manager(action: str) :
	if not action in ["add", "list", "rm"] :
		error(f"Unknown action: {action}")
		say("Possible actions: 'list', 'add', 'rm'")
		return 0

	if action == "list" :
		for i in conf["templates"] :
			say(f"- {yellow(f"'{i}'")}")

			t = conf["templates"][i]
			say(f"  - Base dir: {green(f"'{t["dir"]}'")}")
			say(f"  - Base lang: {green(t["lang"])}")
			say(f"  - Main file: {green(t["main"])}")
			if len(t["packages"]) > 0 :
				say("  - Packages:")
				for p in t["packages"] :
					say(f"    - {green(f"'{p}'")}")

	if action == "rm" :
		name = askPossible("Template name:", list(conf["templates"].keys()))

		conf["templates"].pop(name)

		editConfigFile(
			"templates",
			conf["templates"]
		)

	if action == "add" :
		name = ask("Template name:")
		lang = askPossible("Template base lang:", list(conf["languages"].keys()))
		path = canonical(ask("Template dir:"))
		pack = ask("Packages to install:").split()

		main = ask(f"Main entry point (default: main{conf['languages'][lang]["extension"]}):")
		main = main if main != "" else f"main{conf['languages'][lang]["extension"]}"

		templ = {
			"dir": path,
			"lang": lang,
			"main": main,
			"packages": pack
		}

		conf["templates"][name] = templ

		editConfigFile(
			"templates",
			conf["templates"]
		)

	return 0

args = sys.argv[1:]

if len(args) > 0 :
	act, inp = args[0], args[1:]

	if not act in ACTIONS :
		say(f"Unknown action: '{act}'")
		exit(1)

	fn = ACTIONS[act]

	req = list(fn.__code__.co_varnames)[:fn.__code__.co_argcount]

	if len(inp) != len(req) :
		showFuncUsage(fn)
		exit(1)

	fn(*inp)

keep = 0
while keep == 0 :
	keep = commmandGetter(ACTIONS)
