import requests, json, os, getpass
from base64 import b64encode # Shouldn't be necessary, but keep it still.
from console.utils import wait_key
from colorama import Fore, Back, Style
bootupstring = f"""{Fore.CYAN}
_____ _____        __      .                     ▄█                                             
  |     |   \   / /  \     |               ▀██▄ █████▄                                          
  |     |    \ /  |  |     |   _    _       ▄████████▄                                          
  |     |     |   |  | | | |  / \ |/      ▄  ▀██████▀                                           
  |     |     |   |  | ||| |  |_/ |        ▀██████▀                                             
  |     |     |   \__/ \||  \ \__ |   v0.4                                                      
                                     {Style.DIM}(made by verbatimc3){Style.RESET_ALL}{Fore.CYAN}
                             {Style.RESET_ALL}
Press [S] to update, press [R] to refresh
Press [H], [F], or [P] to switch timelines
Press [Q] to quit
"""
if os.path.exists('pref.pow'):
	f = open('pref.pow')
	pref = json.loads(f.read())
	if pref['old_logo'] == 'true':
		bootupstring = f"""{Fore.CYAN}
 __        __                            ▄█
|  \      /  \     |               ▀██▄ █████▄
|  |      |  |     |   _    _       ▄████████▄
|__/ |  | |  | | | |  / \ |/      ▄  ▀██████▀
|    |  | |  | ||| |  |_/ |        ▀██████▀
|     \_| \__/ \||  \ \__ |   v0.3
        |                    {Style.DIM}(made by verbatimc3){Style.RESET_ALL}{Fore.CYAN}
     __/                     {Style.RESET_ALL}
Press [S] to update, press [R] to refresh
Press [H], [F], or [P] to switch timelines
Press [Q] to quit
"""


os.system('clear')
print(bootupstring)
# Login section
if os.path.exists('login.pow'):
	f = open('login.pow', 'r')
	user = json.loads(f.read())
	username = user[0]
	password = user[1]
else:
	username = input('Login\n\nUsername:\n')
	password = getpass.getpass('Password:\n')
	f = open('login.pow', 'w')
	f.write(f'["{username}", "{password}"]')
	f.close()
login_request = requests.get("https://api.owler.cloud/v1/account/verify_credentials.json", auth=(username, password))

# Status code checks
if login_request.status_code == 401:
	print("Failed to authenticate due to bad username or password.")
	exit(1)
elif login_request.status_code == 400:
	print("Failed to authenticate due to a server or validation error.")
	exit(1)
user = json.loads(requests.get("https://api.owler.cloud/v1/users/show.json", auth=(username, password)).text)
bootupstring = bootupstring + f'Logged in as {Fore.RED}@{user["screen_name"]}{Style.RESET_ALL}{Style.DIM} ({user["name"]}){Style.RESET_ALL}\n'
	
# Owler status stuff
url = "https://api.owler.cloud/v1"

def update_status(status):
	post_request = requests.post(f"{url}/statuses/update.json?status={status}&source=TTYOwler", auth=(username, password)) # update request
	return post_request.status_code
		
def get_timeline(timeline):
	timeline_request = requests.get(f"{url}/statuses/{timeline}_timeline.json", auth=(username, password))
	tljson = json.loads(timeline_request.text)
	#tljson = json.loads('[{"user":{"name":"Owler","screen_name":"owler","id":"65c1421a1897e7840ad8d315","protected":false,"profile_image_url":"https://picsum.photos/48/48"},"text":"what are you doing?","id":20,"created_at":"Wed Nov 08 20:48:50 GMT 2023","source":"web","favorited":false},{"user":{"name":"Owler","screen_name":"owler","id":"65c1421a1897e7840ad8d315","protected":false,"profile_image_url":"https://picsum.photos/48/48"},"text":"testing the api!","id":10,"created_at":"Wed Nov 08 20:47:50 GMT 2023","source":"api","favorited":false}]')
	for t in tljson:
		print(f"{Fore.RED}@{t['user']['screen_name']}{Style.RESET_ALL}: \"{t['text']}\" {Style.DIM}(sent from {t['source']}, created on {t['created_at']}){Style.RESET_ALL}")
tl = 'home'
while True:
	os.system('clear')
	print(bootupstring)
	get_timeline(tl)
	h = wait_key()
	if h == 's':
		os.system('clear')
		print(bootupstring)
		status = input(f'{Fore.CYAN}Type an update {Style.DIM}(maximum 140 characters):{Style.RESET_ALL}\n')
		os.system('clear')
		print(bootupstring)
		print('Waiting...')
		h = update_status(status)
		if h == 200:
			print('Successful! Refreshing timeline now')
		else:
			print('Failed (' + h + '). Refreshing timeline now')
	if h == 'h':
		tl = 'home'
	if h == 'p':
		tl = 'public'
	if h == 'f':
		tl = 'friends'
	if h == 'q':
		os.system('clear')
		print(bootupstring)
		print('Seeya later!')
		exit(0)
		