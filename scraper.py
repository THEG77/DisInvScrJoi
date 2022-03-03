import requests, time,json, selenium, re, random, colorama
from colorama import Fore, Back, Style, init
from os import system
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import cfscrape

## Found Tog.gg api
## https://top.gg/servers/{serverid}/join

init(convert = True)
invitecounter = 0
retrycounter = 0
inviteQueue = []
email = "Your Email here"
password = "Your Password Here"
token = "Your Discord Token Here"

def main():
    global invitecounter, token, inviteQueue
    system('cls')
    curtime = datetime.now()
    print(curtime.strftime(Fore.BLUE + "\t\t\t\t\t\t\t%D\n\t\t\t\t\t\t\t%H:%M:%S\t" + Fore.RESET) )
    runningMode = int(input("\nEnter the Mode:\n1.Manual Mode\n2.Automatic Mode\n3.Manual + Joiner\n"))
    if runningMode == 1:
        numberOfTries = int(input("Enter the number of tries(0 for infinite): "))
        if numberOfTries == 0:
            while True:
                try:
                    if invitecounter>40:
                        invitecounter = 0
                        print(Fore.RED,"\n\n!!!!!!SLEEPING SCRAPE BOT FOR 6 HOURS!!!!!!\n\n",Fore.RESET)
                        time.sleep(18000)

                    disboardLinks = scrape_links()
                    time.sleep(1)
                    openlinks(disboardLinks)
                except Exception as e:
                    print(Fore.RED,e,Fore.RESET)
        else:
            while True:
                try:
                    if invitecounter>numberOfTries:
                        invitecounter = 0
                        print(Fore.RED,"\n\n!!!!!!NUMBER OF TRIES COMPLETED ... EXITING NOW!!!!!!\n\n",Fore.RESET)
                        exit()
                        quit()
                        

                    disboardLinks = scrape_links()
                    time.sleep(1)
                    openlinks(disboardLinks)
                except Exception as e:
                    print(Fore.RED,e,Fore.RESET)           
    elif runningMode == 2:
        pass
    elif runningMode == 3:
        #token = input("Enter the Token for joiner!")
        
        while True:
            try:
                if invitecounter>120:
                    invitecounter = 0
                    # print(Fore.RED,"\n\n!!!!!!SLEEPING SCRAPE BOT FOR 2 HOURS!!!!!!\n\n",Fore.RESET)
                    # time.sleep(8000)
                    print("\nJoiner Started...\n")
                    joinerWithReq(inviteQueue)
                    inviteQueue = []
                    #Temporary limit below
                    exit()
                    quit()
                    

                disboardLinks = scrape_links()
                openlinks(disboardLinks)

            except Exception as e:
                print(Fore.RED,e,Fore.RESET)



def joinerWithReq(inviteQueue):
    global token
    localJoinedCounter = 0
    for invite in inviteQueue:
        invite = invite.replace("https://discord.com/invite/", "")
        scraper = cfscrape.create_scraper()
        #r = scraper.get("url")

        headers = {
            'authority': 'discord.com',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAzIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDMiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTA4OTI0LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
            'x-context-properties': 'eyJsb2NhdGlvbiI6IkpvaW4gR3VpbGQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6IjkxODIyOTI2MzA0NjU3NDExMSIsImxvY2F0aW9uX2NoYW5uZWxfaWQiOiI5MjAxNjc0MDQ0MzEwOTM3OTEiLCJsb2NhdGlvbl9jaGFubmVsX3R5cGUiOjB9',
            'x-debug-options': 'bugReporterEnabled',
            'accept-language': 'en-US,en-IN;q=0.9,gu;q=0.8',
            'authorization': token,
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9003 Chrome/91.0.4472.164 Electron/13.4.0 Safari/537.36',
            'x-discord-locale': 'en-US',
            'accept': '*/*',
            'origin': 'https://discord.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://discord.com/channels/@me',
            'cookie': '__dcfduid=b8c5d1870049f8fa68437a816c3227cc; __sdcfduid=eb8e0090f52111ebaa19b3315727ed04722f54cdfe6c03fb9eb2293f08871503350c14e97fff1342f5bdc38681cdff4e; __stripe_mid=536a01eb-4e79-4616-8820-73e2d795dec1183994',
        }

        data = '{}'
        invite = invite.strip('"')
        response = scraper.post(f'https://discord.com/api/v9/invites/{invite}', headers=headers, data=data)
        print(f'https://discord.com/api/v9/invites/{invite}')
        if response.status_code == 200:
            localJoinedCounter+=1
            print(Fore.BLUE + f"[{localJoinedCounter}] " + Fore.RESET +  Fore.GREEN + "SUCCESSFULLY JOINED " + Fore.RESET)

        elif response.status_code == 404:
            print(response.status_code,response.text,"\n\n")
            continue;
        else:
            print(response.status_code,response.text,"\n\n")
        time.sleep(30)

def joiner(inviteQueue):
    global email, password
    Options = webdriver.ChromeOptions()
    Options.add_argument("--window-size=300,800")
    
    # Options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
    Options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # Options.add_experimental_option('useAutomationExtension', False)
    # Options.add_argument("--disable-blink-features=AutomationControlled")
    
    Options.headless = False;
    s=Service('D:\Cool\Cool\Python stuff\DiscordInviteScrapper\driver.exe')
    driver = webdriver.Chrome(service=s,options=Options)
    driver.get("https://discord.com/login")
    time.sleep(5)
    #inputElement = driver.find_element_by_css_selector("#app-mount > div.app-1q1i1E > div > div > div > div > form > div > div > div.mainLoginContainer-1ddwnR > div.block-egJnc0.marginTop20-3TxNs6 > div:nth-child(2) > div > input")
    inputEmail = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/div[1]/div/div[2]/input")
    inputEmail.send_keys(email)
    time.sleep(1)
    inputPassword = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/div[2]/div/input")
    inputPassword.send_keys(password)
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 1080)") 
    submitButton = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/button[2]").click()
    time.sleep(60)
    driver.execute_script("window.scrollTo(0, 1080)") 

    #JOINING SERVERS AT THIS POINT

    #Doing it the jugadoo way..
    for invite in inviteQueue:
        invite = invite.strip('"')
        print(invite)
        driver.get(invite)
        time.sleep(5)
        try:
            driver.find_element(By.CSS_SELECTOR, "div#app-mount > div:nth-of-type(2) > div > div > div > div > section > div > button").click()
        except Exception as e:
            print("Wasnt Click1")
        try:
            driver.find_element(By.CSS_SELECTOR, "div#app-mount > div:nth-of-type(2) > div > div:nth-of-type(2) > div > div > div > section > div > button").click()
        except Exception as e:
            print(e," error in CLICK2 ")
        try:
            driver.find_element(By.XPATH , "//*[@id='app-mount']/div[2]/div[1]/div[1]/div[1]/div[1]/section[1]/div[1]/button[1]").click()
        except Exception as e:
            print("Wasnt CLick3 ")
        # driver.execute_script("window.open('https://google.com');")    
        # driver.close()
        time.sleep(30)

def generateUrlsToScrapeFrom():
    categoryList = ["category/community","tag/community","category/anime-manga","category/music","tag/music","category/technology","category/movies","tag/anime","category/gaming",
                    "tag/gaming","tag/chill","tag/minecraft","tag/social","tag/rp","tag/roleplay","tag/fun","tag/friendly","tag/roblox","tag/friends","tag/games","tag/dating","category/other"]
    randnum = random.randint(3, 12)
    randCategory = random.choice(categoryList)
    base = "https://disboard.org/servers/"
    lastquery = "?sort=member_count"
    combinedquery = base + str(randCategory) + "/" + str(randnum) + lastquery
    print(Back.LIGHTYELLOW_EX ,Fore.MAGENTA,"Query Generated: ", combinedquery,Fore.RESET,Back.RESET)
    return combinedquery
    
    


def scrape_links():
    req = requests.session()
    scraper = cfscrape.create_scraper()
    r = scraper.get(generateUrlsToScrapeFrom())
    baseurl = "https://disboard.org"
    regex = "\/server\/join\/\d{18}"
    matches = re.findall(regex, r.text)
    #print (r,r.text)
    time.sleep(10)
    matchedall = []
    for match in matches:
        matchedall.append(baseurl+match)
    return matchedall

def sendWebHookLink(currenturl):
    currenturl = currenturl.strip('"')
    global invitecounter
    webhook = "https://ptb.discord.com/api/webhooks/758634491090042880/ApzeV4M4QsmtfEpw1DsYIXs68OgZObsFk8pGO6YEQeWvU2m7arrHlN4rwPsWoLfaXLeQ"
    data = {"username":"Invite Got Yoinked",
            "avatar_url" : "https://i.imgur.com/zm15LzT.png",
            "content": "Invite Link "+ currenturl}
    r = requests.post(webhook, json = data)
    print(Fore.LIGHTGREEN_EX,"Response : ",r, Fore.RESET)
    if(r.status_code == 204):
        invitecounter+=1
        print(Fore.BLUE ,"[",invitecounter,"] ",Fore.RESET,Fore.GREEN, "Sent invite link ",currenturl,Fore.RESET)

def openlinks(linkstopen):
    global inviteQueue
    localcounter = 0
    baseurl ="https://disboard.org/site/get-invite/"
    regex = r"\d{18}"

    for link in linkstopen:
        if localcounter>=10:
            time.sleep(5)
            print("Sleeping for 5 s")
            localcounter = 0
        localcounter+=1
        rearEnd = re.findall(regex, link)
        rearEnd = rearEnd[0]
        currentlink = baseurl + rearEnd
        
        req = cfscrape.create_scraper()
        # r = requests.get(currentlink)
        r = req.get(currentlink) 
        finalInviteLink = r.text
        finalInviteLink = finalInviteLink.replace("https://discord.gg/", "https://discord.com/invite/")

        inviteQueue.append(finalInviteLink)
        sendWebHookLink(finalInviteLink)




main()


