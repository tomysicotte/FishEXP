'''
Created on 2016-09-30
@author: Tomy Sicotte
'''
import random
from psychopy import visual, core, event, data
from Exp_general_function import write_instruction, countdown, get_practice_stim
from psychopy.constants import *
from SendSignal import PortParallel


def get_list_cat_trial_fish_with_orientation(cat_list, win, params):
    """
    :param cat_list: Name of all stim in a list
    :param win: Exp window
    :param params: Exp parameters (N_block = number of block, Trial_per_block = number of trials in a block,
                                    Path_texture = Path to the texture without orientation
                                    This folder should contain a folder for orientation from 5 to 355 for every 15 degree
                                    difference, Cat_folder = Name of the folder for each of the 2 categories)
    :return: A shuffled list that contain a list for each trial
            Index 0 : stim.image.window
            Index 1 : Category either 0 or 1
            Index 2 : Name of the stimulus
            Index 3 : Orientation
    """
    trials = []
    n_block = params["N_block"]
    n_trials_by_block = params["Trial_per_block"]
    while len(trials) < n_block * n_trials_by_block:
        stimulus_bank = []
        for k, cat in enumerate(cat_list):
            cat_bank = []
            for stimulus_name in cat:
                ori = random.randint(1, 24) * 15 - 10
                im_stim = visual.ImageStim(win, image=params["Path_texture"] + str(ori) + "\\"
                                                      + params["Cat_folder"][k] + stimulus_name)
                cat_bank.append([im_stim, k, stimulus_name, ori])
            random.shuffle(cat_bank)
            stimulus_bank.append(cat_bank)
        for i in range(min([len(cat_list[0]), len(cat_list[1])])):
            trials.append(stimulus_bank[0][i])
            if len(trials) == n_block * n_trials_by_block:
                break
            trials.append(stimulus_bank[1][i])
            if len(trials) == n_block * n_trials_by_block:
                break
    random.shuffle(trials)
    return trials


def get_list_cat_trial_texture(cat_list, win, params):
    """
        :param cat_list: Name of all stim in a list
        :param win: Exp window
        :param params: Exp parameters (N_block = number of block, Trial_per_block = number of trials in a block,
                                        Path_texture = Path to the texture
        :return: A shuffled list that contain a list for each trial
                Index 0 : stim.image.window
                Index 1 : Category either 0 or 1
                Index 2 : Name of the stimulus
        """
    trials = []
    n_block = params["N_block"]
    n_trials_by_block = params["Trial_per_block"]
    while len(trials) < n_block * n_trials_by_block:
        random.shuffle(cat_list)
        k_bank = []
        l_bank = []
        for stimulus_name in cat_list:
            if stimulus_name[0] == "k":
                image_stimulus = visual.ImageStim(win, image=params["Path_texture"] + stimulus_name)
                k_bank.append([image_stimulus, 0, stimulus_name])
            else:
                image_stimulus = visual.ImageStim(win, image=params["Path_texture"] + stimulus_name)
                l_bank.append([image_stimulus, 1, stimulus_name])
        for i in range(min([len(k_bank), len(l_bank)])):
            trials.append(k_bank[i])
            if len(trials) == n_block * n_trials_by_block:
                break
            trials.append(l_bank[i])
            if len(trials) == n_block * n_trials_by_block:
                break
    random.shuffle(trials)
    return trials


class CatTrials(object):
    def __init__(self, win=None, params=None, exp_info=None, txt_ins=None, stimulus_list=None):
        self.win = win
        self.params = params
        self.exp_info = exp_info
        self.txt_ins = txt_ins
        self.stimulus_list = stimulus_list

        if self.params["EEG"] :
            self.pport = PortParallel()
        else :
            self.pport = False

        # Get a list of stimuli for the practice trial
        # The list contain all the stimuli in the practice folder as win.image
        self.practice_stim_list = get_practice_stim(params["Practice_path"], self.win)

        self.pic_time = float(params[u"Cat_stim_time"])
        self.primer_time = float(params[u"Primer_time"])
        self.maxanswer_time = float(params[u"Maxanswer_time"])
        self.feedback_time = float(params["Feedback_time"])
        self.stim_end = self.primer_time + self.pic_time
        self.trial_end = self.primer_time + self.maxanswer_time

        # Create the mouse, primer and categorisation choices txt
        self.mouse = event.Mouse(visible=False, newPos=None, win=None)
        self.primer = visual.Circle(win=win, radius=45, units="pix", fillColor=[-1, -1, -1], lineColor=[-1, -1, -1])
        self.horizontal_line = visual.Line(win=win, units="pix", lineColor=[+1, +1, +1],
                                           lineWidth=10, start=(-50, 0), end=(+50, 0))
        self.vertical_line = visual.Line(win=win, units="pix", lineColor=[+1, +1, +1],
                                         lineWidth=10, start=(0, -50), end=(0, +50))
        self.center = visual.Circle(win=win, radius=5, units="pix", fillColor=[-1, -1, -1], lineColor=[-1, -1, -1])
        self.txt_categorisation_choices = visual.TextStim(win=win, text=self.txt_ins["Cat_answer_option"],
                                                          pos=(0.0, 0.0), color="Black")

        # Create a trial_list
        # Method must be adapted to the way stimuli are stored in the computer and rules wanted
        if exp_info["Exp"] == "Fish":
            if self.params["Orientation"] == "True":
                self.cat_trials_list = get_list_cat_trial_fish_with_orientation(stimulus_list, self.win, params)
        elif exp_info["Exp"] == "Textures":
            self.cat_trials_list = get_list_cat_trial_texture(stimulus_list, self.win, params)

        # Create data handler
        file_name = exp_info['Exp'] + "_Version" + exp_info['Version'] + "_" + exp_info["Name"] + "_Cat"
        self.cat_data = data.ExperimentHandler(name='Cat',
                                               version=exp_info['Version'],
                                               extraInfo=exp_info,
                                               runtimeInfo=None,
                                               savePickle=False,
                                               saveWideText=True,
                                               dataFileName=params["Cat_saving_path"]+file_name,
                                               autoLog=True)

    def primer_activation(self, on):
        if on :
            self.primer.setAutoDraw(True)
            self.horizontal_line.setAutoDraw(True)
            self.vertical_line.setAutoDraw(True)
            self.center.setAutoDraw(True)
        else :
            self.primer.setAutoDraw(False)
            self.horizontal_line.setAutoDraw(False)
            self.vertical_line.setAutoDraw(False)
            self.center.setAutoDraw(False)

    def practice_routine(self):
        self.params["EEG"] = False
        for i in range(self.params["N_Cat_Practice"]) :
            x = self.trial(self.practice_stim_list[random.randint(0,len(self.practice_stim_list)-1)], random.randint(0,1))
        if self.pport :
            self.params["EEG"] = True

    def categorization_routine(self):
        # Write instruction and practice if it's block 1
        write_instruction(self.txt_ins["Cat_ins1"], self.txt_ins["Key_to_continue"],self.win, "Black")
        write_instruction(self.txt_ins["Cat_ins2"], self.txt_ins["Key_to_continue"],self.win, "Black")
        write_instruction(self.txt_ins["Cat_ins3"], self.txt_ins["Key_to_continue"],self.win, "Black")
        write_instruction(self.txt_ins["Cat_ins4"], self.txt_ins["Key_to_continue"], self.win, "Black")
        countdown(self.txt_ins["Practice_countdown"], 5, self.win, "Black")
        self.practice_routine()
        write_instruction(self.txt_ins["VF_rdy"], self.txt_ins["Key_to_continue"],self.win, "Black")

        # Start the trials
        countdown(self.txt_ins["Cat_countdown"], 5, self.win, "Black")
        for n in range(self.params["N_block"]):
            if self.params["EEG"]:
                self.pport.send_signal(10+n+1)
            # Iterate in blocks
            if n > 0:
                # Write instruction between blocks
                write_instruction(self.txt_ins["Cat_between_bloc"], self.txt_ins["Key_to_continue"],self.win, "Black")
                write_instruction(self.txt_ins["VF_rdy"], self.txt_ins["Key_to_continue"],self.win, "Black")
                countdown(self.txt_ins["Cat_countdown"], 5, self.win, "Black")

            for i in range(self.params["Trial_per_block"]):
                # Iterate in trials
                stimulus_category = self.cat_trials_list[n * self.params["Trial_per_block"] + i][1]
                stimulus_name = self.cat_trials_list[n * self.params["Trial_per_block"] + i][2]
                stimulus = self.cat_trials_list[n * self.params["Trial_per_block"] + i][0]
                trial = self.trial(stimulus, stimulus_category)

                # Add data to this entry
                self.cat_data.addData("Block", n+1)
                self.cat_data.addData("Index", i+1)
                self.cat_data.addData("Resultat", trial[0])
                self.cat_data.addData("TR", trial[1])
                self.cat_data.addData("Stim", stimulus_name)
                self.cat_data.addData("Cat", stimulus_category)
                if self.params["Orientation"] == "True":
                    stim_orientation = self.cat_trials_list[n * self.params["Trial_per_block"] + i][3]
                    self.cat_data.addData("Orientation", stim_orientation)

                self.cat_data.nextEntry()

        write_instruction(self.txt_ins["Cat_end"], self.txt_ins["Key_to_continue"],self.win, "Black")

    def trial(self, stimulus, good_cat):
        """
        :param stimulus: stim.image
        :param good_cat: category of the stim (int)
        :return: A list
                Index 0 = 0 if bad answer, 1 if good answer
                Index 1 = Reaction time
        """

        t = 0

        # Create trial clock and event.Key
        key_resp = event.BuilderKeyResponse()
        trial_clock = core.Clock()

        # Add status to trial components
        trial_components = [stimulus, key_resp, self.primer]
        for thisComponent in trial_components:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        trial_clock.reset()
        continue_routine = True
        # Trial routine
        while continue_routine:
            # Using while method to adjust loop to screen frame rate for more precise EEG trigger
            t = trial_clock.getTime()
            if t < self.primer_time and self.primer.status == NOT_STARTED:  # Start trial
                if self.params["EEG"]:
                    self.pport.send_signal(1)
                self.primer_activation(True)
                self.primer.status = STARTED

            elif self.stim_end > t >= self.primer_time: #Stimulus period
                self.primer_activation(False)
                if stimulus.status == NOT_STARTED: # If stimulus just appeared
                    key_resp.tStart = t
                    key_resp.status = STARTED # Accept answer from now
                    key_resp.keys = []
                    key_resp.clock.reset()
                    event.clearEvents()
                    if self.params["EEG"] :
                        # Trigger identification
                        # 20 Category 1
                        # 21 Category 2
                        self.pport.send_signal(20 + int(good_cat))
                    stimulus.setAutoDraw(True)
                    stimulus.status = STARTED

            elif t >= self.stim_end and stimulus.status == STARTED: # End of stimulus period
                stimulus.setAutoDraw(False)
                stimulus.status = STOPPED
                if key_resp.status == STARTED and t <= self.trial_end: # If still no answer, show answer option
                    self.txt_categorisation_choices.setAutoDraw(True)

            elif stimulus.status == STOPPED and key_resp.status == STOPPED:
                # If stimulus is finished and answer, end routine
                self.txt_categorisation_choices.setAutoDraw(False)
                continue_routine = False

            elif t >= self.trial_end:
                # If no more time
                self.txt_categorisation_choices.setAutoDraw(False)
                key_resp.status = STOPPED
                continue_routine = False

            if key_resp.status == STARTED:  # If expecting a key press
                these_keys = event.getKeys()
                if len(these_keys) > 0:  # at least one key was pressed
                    if self.params["EEG"] :
                        self.pport.send_signal(30 + int(good_cat))
                    key_resp.keys = these_keys[-1]  # just the last key pressed
                    key_resp.rt = key_resp.clock.getTime()
                    key_resp.status = STOPPED
            self.win.flip() # Adjust loop to screen frame rate

        # VF answer, give feedback and send trigger according to category and accuracy
        # Trigger identification
        # 40 Category 1 and bad
        # 41 Category 1 and good
        # 50 Category 2 and bad
        # 51 Category 2 and good
        score = 0
        if key_resp.keys == self.params["Key_answer"][0]:
            if good_cat == 0:
                score = 1
                instruction = visual.TextStim(self.win, text=self.txt_ins["Feedback_good"], pos=(0.0, 0.0),
                                              color="green")
                instruction.draw()
            else:
                instruction = visual.TextStim(self.win, text=self.txt_ins["Feedback_bad"], pos=(0.0, 0.0),
                                              color="red")
                instruction.draw()
            if self.params["EEG"]:
                self.pport.send_signal(40 + int(score))
        elif key_resp.keys == self.params["Key_answer"][1]:
            if good_cat == 1:
                score = 1
                instruction = visual.TextStim(self.win, text=self.txt_ins["Feedback_good"], pos=(0.0, 0.0),
                                              color="green")
                instruction.draw()
            else:
                instruction = visual.TextStim(self.win, text=self.txt_ins["Feedback_bad"], pos=(0.0, 0.0),
                                              color="red")
                instruction.draw()
            if self.params["EEG"]:
                self.pport.send_signal(50 + int(score))
        elif key_resp.keys == "q" or key_resp.keys == "escape":
            core.quit()
        else:
            if key_resp.rt == 0:
                write_instruction(self.txt_ins["Wrong_key"], self.txt_ins["Key_to_continue"],self.win, "black")
            else:
                key_resp.rt = 0
                write_instruction(self.txt_ins["Too_long"], self.txt_ins["Key_to_continue"],self.win, "black")
        self.win.flip()
        core.wait(self.feedback_time)

        return [score, key_resp.rt]

    def add_answers_info(self, answers):
        for key in answers :
            self.cat_data.addData(key, answers[key])
        self.cat_data.nextEntry()
