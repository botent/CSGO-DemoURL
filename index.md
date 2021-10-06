# CSGO-DemoURL
## _The easy way to develop your next CSGO Project_

Steam is a bit tough when it comes to fetching info. However, they are cool with community projects and this aims to enable other developers save time and efforts (and preferably spend more time parsing demo file data than getting the file itself ;-))

## Installation

This project requires [Python >3.0](https://python.org/) to run.

```sh
git clone https://github.com/botent/CSGO-DemoURL.git
```
or
```sh
pip install csgo-demourl
```

## Usage

1. Initialize the ```SteamWorker()```  instance from ```core.py```
2. Get SteamAuthenticator Code from ```authenticatorCode(secrets=PATH_TO_SECRETS.JSON FILE)``` method
3. Login using ```pr_login(uname=USERNAME, pword=PASSWORD, code=STEAM_AUTHENTICATOR_CODE)``` method
4. Now it is optional but advised to define a function to return Match Demo File URL as ---

```Python

def matchInfo():
    matchinfo = worker.getSharecodeInfo(matchcode=MATCH_SHARE_CODE)
    matchid = matchinfo['matchid']
    outcomeid = matchinfo['outcomeid']
    token = matchinfo['token']

    info = worker.getMatchInfo(matchid=matchid, outcomeid=outcomeid, token=token)
    result = json.loads(MessageToJson(info))['matches'][0]['roundstatsall'][23]['map']
    worker.close() # Optional (to logout and disconnect from Steam Account)
    return result
    
resp = matchInfo() # This gives you the demo URL

```


## Help

I am more than happy to help in any way I can. Feel free to reach out to me via Twitter (@KumarPeri)

![Twitter Follow](https://img.shields.io/twitter/follow/KumarPeri?color=blue&logo=twitter&style=for-the-badge)

## Tech

This projects uses a number of open source projects to work properly:

- [Steam](https://github.com/ValvePython/steam) - ValvePython/Steam
- [CSGO](https://github.com/ValvePython/csgo) - ValvePython/CSGO
- [Gevent](https://github.com/gevent/gevent) - gevent is a coroutine -based Python networking library that uses greenlet to provide a high-level synchronous API on top of the libev or libuv event loop.


And of course this project itself is open source with a [public repository](https://github.com/botent/CSGO-DemoURL) on GitHub.


## License

MIT

**Free Software, Hell Yeah!**


