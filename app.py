import requests
import config
import json
from time import sleep
import numpy as np
from Grapher import ScrollableWindow 
from DashboardContants import DashBoard


DataSetSize = 8

class BallChaser:
    BASE_URL = "https://ballchasing.com/api" #the the root url to BallChase API
    IndexOfCurrentPlayer = 0 #stores the index of which PlayerId we are dealing with atm
    CurrentPlayerName = None #stores the current player name we are dealing with atm
    def __init__(self, tokens, NumOfMaxTopScores):
        self.Tokens = tokens #stores the players ids
        self.NumOfMaxTopScores = NumOfMaxTopScores #max number of replays that gonna be taking which at the same time sets the max number of scores
        self.header = {'Authorization': config.TOKEN} #setting up the header with the token (this token is taken from another file just for security purposes)
        self.params = None
        self.Replays = None #stores the whole Json Replays's response of some player
        self.ReplaysLinks = [] #stores the Replay links (API links not normal ones)
        self.BestScores = [] #stores best scores of player, higher score means better performance 
        self.PureData = [] #stores player's cam settings data
        self._state()

       # self.ReplaysTok = [] 
    
    def _state(self): #making sure that the API is up
        state = requests.get(self.BASE_URL, headers= self.header).status_code #basic test on the api and getting the status code which teels if it worked or not
        if state == 200:
            print("Working")
        elif state == 401:
            print("Invalid Tokens / Tokens Requried")
            exit(-1)
        else:
            print("Something is wrong")
            exit(-1)

    
    def GetCamSettingsInfo(self):
        for i in self.Tokens:
           self.GetCamSettingsInfoProcess()

    def GetCamSettingsInfoProcess(self): 
        self.MakeParams()
        self.FindReplays()
        self.EliminateUnvalidReplays()
        self.FindBestPlayerPerformances()
        self.PureDataExtractor()
        self.CleanUp()
        self.IndexOfCurrentPlayer += 1
        print(self.PureData)

    def CleanUp(self): #cleans the lists so we don't use the previous player data
        self.params = None
        self.Replays = None
        self.ReplaysLinks.clear()
        self.BestScores.clear()
        self.CurrentPlayerName = ""


    def MakeParams(self): #the filters you wanna apply for search (not finished working on it yet)
        self.params = {"player-id": f'Steam:{self.Tokens[self.IndexOfCurrentPlayer]}', "count": 10}


    def FindReplays(self, params = None): #finds all replays of a player
        url = f"{self.BASE_URL}/replays"
        self.Replays = requests.get(url, headers=self.header, params=self.params).json() #doin the request and parsing the respone as Json
        #VVVVVVVVV in this part im just writing that file to a text file so i can see everything more clearly 
        temp = json.dumps(self.Replays, indent=4)
        with open("Data.json",'w',encoding = 'utf-8') as f:
                f.write(temp)

    def EliminateUnvalidReplays(self): #Removes useless replies where the game duration is smaller than 1.5 minutes
        temp = self.Replays["list"].copy() #copies it so i can remove the elements from the original list , if i apply this on roiginal list it might cause problems
        for replay in temp:
            if replay["duration"]/60 < 1.5:
                self.Replays["list"].remove(replay)
    
    def FindPlayerScores(self): #finding scores of the player so then i can loop again on the Json data and get the api replays links that connected with this score
        for replay in self.Replays["list"]: 
            flag = False #saves more time so when i find the right player i dont have to check others and if i found it in one team
                         #i dont have to check the other team because obviously you can't be in both teams
            for player in replay["blue"]["players"]:
                if player["id"]["id"] == self.Tokens[self.IndexOfCurrentPlayer]:
                        self.BestScores.append(player["score"])
                        self.CurrentPlayerName = player["name"]
                        flag = True
                        break
                if flag == True:
                    break
            for player in replay["orange"]["players"]:
                if player["id"]["id"] == self.Tokens[self.IndexOfCurrentPlayer]:
                        self.BestScores.append(player["score"])
                        self.CurrentPlayerName = player["name"]
                        flag = True

    def FindBestPlayerPerformances(self):
        self.FindPlayerScores()
        self.BestScores.sort(reverse=True) #sorts the scores from the biggest to the lowwest
        Temparr = [] #i copy the biggest N scores to this list so then i can clear BestScores and keep these numbers that i gonna use
        limit = 0
        #making sure that the requried number of scores isn't bigger than the number of replies lets say the user wanted 10 scores but there was 3 which would cause an error
        if self.NumOfMaxTopScores > len(self.BestScores): self.NumOfMaxTopScores = len(self.BestScores) 
        while(limit < self.NumOfMaxTopScores):
            Temparr.append(self.BestScores[limit])
            limit += 1
        self.BestScores.clear()
        self.BestScores.extend(Temparr)
        # print(self.BestScores) #temp test
        self.FindReplayTokens()
        
    
    def FindReplayTokens(self): #getting the replay tokens so i can get the data from it
        #CopyReplays = self.Replays["list"].copy()
        for score in self.BestScores:
            for replay in  self.Replays["list"]: 
                flag = False               
                for player in replay["blue"]["players"]: #blue team search part
                    if player["score"] ==  score:
                        if replay["link"] in self.ReplaysLinks: #making sure that we won't take the same link if a it happened and we got same scores for different replays
                            break
                        self.ReplaysLinks.append(replay["link"])
                        flag = True
                        break
                if flag: break
                for player in replay["orange"]["players"]: #orange team search part
                    if player["score"] ==  score:
                        if  replay["link"] in self.ReplaysLinks:
                            break
                        self.ReplaysLinks.append(replay["link"])
                        break
        # print(self.ReplaysLinks) #temp test

    
    def PureDataExtractor(self): #extracts camera settings of the player
        temp = []
        for link in self.ReplaysLinks:
            sleep(0.125) #stops executing for the specefied amount of time because there is a limit fot requests that you can do per second
            flag = False
            ReplayData = requests.get(link, headers=self.header).json() #makes request for the replay itself
            for player in ReplayData["blue"]["players"]:
                if player["id"]["id"] == self.Tokens[self.IndexOfCurrentPlayer]:
                    self.PureDataAppender(player, temp)
                    flag = True
                    break
            if flag: continue
            for player in ReplayData["orange"]["players"]:
                if player["id"]["id"] == self.Tokens[self.IndexOfCurrentPlayer]:
                    self.PureDataAppender(player, temp)
        self.PureData.append(temp)
        self.PlayerDataAVG()
        self.PureData[self.IndexOfCurrentPlayer].insert(0, self.CurrentPlayerName)
        self.PureData[self.IndexOfCurrentPlayer].insert(0, self.Tokens[self.IndexOfCurrentPlayer])

        # temp = json.dumps(temp.json(), indent=4)
        # with open("datalink.json","w+" , encoding = 'utf-8') as f:
        #     f.write(temp)

    def PureDataAppender(self, player, temp):
        data = [player["camera"][key] for key in player["camera"].keys()]
        data.append(player["steering_sensitivity"])
        temp.append(data) #takes camera settings
        #temp.append([player["camera"][key] for key in player["camera"]])

    def PlayerDataAVG(self):
        result = []
        DataContainer = [] #sorts each kind if data in one list for example stiffness data gonna be in one list
        for i in range(DataSetSize):
            temp = []
            for DataList in self.PureData[self.IndexOfCurrentPlayer]:
                temp.append(DataList[i])
            DataContainer.append(temp)   
        for DataList in DataContainer:
            result.append(float("{:.2f}".format(np.average(DataList)))) #taking 2 digits after the decimal point
        self.PureData[self.IndexOfCurrentPlayer] = result

    def GetDashBoard(self):
        ScrollableWindow(DashBoard(self.PureData).GetMainFigure())
