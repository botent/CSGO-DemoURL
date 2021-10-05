# Generic Imports
import json
from gevent import monkey
monkey.patch_all()
import logging

# Third-party Imports
from steam.client import SteamClient
from csgo.client import CSGOClient
from csgo import sharecode
from steam.guard import SteamAuthenticator
from steam.steamid import SteamID


LOG = logging.getLogger("Steam Worker")

class SteamWorker():
    """SteamWorker class to initiate Steam Client and access URL to download match demo file using Match Share Code
    """
    def __init__(self) -> None:
        self.logged_on_once = False

        self.steam = client = SteamClient()
        self.cs = cs = CSGOClient(client)
        client.set_credential_location(".")
        
        @client.on('logged_on')
        def start_csgo():
            LOG.info('CSGO Launching')
            cs.launch()

        @cs.on('ready')
        def handle_csgo():
            LOG.info('CSGO Running')
        
        @client.on("error")
        def handle_error(result):
            LOG.info("Logon result: %s", repr(result))

        @client.on("connected")
        def handle_connected():
            LOG.info("Connected to %s", client.current_server_addr)

        @client.on("channel_secured")
        def send_login():
            if self.logged_on_once and self.steam.relogin_available:
                self.steam.relogin()

        @client.on("logged_on")
        def handle_after_logon():
            self.logged_on_once = True

            LOG.info("-"*30)
            LOG.info("Logged on as: %s", client.user.name)
            LOG.info("Community profile: %s", client.steam_id.community_url)
            LOG.info("Last logon: %s", client.user.last_logon)
            LOG.info("Last logoff: %s", client.user.last_logoff)
            LOG.info("-"*30)
            client.run_forever()

        @client.on("disconnected")
        def handle_disconnect():
            LOG.info("Disconnected.")

            if self.logged_on_once:
                LOG.info("Reconnecting...")
                client.reconnect(maxdelay=30)

        @client.on("reconnect")
        def handle_reconnect(delay):
            LOG.info("Reconnect in %ds...", delay)
    
    def authenticatorCode(self, secrets: any):
        """After setting up Steam Guard Authenticator, use this method to get 2FA code to signin using secrets

        Args:
            secrets (any): JSON File path containing your secrets after setting up Steam Guard Authenticator

        Returns:
            str: Steam 2FA/ Auth Code
        """
        secrets = json.load(open(secrets))
        code = SteamAuthenticator(secrets=secrets).get_code()
        return code
    
    def accountIdFetch(self, steamid: int):
        """Fetches account id of the steam id input

        Args:
            steamid (int): User Steam ID

        Returns:
            int: Account ID
        """
        accountid = SteamID(steamid).as_32
        return accountid
    

    def pr_login(self, uname: str, pword: str, code: str):
        """Login to the Steam account

        Args:
            uname (str): Username of your Steam Account
            pword (str): Your password
            code (str): 2FA Code
        """
        self.steam.login(username=str(uname), password=str(pword), two_factor_code=code)

    def close(self):
        """Logout and Disconnect method
        """
        if self.steam.logged_on:
            self.logged_on_once = False
            
            self.steam.logout()
        if self.steam.connected:
            self.steam.disconnect()
            
    def getSharecodeInfo(self, matchcode: str):
        """Decodes Match sharecode to ```getMatchInfo```

        Args:
            matchcode (str): Match share code of CSGO game (starting with CSGO-XXXX-XXXX-XXXX)

        Returns:
            dict: dictionary containing matchid, outcomeid, and token of the entered match share code
        """
        info = sharecode.decode(matchcode)
        return info
    
    def getMatchInfo(self, matchid: any, outcomeid: any, token: any):
        """Match full info with URL to download demo file

        Args:
            matchid (str): unique match id
            outcomeid (str): outcome id of the match
            token (str): token

        Returns:
            [CMsgGCCStrike15_v2_MatchList]: Protobuf object and can be converted to other formats
        """
        self.cs.request_full_match_info(matchid=matchid, outcomeid=outcomeid, token=token)
        resp, = self.cs.wait_event('full_match_info')
        return resp