# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 08:27:19 2021

@author: jamie
"""

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import base64
from bs4 import BeautifulSoup
import pandas

# If modifying these scopes, delete the file token.json.



def connectToGoogle(folder=''):
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    
    token_path = folder + 'token.json'
    creds_path = folder + 'credentials.json'
    
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    
    return service   

def getEmails(service, search_string):
    #TODO paginate request
    
    next_page = True
    ids = []
    query  = service.users().messages().list(userId='me',maxResults=500, q=search_string).execute()
    
    while True:
    
        ids += [i['id'] for i in query['messages']]    
        if 'nextPageToken' in query.keys():
            next_page = query['nextPageToken']

            query  = service.users().messages().list(userId='me',
                                                     maxResults=500,
                                                     q=search_string, 
                                                     pageToken=next_page).execute()
           
        else:
            break
              
    results = []
    
    for i in ids:
         m = service.users().messages().get(userId='me', id =  i,format='raw').execute()
         text = parseEmail(m)
         if text != None:
             results.append(text)
    return results
    
def parseEmail(email):
    
    #rejects non ending or cycle emails#
    
    valid = ["Galactic Cycle Complete! You have received new funds to spend upgrading your empire",
             "Login now and congratulate the winners!"]
    
    snip = email['snippet']
    
    search = [snip.find(i) >= 0 for i in valid]
    if any(search):
        text =  str(base64.b64decode(email['raw'],"-_"))
        text = text.replace('\\n','')
        text = text.replace('\\r','')
        return text
    else:
        return None

#TODO convert all to integers
def extractTable(email):
    soup = BeautifulSoup(email, 'html.parser')
    table = soup.find_all('table')[1]
    rows = table.find_all('tr')
    
    gameDetails = getGameDetails(email)
    
    
    results = []
    
    for i in range(len(rows)):
        rank = i + 1
        
        data = rows[i].find_all('td')
        
        player = data[0].text.strip()
        
        #turns stars to just a number
        stars = data[1].text.strip()
        index = stars.find('Stars')-1
        stars = stars[:index]
        
        #splits fleet data to ships and carriers
        fleet = data[2].text.strip()
        
        ship_index = fleet.find('Ships')-1
        ships = fleet[:ship_index]
        
        in_index = fleet.find('in')+3
        car_index = fleet.find('Carriers')-1
        carriers = fleet[in_index : car_index]
        
        entry = {"Id"        : gameDetails['Id'],
                 "Name"      : gameDetails['Name'],
                 "Cycle"     : gameDetails['Cycle'],
                 "Player"    : player,
                 "Rank"      : rank,
                 "Stars"     : stars,
                 "Ships"     : ships,
                 "Carriers"  : carriers}
        results.append(entry)
    
    players = len(results)
    for i in results:
        i['GameSize'] = players
    
    return results
    
def getGameDetails(email):
    
    game_stem = "http://np.ironhelmet.com/game/"
    
    soup = BeautifulSoup(email, 'html.parser')
    links = soup.find_all('a')
    
    #Strips the gameId from the link
    gameid = False
    for l in links:
        text = l.text.strip()
        if text.find(game_stem) == 0:
           gameid =  text[len(game_stem) : ]
    

    #TODO functionise the name stripper    
    #Checks if this is an end of game email
    gameEnd = email.find('has ended!') >= 0
    
    if gameEnd:
        start = email.find("Subject: NP2: Game")
        end = email.find('has ended!')
        name = email[start+18:end].strip() 
        cycle = "End"
    else:
        start = email.find("Subject: NP2:")
        end = email.find("From: Iron Helmet Games")
        title = email[start:end] 
        cycle_index = title.find("Cycle")
        
        cycle = title[cycle_index + 5 :].strip()
        name = title[13:cycle_index].strip()
        name = name[:-1]
        
    #Returns game details as a dict
    results = {'Id'     : gameid,
               'Name'   : name,
               'Cycle'  : cycle}
    
    return results
    

        
    
        


if __name__ == '__main__':


    queries = ['np2 "Galactic Cycle Complete"',
               'NP2 "has ended"']    
    
    service = connectToGoogle('./inputs/')
    
    tables = []
    
    for i in queries:       
        emails = getEmails(service, i)
        result = []
        for i in emails:
            result += extractTable(i)
        tables = tables + result

    





    


    
