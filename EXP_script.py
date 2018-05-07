'''
Created on 2016-09-30

@author: tsico
'''


from psychopy import data, gui, visual
from Trials import cat_trials, get_list_cat_trial
from Cat_exp_function import get_info_from_dlg, write_instruction, countdown
import json
import os
import random



# Crée expInfo et demande les informations pertinentes
exp_info = get_info_from_dlg({"Name":None, "Exp" : ["Fish", "Textures"], "Version" : ["1", "2"]})


param_name = "parametres"+ exp_info['Exp']+exp_info['Version']+".json"
with open(param_name, "r") as params_file :
    params = json.load(params_file)


kalamites = os.listdir(params['Path_texture']+"K\\")
lakamites = os.listdir(params['Path_texture']+"L\\")

if params["JS_trial"] > 0 :
    js_stim = []
cat_trials_list = get_list_cat_trial(kalamites,lakamites,params["Block"], params["Trial_per_block"])

file_name = exp_info['Exp'] + "_" + exp_info['Version'] + "_" + exp_info["participant"]

win = visual.Window(fullscr = True, color="white")
result_data = data.ExperimentHandler(name='Cat', version=exp_info['Version'], extraInfo=exp_info,
                                     runtimeInfo=None, originPath=params['Path_texture'], savePickle=False,
                                     saveWideText=True, dataFileName=file_name,
                                     autoLog=True)


cat_trials = cat_trials(primer =params[u"Primer"],
                        primer_time = float(params[u"Primer_time"]),
                        pic_time = float(params[u"Pic_time"]),
                        maxanswer_time = float(params[u"Maxanswer_time"]),
                        folder_path = params['Path_texture'],
                        win = win)


write_instruction(u"Bonjour! Dans la t\xe2che qui suit, des s\xe9quences de trois images seront pr\xe9sent\xe9es. "
                  u"\xc0 la fin de chaque s\xe9quence, vous devrez indiquer laquelle des deux premi\xe8res images "
                  u"\xe9tait identique \xe0 la troisi\xe8me. ", win, "Black")


countdown(u"La pratique commmence dans :", 5, win, "Black")

cat_trials.folder_path = texture_folder_location + str(params[u"Texture_folder"]) + "\\"

write_instruction(u"La pratique est termin\xe9e ", win, "Black")
write_instruction(u"\xcates-vous pr\xeat \xe0 commencer la t\xe2che principale? ", win, "Black")
countdown(u"L'exp\xe9rimentation commmence dans :", 5, win, "Black")

for n in range(100):
    
    x = random.randint(0,1)
    
    trial = cat_trials.trial(stim[x][n], x, path)
    
    if str(trial[0]).isdigit() :
        trial_res_info = {}
        trial_res_info["Resultat"] = trial[0]
        trial_res_info["TR"] = trial[1]

        for item in trial_res_info :
            result_data.addData(item, trial_res_info[item])
        result_data.nextEntry()


    
    

write_instruction(u"Vous avez termin\xe9! ", win, "Black")
write_instruction(u"Merci pour votre participation! ", win, "Black")

