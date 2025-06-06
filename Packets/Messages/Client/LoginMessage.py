from Utils.Reader import ByteStream
from Packets.Messages.Server.LoginOkMessage import LoginOkMessage
from Packets.Messages.Server.LoginFailedMessage import LoginFailedMessage
from Packets.Messages.Server.OwnHomeDataMessage import OwnHomeDataMessage
from Packets.Messages.Server.MyAlliance import MyAlliance
from Packets.Messages.Server.ClanStream import ClanStream
from Packets.Messages.Server.StartLoadingMessage import StartLoadingMessage
from Logic.Player import Player
from Logic.Battle.LogicBattle import LogicBattle
from Packets.Messages.Server.UDPConnectionInfoMessage import UDPConnectionInfoMessage
from Database.DatabaseManager import DataBase
from Utils.Helpers import Helpers
import time
from Packets.Messages.Server.TeamMessage import TeamMessage
import json
from Packets.Messages.Server.TeamStreamMessage import TeamStreamMessage
from datetime import datetime
from Utils.Utility import Utility
from Packets.Messages.Server.FriendListMessage import FriendListMessage
from Packets.Messages.Server.AllianceTeamsMessage import AllianceTeamsMessage
class LoginMessage(ByteStream):

    def __init__(self, data, device, player):
        super().__init__(data)
        self.device = device
        self.data = data
        self.settings = json.load(open('Settings.json'))
        self.banned_acc = json.load(open('banned_acc.json'))
        self.banned_ip =  json.load(open('banned_ip.json'))
        self.player = player
        
    def save_ban_lists(self):
        with open('banned_acc.json', 'w') as f:
            json.dump(self.banned_acc, f, indent=4)
        with open('banned_ip.json', 'w') as f:
            json.dump(self.banned_ip, f, indent=4)

    def decode(self):
        self.loginPayload = {}
        self.loginPayload["highID"] = self.readInt()
        self.loginPayload["lowID"] = self.readInt()
        self.loginPayload["token"] = self.readString()
        self.loginPayload["majorVersion"] = self.readInt()
        self.loginPayload["minorVersion"] = self.readInt()
        self.loginPayload["build"] = self.readInt()
        self.loginPayload["fingerprintSHA"] = self.readString()
        self.loginPayload["unknownString1"] = self.readString()
        self.loginPayload["deviceID"] = self.readString()
        self.loginPayload["unknownString2"] = self.readString()
        self.loginPayload["device"] = self.readString()
        self.loginPayload["systemLanguage"] = self.readVInt()
        try:
            self.loginPayload["region"] = self.loginPayload["systemLanguage"] = self.readString().split('-')[1]
        except:
            self.loginPayload["region"] = self.loginPayload["systemLanguage"] = "EN"
        self.player.usedVersion = self.loginPayload["majorVersion"]

    def process(self):
        db = DataBase(self.player)
        if self.player.usedVersion == 5:
            if not db.is_token_in_table(self.loginPayload["token"]):
                if self.loginPayload["token"] == b'':
                    self.loginPayload["token"] = self.player.token = Helpers.randomStringDigits(self)
                else:
                    self.player.token = self.loginPayload["token"]
                db.getPlayerId()
                db.createAccount()
            content = open("AssetsServer/lastversion.txt", "r").read()
            lastSHA = content.split("...")[1]
            self.loginPayload["fingerprintData"] = Utility.getFingerprintData(lastSHA)
            # Process login information
            self.player.high_d = self.loginPayload["highID"]
            self.player.low_id = self.loginPayload["lowID"]
            self.player.token = str(self.loginPayload["token"])
            self.player.region = self.loginPayload["region"]
            db.replaceValue("region", self.player.region)
            db.loadAccount()
            if str(self.player.low_id) in self.banned_acc:
                LoginFailedMessage(self.device, self.player,self.loginPayload,self.banned_acc[str(self.player.low_id)]["reason"], 11).Send()
                self.banned_ip[self.device.address[0]] = {"reason": self.banned_acc[str(self.player.low_id)]["reason"]}
                self.save_ban_lists()
                return
            if self.device.address[0] in self.banned_ip:
                LoginFailedMessage(self.device, self.player,self.loginPayload,self.banned_ip[self.device.address]["reason"], 11).Send()
                self.banned_acc[str(self.player.low_id)] = {"reason": self.banned_ip[self.device.address[0]]["reason"]}
                self.save_ban_lists()
                return

            if self.loginPayload["fingerprintSHA"] != lastSHA:
                LoginFailedMessage(self.device, self.player,self.loginPayload,"slay", 7).Send()
                return
            # Send success messages
            LoginOkMessage(self.device, self.player, self.loginPayload).Send()
              # 14109
            
            try:
                battleInfo = db.getBattleInfo([self.player.battleID])[0]
            except:
                self.player.battleID = 0
                db.replaceValue("battleID", 0)
            if self.player.battleID == 0:
                change = True
                if self.player.coinsbooster - int(datetime.timestamp(datetime.now())) <= 0:
                    for x in self.player.homeNotifications:
                        notif = self.player.homeNotifications[x]
                        if notif["ID"] ==97 and notif["type"] ==1:
                            change = False
                    if change:
                        self.player.homeNotifications[len(self.player.homeNotifications)] = {"ID": 97, "type": 1, "seen": False}
                        db.replaceValue("homeNotifications", self.player.homeNotifications)
                OwnHomeDataMessage(self.device, self.player).Send()
                
                ClanStream(self.device, self.player).Send()
                if self.player.club_id != 0:
                    db.onlineMembers(self.player.club_id, 1)
                    AllianceTeamsMessage(self.device, self.player).Send()
                MyAlliance(self.device, self.player).Send()  # 14109
                FriendListMessage(self.device, self.player).Send()
                if self.player.teamID != 0:
                    if db.getGameroomInfo("info") != None:
                        playerInfo = db.getPlayerInfo(self.player.low_id)
                        playerInfo['status'] = 3
                        db.updateGameroomPlayerInfo(self.player.low_id, self.player.teamID, playerInfo)
                        TeamMessage(self.device, self.player).Send()
                        TeamStreamMessage(self.device,self.player).Send()
                    else:
                        self.player.teamID = 0
                        db.replaceValue("teamID", self.player.teamID)
            else:
                StartLoadingMessage(self.device, self.player).Send()
                self.settings = json.load(open('Settings.json'))
                
                if self.settings["UseUDPServer"]:
                    UDPConnectionInfoMessage(self.device, self.player).Send() # its broken so please keep tcp
                else:
                    battle = LogicBattle(self.device, self.player)
                    battle.start()
        else:
            LoginFailedMessage(self.device, self.player, self.loginPayload, " ", 8).Send()
