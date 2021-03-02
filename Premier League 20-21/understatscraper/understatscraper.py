import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

class understatscraper :
    def __init__(self , id) :
        self.id = id
        self.base_url = 'https://understat.com/match/'
        self.url = self.base_url+self.id
        
        
    def scrape(self) :
        res = requests.get(self.url)
        soup = BeautifulSoup(res.content, 'lxml')
        scripts = soup.find_all('script')
        strings = scripts[1].string
        # strip unnecessary symbols and get only JSON data 
        ind_start = strings.index("('")+2 
        ind_end = strings.index("')") 
        json_data = strings[ind_start:ind_end] 
        json_data = json_data.encode('utf8').decode('unicode_escape')

        #convert string to json format
        data = json.loads(json_data)
        
        x = []
        y = []
        xG = []
        result = []
        team = []
        minute = []
        data_away = data['a']
        data_home = data['h']

        for index in range(len(data_home)):
            for key in data_home[index]:
                if key == 'X':
                    x.append(data_home[index][key])
                if key == 'Y':
                    y.append(data_home[index][key])
                if key == 'h_team':
                    team.append(data_home[index][key])
                if key == 'xG':
                    xG.append(data_home[index][key])
                if key == 'result':
                    result.append(data_home[index][key])
                if key == 'minute':
                    minute.append(data_home[index][key])
                    

        for index in range(len(data_away)):
            for key in data_away[index]:
                if key == 'X':
                    x.append(data_away[index][key])
                if key == 'Y':
                    y.append(data_away[index][key])
                if key == 'a_team':
                    team.append(data_away[index][key])
                if key == 'xG':
                    xG.append(data_away[index][key])
                if key == 'result':
                    result.append(data_away[index][key])
                if key == 'minute':
                    minute.append(data_away[index][key])
                    
                    
        col_names = ['x','y','xG','result' ,  'team', 'minute']
        df = pd.DataFrame([x,y,xG,result,team,minute],index=col_names)
        df = df.T
        
        return df

                    