import heroku3
from time import time
import random
import requests
from git import Repo
from up_qurulum import *
from .astring import main
import os
from telethon import TelegramClient, functions
from telethon.sessions import StringSession
from telethon.tl.functions.channels import EditPhotoRequest, CreateChannelRequest
from asyncio import get_event_loop
from .language import LANG, COUNTRY, LANGUAGE, TZ
from rich.prompt import Prompt, Confirm
import base64

LANG = LANG['MAIN']

def connect(api_key):
    heroku_conn = heroku3.from_key(api_key)
    try:
        heroku_conn.apps()
    except Exception as e:
        hata(LANG['INVALID_KEY'])
        exit(1)
    return heroku_conn

def create_app(heroku_conn):
    appname = "up" + str(time() * 1000)[-4:].replace(".", "") + str(random.randint(0, 500))
    try:
        app = heroku_conn.create_app(name=appname, stack_id_or_name='container', region_id_or_name="eu")
    except requests.exceptions.HTTPError:
        hata(LANG['MOST_APP'])
        exit(1)
    return appname

def hgit(heroku_conn, repo, appname):
    global api
    app = heroku_conn.apps()[appname]
    giturl = app.git_url.replace("https://", f"https://api:{api}@")

    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(giturl)
    else:
        remote = repo.create_remote("heroku", giturl)
    
    try:
        remote.push(refspec="HEAD:refs/heads/master", force=True)
    except Exception as e:
        hata(LANG['ERROR'] + str(e))

    bilgi(LANG['POSTGRE'])
    try:
        app.install_addon(plan_id_or_name='heroku-postgresql:hobby-dev', config={})
        basarili(LANG['SUCCESS_POSTGRE'])
    except requests.exceptions.HTTPError as e:
        hata(LANG['ERROR'] + str(e))
        exit(1)

    return app

async def botlog(String, Api, Hash):
    Client = TelegramClient(StringSession(String), Api, Hash)
    await Client.start()

    KanalId = await Client(CreateChannelRequest(
        title='⚝ 𝑺𝑰𝑳𝑮𝑰 𝑼𝑺𝑬𝑹𝑩𝑶𝑻 ⚝ BotLog',
        about=LANG['AUTO_BOTLOG'],
        megagroup=True
    ))
    KanalId = KanalId.chats[0].id

    Photo = await Client.upload_file(file='uplogo.jpg')
    await Client(EditPhotoRequest(channel=KanalId, photo=Photo))
    msg = await Client.send_message(KanalId, LANG['DONT_LEAVE'])
    await msg.pin()

    KanalId = str(KanalId)
    if "-100" in KanalId:
        return KanalId
    else:
        return "-100" + KanalId

if __name__ == "__main__":
    logo(LANGUAGE)
    loop = get_event_loop()
    api = soru(LANG['HEROKU_KEY'])
    bilgi(LANG['HEROKU_KEY_LOGIN'])
    heroku = connect(api)
    basarili(LANG['LOGGED'])

    # Telegram #
    onemli(LANG['GETTING_STRING_SESSION'])
    stri, aid, ahash = main()
    basarili(LANG['SUCCESS_STRING'])
    baslangic = time()

    # Heroku #
    bilgi(LANG['CREATING_APP'])
    appname = create_app(heroku)
    basarili(LANG['SUCCESS_APP'])
    onemli(LANG['DOWNLOADING'])

    # Repo URL Decoding
    SyperStringKey = "rotaresU/"
    GiperStringKey = "itreqoG/"
    InvalidKey = "moc.buhtig//:ptth" 
    str1 = SyperStringKey + GiperStringKey + InvalidKey
    slicedString = str1[::-1]

    if os.path.isdir("./Userator/"):
        rm_r("./Userator/")
    repo = Repo.clone_from(slicedString, "./repo/", branch="master")
    basarili(LANG['DOWNLOADED'])
    onemli(LANG['DEPLOYING'])
    app = hgit(heroku, repo, appname)
    config = app.config()

    onemli(LANG['WRITING_CONFIG'])
    config['ANTI_SPAMBOT'] = 'False'
    config['ANTI_SPAMBOT_SHOUT'] = 'False'
    config['API_HASH'] = ahash
    config['API_KEY'] = str(aid)
    config['BOTLOG'] = "False"
    config['BOTLOG_CHATID'] = "0"
    config['CLEAN_WELCOME'] = "True"
    config['CONSOLE_LOGGER_VERBOSE'] = "False"
    config['COUNTRY'] = COUNTRY
    config['DEFAULT_BIO'] = "@silgiuserbot"
    config['GALERI_SURE'] = "60"
    config['CHROME_DRIVER'] = "/usr/sbin/chromedriver"
    config['GOOGLE_CHROME_BIN'] = "/usr/sbin/chromium"
    config['HEROKU_APIKEY'] = api
    config['HEROKU_APPNAME'] = appname
    config['STRING_SESSION'] = stri
    config['HEROKU_MEMEZ'] = "True"
    config['LOGSPAMMER'] = "False"
    config['PM_AUTO_BAN'] = "False"
    config['PM_AUTO_BAN_LIMIT'] = "4"
    config['TMP_DOWNLOAD_DIRECTORY'] = "./downloads/"
    config['TZ'] = TZ
    config['TZ_NUMBER'] = "1"
    config['UPSTREAM_REPO_URL'] = "https://github.com/Silgimusicbot/SilgiUserbot"
    config['WARN_LIMIT'] = "3"
    config['WARN_MODE'] = "gmute"
    config['LANGUAGE'] = LANGUAGE

    basarili(LANG['SUCCESS_CONFIG'])
    bilgi(LANG['OPENING_DYNO'])

    try:
        app.process_formation()["worker"].scale(1)
    except Exception as e:
        hata(LANG['ERROR_DYNO'] + str(e))
        exit(1)

    basarili(LANG['OPENED_DYNO'])
    basarili(LANG['SUCCESS_DEPLOY'])
    tamamlandi(time() - baslangic)

    Sonra = Confirm.ask(f"[bold yellow]{LANG['AFTERDEPLOY']}[/]", default=True)
    if Sonra == True:
        BotLog = False
        Cevap = ""
        while Cevap != "3":
            if Cevap == "1":
                bilgi(LANG['OPENING_BOTLOG'])
                KanalId = loop.run_until_complete(botlog(stri, aid, ahash))
                config['BOTLOG'] = "True"
                config['BOTLOG_CHATID'] = KanalId
                basarili(LANG['OPENED_BOTLOG'])
                BotLog = True
            elif Cevap == "2":
                if BotLog:
                    config['LOGSPAMMER'] = "True"
                    basarili(LANG['SUCCESS_LOG'])
                else:
                    hata(LANG['NEED_BOTLOG'])
            
            bilgi(f"\[1] {LANG['BOTLOG']}\n[2] {LANG['NO_LOG']}\n\[3] {LANG['CLOSE']}")
            Cevap = Prompt.ask(f"[bold yellow]{LANG['WHAT_YOU_WANT']}[/]", choices=["1", "2", "3"], default="3")
        basarili(LANG['SEEYOU'])
