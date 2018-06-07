import random
from psychopy import core, visual, event, data
from Exp_general_function import write_instruction, countdown
from random import randint
from SendSignal import PortParallel


def get_oddball_list(n_deviant) :
    """
    :param n_deviant: Determine the number of time the deviant stimulus will appear in a trial
    :return: Return a list of int containing n_deviant*10 values, 80% 0 main, 10% deviant, 10% target
    """
    n = n_deviant * 10
    beginning_trials = ['0'] * 5  # Each block starts with five standard trials
    trials = ['0'] * int(n-2*n_deviant-5) + ['1'] * n_deviant + ['2'] * n_deviant  # creates trial list
    while '11' in ''.join(trials):  # Makes sure that two deviants are not next to each other in the trial list
        random.shuffle(trials)
    trials = beginning_trials + trials
    for i in range(len(trials)):
        trials[i] = int(trials[i])
    return trials


def return_number(name):
    number = ""
    for letter in name :
        if letter.isdigit() :
            number += letter
    return number


def get_oddball_stim(all_stimulus, win, path):
    """
    :param all_stimulus: List of all stimulus
    :param win: exp window
    :param path: path to stimulus folder
    Note that pair of stimuli that can be matched together need to be identified in the name of the stimulus
    :return: A list that contain a list for each 4 trials (2 Between category, 2 within category)
            Index 0 : [target.image, target name]
            Index 1 : [deviant.image, deviant name]
    """
    kk = []
    lk = []
    kl = []
    ll = []
    random.shuffle(all_stimulus)
    for stimulus in all_stimulus:
        if stimulus[0] == "k" and stimulus[13] == "R" and len(kl)==0:
            my_img = visual.ImageStim(win, image=path+stimulus)
            kl.append([my_img, stimulus])
            for stimulus_2 in all_stimulus:
                if return_number(stimulus) == return_number(stimulus_2) and stimulus != stimulus_2 :
                    my_img2 = visual.ImageStim(win, image=path+stimulus_2)
                    kl.append([my_img2, stimulus_2])
        elif stimulus[0] == "l" and stimulus[13] == "R" and len(lk)==0 :
            my_img = visual.ImageStim(win, image=path + stimulus)
            lk.append([my_img, stimulus])
            for stimulus_2 in all_stimulus :
                if return_number(stimulus) == return_number(stimulus_2) and stimulus != stimulus_2 :
                    my_img2 = visual.ImageStim(win, image=path + stimulus_2)
                    lk.append([my_img2, stimulus_2])
        elif stimulus[0] == "l" and stimulus[13] == "A" and len(ll)==0 :
            my_img = visual.ImageStim(win, image=path + stimulus)
            ll.append([my_img, stimulus])
            for stimulus_2 in all_stimulus :
                if return_number(stimulus) == return_number(stimulus_2) and stimulus != stimulus_2 :
                    my_img2 = visual.ImageStim(win, image=path + stimulus_2)
                    ll.append([my_img2, stimulus_2])
        elif stimulus[0] == "k" and stimulus[13] == "A" and len(kk)==0 :
            my_img = visual.ImageStim(win, image=path + stimulus)
            kk.append([my_img, stimulus])
            for stimulus_2 in all_stimulus :
                if return_number(stimulus) == return_number(stimulus_2) and stimulus != stimulus_2 :
                    my_img2 = visual.ImageStim(win, image=path + stimulus_2)
                    kk.append([my_img2, stimulus_2])

    my_list = [kk,ll,lk,kl]
    random.shuffle(my_list)
    return my_list


class OddballTrials(object):
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

        self.oddball_trials_structure = []
        for i in range(4) :
            self.oddball_trials_structure.append(get_oddball_list(self.params["N_deviant"]))
        self.stim_trials_list = get_oddball_stim(self.stimulus_list, self.win, params["Stim_list_folder"])

        # Either create the target or load an image as the target
        if params[u"Oddball_target"] == "Cross" :
            self.target = visual.RadialStim(self.win, tex=None, color=(0, 0, 0), colorSpace='rgb255', pos=(0, 0),
                                       units='pix', size=(35, 35), mask=[0, 0, 0, 0, 0, 0, 1, 1], radialCycles=0,
                                       angularCycles=0, opacity=1, contrast=1.0, interpolate=False)
            self.fixation_cross_horizontal = visual.Line(win=self.win, units="pix", lineColor=[-1, -1, -1],
                                                                lineWidth=4, start=(-15, 0), end=(+15, 0))
            self.fixation_cross_vertical = visual.Line(win=self.win, units="pix", lineColor=[-1, -1, -1],
                                                                lineWidth=4, start=(0, -15), end=(0, +15))
        else :
            self.target = visual.ImageStim(self.win, image=params[u"Oddball_target"])

        #Create data handler
        file_name = exp_info['Exp'] + "_Version" + exp_info['Version'] + "_" + exp_info["Name"] + "_Oddball"
        self.oddball_data = data.ExperimentHandler(name='Oddball',
                                               version=exp_info['Version'],
                                               extraInfo=exp_info,
                                               runtimeInfo=None,
                                               savePickle=False,
                                               saveWideText=True,
                                               dataFileName=params["Oddball_saving_path"]+file_name,
                                               autoLog=True)

    def oddball_routine(self,block):
        # Activate saving on BIOSEMI (need to be added in BIOSEMI config)
        if self.params["EEG"]:
            self.pport.send_signal(254)
        for i,trial_structure in enumerate(self.oddball_trials_structure):
            # Write instruction according to trial number
            if i == 0 :
                if block == 1 :
                    write_instruction(self.txt_ins["Oddball_ins1"], self.txt_ins["Key_to_continue"],self.win, "Black")
                    write_instruction(self.txt_ins["Oddball_ins2"], self.txt_ins["Key_to_continue"],self.win, "Black")
                    write_instruction(self.txt_ins["Oddball_ins3"], self.txt_ins["Key_to_continue"], self.win, "Black")
                else :
                    write_instruction(self.txt_ins["Oddball_ins4"], self.txt_ins["Key_to_continue"], self.win, "Black")
                    write_instruction(self.txt_ins["Oddball_ins5"], self.txt_ins["Key_to_continue"], self.win, "Black")
            else :
                write_instruction(self.txt_ins["Oddball_pause1"], self.txt_ins["Key_to_continue"],self.win, "Black")
                write_instruction(self.txt_ins["Oddball_pause2"], self.txt_ins["Key_to_continue"],self.win, "Black")
            # VF trial_type
            trial_type = "Different"
            if self.stim_trials_list[i][0][1][0] == self.stim_trials_list[i][1][1][0]:
                trial_type = "Same"

            rts = self.oddball_trial(trial_structure, self.stim_trials_list[i], trial_type, block)
            for rt in rts:
                self.oddball_data.addData("RT", rt)
                self.oddball_data.addData("Type", trial_type)
                self.oddball_data.addData("Standard", self.stim_trials_list[i][0][1])
                self.oddball_data.addData("Deviant", self.stim_trials_list[i][1][1])
                self.oddball_data.addData("Block", block)
                self.oddball_data.nextEntry()

        # Deactivate saving on BIOSEMI (need to be added in BIOSEMI config)
        if self.params["EEG"]:
            self.pport.send_signal(255)

    def oddball_trial(self, structure, trial_stim, trial_type, block):
        """
        :param structure: List of int for the order of the trial
        :param trial_stim: [[main.image, main name],[deviant.image, deviant name]]
        :param trial_type: "Same" or "Different"
        :return: A list of reaction time for each target appearance, 0 if the participant did not answer in time
        """
        standard = trial_stim[0][0]
        deviant = trial_stim[1][0]
        key_resp = event.BuilderKeyResponse()

        # Modify trigger according to trial type
        eeg_val_modifier = 0
        if trial_type == "Diffenrent" :
            eeg_val_modifier = 10

        frame_trial = -1

        # Duration of a trial varies by 0 to trial_variance frames
        trial_variance = randint(0,self.params["Variance_by_odd_trial"])

        self.win.flip()
        core.wait(2)
        trial_clock = core.Clock()
        trial_clock.reset()
        target_time = []
        behavioral_time = []
        i = 0

        continue_routine = True
        while continue_routine:
            t = trial_clock.getTime()
            frame_trial += 1
            theseKeys = event.getKeys()
            if len(theseKeys) > 0: # if a key was pressed
                key_resp.keys = theseKeys[-1]  # just the last key pressed
                if key_resp.keys == "q" :
                    core.quit()
                if len(behavioral_time) < len(target_time) : # if there is more target shown than answer received
                    behavioral_time.append(key_resp.clock.getTime())
                key_resp = event.BuilderKeyResponse()
            if len(target_time) > 0 :
                if t > target_time[len(target_time)-1] + 1 :
                    # if one second after target there is no answer, mark answer as False
                    behavioral_time.append(False)
            if frame_trial%(self.params["Min_frames_by_odd_trial"]+trial_variance) == 0:  # New step in structure
                frame_trial = 0
                trial_variance = randint(0,self.params["Variance_by_odd_trial"])
                # Show image according to trial structure
                # Trigger identification
                # 80 Same and main
                # 81 Same and distractor
                # 82 Same and target
                # 90 Different and main
                # 91 Different and distractor
                # 92 Different and target
                if structure[i] == 2:
                    if self.params["EEG"]:
                        self.pport.send_signal(82+eeg_val_modifier+(block-1)*100)
                    standard.setAutoDraw(True)
                    self.target.setAutoDraw(True)
                    target_time.append(t)
                elif structure[i] == 0 :
                    if self.params["EEG"]:
                        self.pport.send_signal(80+eeg_val_modifier+(block-1)*100)
                    standard.setAutoDraw(True)
                    self.fixation_cross_vertical.setAutoDraw(True)
                    self.fixation_cross_horizontal.setAutoDraw(True)
                elif structure[i] == 1 :
                    if self.params["EEG"] :
                        self.pport.send_signal(81+eeg_val_modifier+(block-1)*100)
                    deviant.setAutoDraw(True)
                    self.fixation_cross_vertical.setAutoDraw(True)
                    self.fixation_cross_horizontal.setAutoDraw(True)
                i += 1
            elif frame_trial == self.params["Frames_by_odd_stim"] : # End of stimulus duration
                self.target.setAutoDraw(False)
                standard.setAutoDraw(False)
                deviant.setAutoDraw(False)
                self.fixation_cross_vertical.setAutoDraw(False)
                self.fixation_cross_horizontal.setAutoDraw(False)
                if i == len(structure) :
                    if structure[-1] == 2 or structure[-2] == 2 :
                        if len(behavioral_time) < len(target_time) :
                            behavioral_time.append(False)
                    continue_routine = False
            self.win.flip()
        rt = []
        for i,this_target in enumerate(target_time) :
            if behavioral_time[i] :
                rt.append(behavioral_time[i]-this_target)
            else :
                rt.append(0)
        return rt


