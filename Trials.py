'''
Created on 2016-09-30

@author: tsico
'''


import random
from psychopy import visual, core, event
from Cat_exp_function import countdown, write_instruction
from random import shuffle


def get_list_cat_trial(cat0, cat1, n_block, n_trials_by_block):
    trials = []
    while len(trials)<n_block*n_trials_by_block :
        stim_bank = []
        for stim in cat0 :
            stim_bank.append([stim, 0])
        for stim in cat1 :
            stim_bank.append([stim, 1])
        stim_bank.shuffle
        for stim in stim_bank :
            trials.append(stim)
            if len(trials) == n_block*n_trials_by_block :
                break
    return trials

class cat_trials(object):
    def __init__(self, primer = None, primer_time = None,pic_time = None,
                 maxanswer_time = None, folder_path = None, win=None):
        self.pic_time = pic_time
        self.primer_time = primer_time
        self.maxanswer_time = maxanswer_time
        self.win = win
        self.primer = visual.ImageStim(self.win, image=primer)
        self.mouse = event.Mouse(visible=False, newPos=None, win=None)
        self.folder_path = folder_path + "\\"

    def trial(self, stim_name, KorL, path):

        stim = visual.ImageStim(self.win, image=self.folder_path + stim_name)
        self.win.flip()
        core.wait(1)
        self.primer.draw()
        self.win.flip()
        core.wait(self.primer_time)
        stim.draw()
        self.win.flip()
        time_stim = core.getTime()
        
        thisResp=None
        while thisResp==None:
            allKeys=event.waitKeys(maxWait=float(self.pic_time),timeStamped=True)
            if allKeys == None :
                instruction = visual.TextStim(self.win, text=u"K or L", pos=(0.0, 0.0), color = "Black")
                instruction.draw()
                self.win.flip()
                allKeys=event.waitKeys(maxWait=float(self.maxanswer_time - self.pic_time),timeStamped=True)
                
            if allKeys == None :
                thisResp = "Nothing"
            else :
                #A changer
                for thisTuple in allKeys:
                    thisResp = [thisTuple[0], thisTuple[1]]
            
        if thisResp[0] == "k" :
            thisResp[0] = 0
        elif thisResp[0] == "l" :
            thisResp[0] = 1
        elif thisResp[0] == "q" :
            core.quit() 
            event.clearEvents()
        elif thisResp == "Nothing":
            thisResp = [0,0]
        else :
            thisResp = [0,0]
        
            
        if thisResp[0] == 0 or thisResp[0] == 1 :
            thisResp[1] = thisResp[1] - time_stim
            

        if thisResp[0] == KorL :
            thisResp[0] = 1
            instruction = visual.TextStim(self.win, text=u"Correct", pos=(0.0, 0.2), color = "green")
            instruction.draw()
        else :
            thisResp[0] = 0
            instruction = visual.TextStim(self.win, text=u"Incorrect", pos=(0.0, 0.2), color = "Red")
            instruction.draw()
        
        self.win.flip()
        core.wait(1) 
            
        return thisResp #Dictionnaire [0 ou 1(bon), TR]
    


        

        
        
        
        
        
        