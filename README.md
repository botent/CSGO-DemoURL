# CSGO-DemoURL
## _The easy way to develop your next CSGO Project_
[![GitHub issues](https://img.shields.io/github/issues/botent/CSGO-DemoURL?style=for-the-badge)](https://github.com/botent/CSGO-DemoURL/issues)  [![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge)](https://github.com/botent/CSGO-DemoURL) [![Version](https://img.shields.io/badge/Version-1.11-informational?style=for-the-badge)](https://github.com/botent/CSGO-DemoURL)

Simply get demo file URL of a CSGO Match (which happens to be the toughest part, for some!)


## Tech

This projects uses a number of open source projects to work properly:

- [Steam](https://github.com/ValvePython/steam) - ValvePython/Steam
- [CSGO](https://github.com/ValvePython/csgo) - ValvePython/CSGO
- [Gevent](https://github.com/gevent/gevent) - gevent is a coroutine -based Python networking library that uses greenlet to provide a high-level synchronous API on top of the libev or libuv event loop.


And of course this project itself is open source with a [public repository](https://github.com/botent/CSGO-DemoURL) on GitHub.

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
```python
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

## License

MIT

**Free Software, Hell Yeah!**


