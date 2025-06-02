# -*- coding: utf-8 -*-
from Utils.Writer import Writer

from Files.CsvLogic.Cards import Cards
from Files.CsvLogic.Characters import Characters
import json
from Database.DatabaseManager import DataBase
class Profile(Writer):

    def __init__(self, device, player, HighID, LowID, players):
        self.id = 24113
        self.device = device
        self.player = player
        self.HighID = HighID
        self.LowID = LowID
        self.players = players
        super().__init__(self.device)

    def encode(self):

        db = DataBase(self.player)
        for player in self.players:
            if self.LowID == player["low_id"]:
                self.writeVInt(self.HighID) # Player HighID
                self.writeVInt(self.LowID) # Player LowID
                self.writeString(player["name"])
                self.writeVInt(0) # Unknown Data 
                
                self.writeVInt(len(player["unlocked_brawlers"])) 

                for key, brawler_id in player["unlocked_brawlers"].items():
                    self.writeDataReference(16, int(key))
                    self.writeVInt(0)
                    self.writeVInt(brawler_id["Trophies"])  # Trophies 
                    self.writeVInt(brawler_id["HighestTrophies"])  # Trophies for rank
                    powerLevel = 0
                    for card, amount in brawler_id["Cards"].items():
                        if not Cards().isUnlock(card):
                            powerLevel += amount
                    self.writeVInt(powerLevel-1) # Brawler Upgrade Level TOO

                self.writeVInt(7) # Stats Count
                self.writeVInt(1) # Stats Index
                self.writeVInt(player["three_vs_three_wins"]) # Total Victories

                self.writeVInt(2) # Stats Index
                self.writeVInt(player["player_experience"]) # Player Experience Points
                self.writeVInt(3) # Stats Index

                self.writeVInt(player["trophies"]) # Player Trophies
                self.writeVInt(4) # Stats Index
                self.writeVInt(player["highest_trophies"]) # Highest Trophies
                self.writeVInt(5) # Stats Index
                self.writeVInt(len(player["unlocked_brawlers"])) # Unlocked Brawlers
                self.writeVInt(7) # Stats Index
                self.writeVInt(28000000 + player["profile_icon"]) # Player Profile Icon
                self.writeVInt(8) # Stats Index
                self.writeVInt(player["solo_wins"]) # Showdown Victories


                # Stats Entry Array End
                # Player Profile End
                

                # Alliance Header Entry Array
                
                self.writeBoolean(player["club_id"] != 0) # Joined in a Band
                if player["club_id"] != 0:
                    club = db.loadClub(player["club_id"])
                    self.writeLong(0, player["club_id"]) # Band ID
                    self.writeString(club["info"]["name"]) # Band Name
                    self.writeDataReference(8, club["info"]["clubBadge"]) # Band Badge
                    self.writeVInt(club["info"]["clubType"]) # Band Type
                    self.writeVInt(club["info"]["onlineMembers"]) # Band Members
                    self.writeVInt(len(club["info"]["memberCount"])) # players count
                    trophies = 0
                    for token in club["info"]["memberCount"]:
                        memberData = db.getMemberData(token)
                        trophies += memberData["trophies"]
                    self.writeVInt(trophies) # club trophies
                    self.writeVInt(club["info"]["requiredTrophies"]) # Band Required Trophies
                    self.writeDataReference(0, 1) # Unknown Data Reference
                    self.writeVInt(1)
                    self.writeDataReference(25, player["club_role"]) # player club role