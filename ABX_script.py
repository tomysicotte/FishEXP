'''
Created on 2016-09-30

@author: tsico
'''


from psychopy import data, gui, visual
from Trials import CAT_trials, write_instruction, decompte
import json
import os
import random


script_folder_path = "C:\Users\\tsico\\git\\TEST_ABX\\"
texture_folder_location = "C:\\Exp\\Textures3inv\\"

param_name = "parametres.json"


with open(script_folder_path + param_name, "r") as params_file :
    params = json.load(params_file)


expInfo = {'participant':'', 'Invariant':'ABCDEF', "Version" : "1"}
gui.DlgFromDict(dictionary=expInfo, title="CAT")
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = "CAT"

path = texture_folder_location+expInfo['Invariant']+"3-GOODSIZE\\"

All_stim = os.listdir(path)
k = []
l = []
for stim in All_stim :
    if stim[0] == u'k' :
        k.append(stim)
    else :
        l.append(stim)
        
print k  
random.shuffle(k)
random.shuffle(l)    
stim = [k,l]



file_name = expInfo["participant"]

win = visual.Window(fullscr = True, color="white")
Result_data = data.ExperimentHandler(name='CAT', version='1', extraInfo=expInfo, 
                                     runtimeInfo=None, originPath=params["Data_folder"], savePickle=False, 
                                     saveWideText=True, dataFileName=file_name, 
                                     autoLog=True)


CAT_trials = CAT_trials(primer = texture_folder_location + str(params[u"Primer"]), 
                        primer_time = float(params[u"Primer_time"]),
                        pic_time = float(params[u"Pic_time"]), 
                        white_time = float(params[u"White_time"]),
                        maxanswer_time = float(params[u"Maxanswer_time"]), 
                        folder_path = texture_folder_location + str(params[u"PRATIQUE_folder"]),
                        win = win)


write_instruction(u"Bonjour! Dans la t\xe2che qui suit, des s\xe9quences de trois images seront pr\xe9sent\xe9es. \xc0 la fin de chaque s\xe9quence, vous devrez indiquer laquelle des deux premi\xe8res images \xe9tait identique \xe0 la troisi\xe8me. ", win, "Black")



decompte(u"La pratique commmence dans :", 5, win, "Black")




CAT_trials.folder_path = texture_folder_location + str(params[u"Texture_folder"])+ "\\"

write_instruction(u"La pratique est termin\xe9e ", win, "Black")
write_instruction(u"\xcates-vous pr\xeat \xe0 commencer la t\xe2che principale? ", win, "Black")
decompte(u"L'exp\xe9rimentation commmence dans :", 5, win, "Black")





for n in range(100):
    
    x = random.randint(0,1)
    
    trial = CAT_trials.trial(stim[x][n], x, path)
    
    if str(trial[0]).isdigit() :
        trial_res_info = {}
        trial_res_info["Resultat"] = trial[0]
        trial_res_info["TR"] = trial[1]

        for item in trial_res_info :
            Result_data.addData(item, trial_res_info[item])
        Result_data.nextEntry()


    
    

write_instruction(u"Vous avez termin\xe9! ", win, "Black")
write_instruction(u"Merci pour votre participation! ", win, "Black")



