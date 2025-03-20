import os, json, sys, time

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

	fil = [x for x in possible if got.lower() in x.lower()]

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
		spl = ask(">").split()
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
		mainProject(settings)
	else :
		error(f"'{project_dir}' is not a registered project")
		exit(1)

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

	open_project(path)

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

	open_project(path)

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

	exit(0)

commmandGetter(ACTIONS)
