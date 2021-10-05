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
    result = json.loads(MessageToJson(info))['matches'][0]['roundstatsall'][23]['map']
    worker.close() # Optional
    return result



