from gevent import monkey
import gevent
monkey.patch_all()
import core, json
from google.protobuf.json_format import MessageToJson

import logging


LOG = logging.getLogger('SteamProj')

worker = core.SteamWorker()
code = worker.authenticatorCode(secrets='')
worker.pr_login()

def matchInfo():
    matchinfo = worker.getSharecodeInfo(matchcode='')
    matchid = matchinfo['matchid']
    outcomeid = matchinfo['outcomeid']
    token = matchinfo['token']

    info = worker.getMatchInfo(matchid=matchid, outcomeid=outcomeid, token=token)
    
    worker.close() # Optional
    return info

result = matchInfo()
res = MessageToJson(result)
json.dump(res, open('./info.json', 'w'))
