'''
Created on 2016-09-30

@author: tsico
'''

from psychopy import visual, core
from Categorization import CatTrials
from Exp_general_function import get_info_from_dlg, write_instruction
from Similarity_judgment import sj_trials
from Oddball import OddballTrials
from random import randint
import json
import os

"""
Principal script for categorization experience with an EEG option

For this script to work, you need a parameter's file and an instruction's file in .json
See ParametersModel.py and InstructionsModel.py for instruction

EEG trigger identification :
    No trigger are sent during practice trials

    Categorization
        New Block
            11 Block 1
            12 Block 2
            13 Block 3
            14 Block 4
        Stimulus appearance
            20 Stimulus Category 1
            21 Stimulus Category 2
        Answer
            40 Stimulus Category 1 and bad
            41 Stimulus Category 1 and good
            50 Stimulus Category 2 and bad
            51 Stimulus Category 2 and good
    
    Similarity judgement
        Stimulus appearance
            101 Stimulus 1 Category 1 and same  1st JS
            111 Stimulus 1 Category 1 and diff  1st JS
            201 Stimulus 1 Category 2 and same  1st JS
            211 Stimulus 1 Category 2 and diff  1st JS
            102 Stimulus 2 Category 1 and same  1st JS
            112 Stimulus 2 Category 1 and diff  1st JS
            202 Stimulus 2 Category 2 and same  1st JS
            212 Stimulus 2 Category 2 and diff  1st JS
            103 Stimulus 1 Category 1 and same  2nd JS
            113 Stimulus 1 Category 1 and diff  2nd JS
            203 Stimulus 1 Category 2 and same  2nd JS
            213 Stimulus 1 Category 2 and diff  2nd JS
            104 Stimulus 2 Category 1 and same  2nd JS
            114 Stimulus 2 Category 1 and diff  2nd JS
            204 Stimulus 2 Category 2 and same  2nd JS
            214 Stimulus 2 Category 2 and diff  2nd JS
            
            
            
            
    Oddball
        Stimulus appearance
            Oddball #1
                80 Type Same and main
                81 Type Same and distractor
                82 Type Same and target
                90 Type Different and main
                91 Type Different and distractor
                92 Type Different and target
            Oddball #2
                180 Type Same and main
                181 Type Same and distractor
                182 Type Same and target
                190 Type Different and main
                191 Type Different and distractor
                192 Type Different and target
"""

if __name__ == '__main__':
    # Get information about the study you want to do
    exp_info = get_info_from_dlg({"Exp": ["Fish", "Textures"],"Langage": ["Francais", "English"], 'EEG': ['Yes', 'No']})

    # Load parameters as params(dict) for this study
    param_name = "parametres" + exp_info['Exp'] + ".json"
    with open(param_name, "r") as params_file:
        params = json.load(params_file)
    if exp_info['EEG'] == 'Yes':
        params['EEG'] = True
    else:
        params['EEG'] = False

    # Determine the wanted version
    version = get_info_from_dlg({"Version": params["Path_texture"]+["Random"]})
    if version["Version"] == "Random" :
        version["Version"] = params["Path_texture"][randint(0,len(params["Path_texture"])-1)]
    exp_info["Version"] = str(params["Path_texture"].index(version["Version"])+1)
    params["Stim_list_folder"] = params["Stim_list_folder"][int(exp_info["Version"]) - 1]
    params["Path_texture"] = params["Path_texture"][int(exp_info["Version"]) - 1]

    # Get information about participant and add it to exp_info
    participant_info = get_info_from_dlg({"ID number": None, "Age": None,
                                          "Gender": ["Woman", "Man", "Other", "Prefer not to say"],
                                          "Main hand": ["Right", "Left", "Ambidextrous"]})
    for key in participant_info:
        if key == "ID number":
            exp_info["Name"] = participant_info[key]
        else:
            exp_info[key] = participant_info[key]

    # Load instruction (Instruction should be adapted to the type of task you have, see model)
    with open(params[exp_info["Langage"] + "_ins"], "r") as ins_file:
        txt_ins = json.load(ins_file)

    # Create window for exp
    win = visual.Window(fullscr=True, color="white")

    # all_names become a list of list for each category if each category as his own folder
    # all_names become a list of all stimuli if they are all in the same folder
    all_names = []
    if len(params["Cat_folder"]) > 1 :
        for cat_folder in params["Cat_folder"] :
            all_names.append(os.listdir(params["Stim_list_folder"] + cat_folder))
    else :
        all_names = os.listdir(params["Stim_list_folder"])

    if "SJ_trial" in params :
        sj_trials = sj_trials(params=params, win=win, exp_info=exp_info, txt_ins=txt_ins,
                              stimulus_list= all_names)
    cat_trials = CatTrials(win=win, params=params, txt_ins=txt_ins, exp_info=exp_info,
                           stimulus_list= all_names)
    if "N_deviant" in params :
        oddball_trials = OddballTrials(params=params, win=win, exp_info=exp_info, txt_ins=txt_ins,
                                       stimulus_list=all_names)

    write_instruction(txt_ins["Intro"], txt_ins["Key_to_continue"], win, "Black")
    if "SJ_trial" in params:
        sj_trials.sj_routine(1)
    if "N_deviant" in params:
        oddball_trials.oddball_routine(1)
    cat_trials.categorization_routine()
    if "SJ_trial" in params:
        sj_trials.sj_routine(2)
    if "N_deviant" in params:
        oddball_trials.oddball_routine(2)
    write_instruction(txt_ins["Exp_end"], txt_ins["Key_to_continue"], win, "Black")

    win.close()
    if params["Trial_per_block"] > 0 :
        if exp_info["Exp"] == "Fish" :
            p_info = get_info_from_dlg({txt_ins["Q1"]: txt_ins["A1"],
                                        txt_ins["Q2"]: txt_ins["A2"],
                                        txt_ins["Q3"]: txt_ins["A3"],
                                        txt_ins["Q4"]: txt_ins["A4"],
                                        txt_ins["Q5"]: txt_ins["A5"],
                                        txt_ins["Q6"]: txt_ins["A6"],
                                        txt_ins["Q7"]: txt_ins["A7"]})
            cat_trials.add_answers_info(p_info)


    core.quit()