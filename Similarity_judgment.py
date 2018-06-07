
import random
from psychopy import visual, event, core, data
from psychopy.constants import *
from Exp_general_function import countdown, write_instruction, get_practice_stim
from SendSignal import PortParallel


def get_list_sj_trial_with_orientation(cat_list, win, params):
    """
    :param cat_list: Name of all stim in a list
    :param win: Exp window
    :param params: Exp parameters (SJ_trial = number of trials, Path_texture = Path to the texture without orientation
                                    This folder should contain a folder for orientation from 5 to 355 for every 15 degree
                                    difference, Cat_folder = Name of the folder for each of the 2 categories)
    :return: A shuffled list that contain a dict for each trial
            For each intra category trial with a difference x in orientation there is one with the same difference as
            inter category
            Dict contain (stim1, stim2 = stim.image.window / cat_stim1 = Category of stimulus 1 eith 0 or 1 /
                            ori1, ori2 = orientation of each stimulus / stim1_name, stim2_name = stimulus name)
    """
    trials = []
    n_trials = params["SJ_trial"]
    stimulus_list = cat_list
    random.shuffle(stimulus_list[0])
    random.shuffle(stimulus_list[1])
    n = 0
    while len(trials) < n_trials :
        ori_diff = random.randint(-6,6) * 15
        for i in range(2) :
            ori_1 = random.randint(1, 24) * 15 - 10
            ori_2 = (ori_1 - ori_diff) % 360
            diff_cat = 0
            if i == 0 :
                diff_cat = 1
            same_cat_stim1 = visual.ImageStim(win, image=params["Path_texture"]+str(ori_1)+"\\"
                                                   +params["Cat_folder"][i]+stimulus_list[i][n])
            same_cat_stim2 = visual.ImageStim(win, image=params["Path_texture"] + str(ori_2) + "\\"
                                                  + params["Cat_folder"][i] + stimulus_list[i][n+1])
            diff_cat_stim1 = visual.ImageStim(win, image=params["Path_texture"] + str(ori_1) + "\\"
                                                         + params["Cat_folder"][i] + stimulus_list[i][n+2])
            diff_cat_stim2 = visual.ImageStim(win, image=params["Path_texture"] + str(ori_2) + "\\"
                                                         + params["Cat_folder"][diff_cat] +
                                                         stimulus_list[diff_cat][n + 3])
            trials.append({"stim1" : same_cat_stim1, "stim2" : same_cat_stim2, "cat_stim1" :i, "type" : "Same",
                           "ori1" : ori_1, "ori2" : ori_2, "stim1_name" : stimulus_list[i][n],
                           "stim2_name" : stimulus_list[i][n+1]})
            trials.append({"stim1" : diff_cat_stim1, "stim2" : diff_cat_stim2, "cat_stim1" :i, "type" : "Different",
                           "ori1" : ori_1, "ori2" : ori_2, "stim1_name" : stimulus_list[i][n+2],
                           "stim2_name" : stimulus_list[diff_cat][n+3]})
        n += 4
        if n > len(stimulus_list[0]) - 4 or len(stimulus_list[1]) - 4 :
            random.shuffle(stimulus_list[0])
            random.shuffle(stimulus_list[1])
            n = 0
    random.shuffle(trials)
    return trials

class sj_trials(object):
    def __init__(self, params = None, win=None, exp_info=None, txt_ins=None, stimulus_list=None):
        self.win = win
        self.params = params
        self.exp_info = exp_info
        self.txt_ins = txt_ins
        self.stimulus_list = stimulus_list

        if self.params["EEG"] :
            self.pport = PortParallel()
        else :
            self.pport = False

        #Get a list of stimuli for the practice trial
        #The list contain all the stimuli in the practice folder as win.image
        self.practice_stim_list = get_practice_stim(params["Practice_path"], self.win)


        self.stimulus_time = float(params[u"SJ_stim_time"])
        self.primer_time = float(params[u"Primer_time"])
        self.between_stim_time = float(params[u"SJ_between_stim_time"])

        # Create the mouse, primer and similarity bar component
        self.primer = visual.Circle(win=self.win, radius=45, units="pix", fillColor=[-1, -1, -1],
                                    lineColor=[-1, -1, -1])
        self.horizontal_line = visual.Line(win=self.win, units="pix", lineColor=[+1, +1, +1],
                                           lineWidth=10, start=(-50, 0), end=(+50, 0))
        self.vertical_line = visual.Line(win=self.win, units="pix", lineColor=[+1, +1, +1],
                                         lineWidth=10, start=(0, -50), end=(0, +50))
        self.center = visual.Circle(win=self.win, radius=5, units="pix", fillColor=[-1, -1, -1], lineColor=[-1, -1, -1])
        self.similarity_bar = visual.Line(win=self.win, units="pix", lineColor=[-1, -1, -1], lineWidth=100,
                                          start=(-500, 0), end=(+500, 0))
        self.cursor = visual.Line(win=self.win, lineColor=[+1, +1, +1], lineWidth=10,
                                  start=(0, -0.1), end=(0, +0.1))
        self.txt_diff = visual.TextStim(win=self.win, text=self.txt_ins["Different"], pos=(-0.7, -0.2), color="Black")
        self.txt_sim = visual.TextStim(win=self.win, text=self.txt_ins["Similar"], pos=(+0.7, -0.2), color="Black")
        self.mouse = event.Mouse(visible=False, newPos=None, win=None)

        #Adapt the trial list if stimuli orientation is changing
        if self.params["Orientation"] == "True" :
            if exp_info['Exp'] == "Fish" :
                self.sj_trials_list = get_list_sj_trial_with_orientation(stimulus_list, self.win, params)
        else :
            pass

        #Create data handler
        file_name = exp_info['Exp'] + "_Version" + exp_info['Version'] + "_" + exp_info["Name"] + "_SJ"
        self.sj_data = data.ExperimentHandler(name='SJ',
                                               version=exp_info['Version'],
                                               extraInfo=exp_info,
                                               runtimeInfo=None,
                                               savePickle=False,
                                               saveWideText=True,
                                               dataFileName=params["SJ_saving_path"]+file_name,
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
        for i in range(self.params["N_SJ_Practice"]):
            x = random.randint(0, len(self.practice_stim_list) - 2)
            stim_1 = self.practice_stim_list[x]
            stim_2 = self.practice_stim_list[x+1]
            x = self.trial([stim_1, stim_2], "Same", 0)
        if self.pport :
            self.params["EEG"] = True

    def sj_routine(self, block):
        """
        :param block: Determine which block is it
        Routine for 1 block of similarity judgement
        """
        # Write instruction and practice if it's block 1
        if self.params["EEG"]:
            self.pport.send_signal(70+block)

        if block == 1 :
            write_instruction(self.txt_ins["SJ_ins1"], self.txt_ins["Key_to_continue"], self.win, "Black")
            write_instruction(self.txt_ins["SJ_ins2"], self.txt_ins["Key_to_continue"], self.win, "Black")
            write_instruction(self.txt_ins["SJ_ins3"], self.txt_ins["Key_to_continue"], self.win, "Black")
            write_instruction(self.txt_ins["SJ_ins4"], self.txt_ins["Key_to_continue"], self.win, "Black")
            countdown(self.txt_ins["Practice_countdown"], 5, self.win, "Black")
            self.practice_routine()
            write_instruction(self.txt_ins["Practice_end"], self.txt_ins["Key_to_continue"],self.win, "Black")
        else :
            write_instruction(self.txt_ins["SJ_ins5"], self.txt_ins["Key_to_continue"], self.win, "Black")
            write_instruction(self.txt_ins["SJ_ins6"], self.txt_ins["Key_to_continue"], self.win, "Black")

        #Start the trials
        countdown(self.txt_ins["SJ_countdown"], 5, self.win, "Black")
        for n in range(self.params["SJ_trial"]) :
            #Iterate in trials
            stim1_cat = self.sj_trials_list[n]["cat_stim1"]
            stim1_name = self.sj_trials_list[n]["stim1_name"]
            stim2_name = self.sj_trials_list[n]["stim2_name"]
            stim1 = self.sj_trials_list[n]["stim1"]
            stim2 = self.sj_trials_list[n]["stim2"]
            trial_type = self.sj_trials_list[n]["type"]
            trial = self.trial([stim1, stim2], trial_type, stim1_cat)

            #Add data to this entry
            self.sj_data.addData("Block", block)
            self.sj_data.addData("Index", n+1)
            self.sj_data.addData("Score", trial)
            self.sj_data.addData("Type", trial_type)
            self.sj_data.addData("Cat_stim1", stim1_cat)
            if self.params["Orientation"] == "True":
                stim1_orientation = self.sj_trials_list[n]["ori1"]
                stim2_orientation = self.sj_trials_list[n]["ori2"]
                self.sj_data.addData("Stim1_orientation", stim1_orientation)
                self.sj_data.addData("Stim2_orientation", stim2_orientation)
            self.sj_data.addData("Stim1", stim1_name)
            self.sj_data.addData("Stim2", stim2_name)
            self.sj_data.nextEntry()

    def sj_answer(self) :
        """
        Routine to get similarity rating
        """
        #Show bar and cursor
        self.similarity_bar.setAutoDraw(True)
        self.txt_sim.setAutoDraw(True)
        self.txt_diff.setAutoDraw(True)
        self.cursor.setPos((0, 0))
        self.cursor.setAutoDraw(True)
        self.win.flip()

        #Adjust the mouse so it is in the middle and hide it
        self.mouse.setPos(newPos=(0, 0))
        max__x = 0.72 #Might have to be adjusted for your screen
        min__x = -0.72
        range__x = max__x - min__x
        score = 0
        continue_routine = True
        while continue_routine == True:
            #Adapt the cursor position to the mouse position
            #Prevent  it to go outside the similarity bar
            mouse_pos = (self.mouse.getPos()[0])
            if mouse_pos > max__x:
                self.mouse.setPos(newPos=(max__x, 0))
                mouse_pos = self.mouse.getPos()[0]
            elif mouse_pos < min__x:
                self.mouse.setPos(newPos=(min__x, 0))
                mouse_pos = self.mouse.getPos()[0]
            score = int((mouse_pos - min__x) / range__x * 100)
            self.cursor.setPos((mouse_pos, 0))
            self.win.flip()
            if self.mouse.getPressed()[0] == 1:
                #If there is a click get rating and stop
                continue_routine = False
        self.cursor.setAutoDraw(False)
        self.similarity_bar.setAutoDraw(False)
        self.txt_sim.setAutoDraw(False)
        self.txt_diff.setAutoDraw(False)
        return score

    def trial(self, stim_pair,trial_type, stim1_cat) :
        """
        :param stim_pair: [Stim1.image, Stim2.image]
        :param trial_type: "Same" or "Different"
        :param stim1_cat: Category of stim1 either 0 or 1
        :return: Score of the similarity rating (Int)
        """
        stim1 = stim_pair[0]
        stim2 = stim_pair[1]
        trialClock = core.Clock()
        trialClock.reset()

        # Add status to trial components
        trialComponents = [stim1, stim2, self.primer]
        for thisComponent in trialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        #Trial routine
        continueRoutine = True
        while continueRoutine:
            t = trialClock.getTime()
            if t < self.primer_time and self.primer.status == NOT_STARTED: # Beginning of the trial
                self.primer_activation(True)
                self.primer.status = STARTED
            elif t > self.primer_time and self.primer.status == STARTED: # Show stim1
                self.primer_activation(False)
                self.primer.status = STOPPED
                stim1.setAutoDraw(True)
                stim1.status = STARTED
                if self.params["EEG"]:
                    val_type = 0
                    if trial_type == "Same" :
                        val_type = 10
                    # Trigger identification
                    # 101 Category 1 and same
                    # 111 Category 1 and diff
                    # 201 Category 2 and same
                    # 211 Category 2 and diff
                    self.pport.send_signal((int(stim1_cat)+1)*100 + val_type+1)
            elif t > self.primer_time + self.stimulus_time and stim1.status == STARTED : # Hide stim1
                stim1.setAutoDraw(False)
                stim1.status = STOPPED
            elif t > self.primer_time + self.stimulus_time + self.between_stim_time and stim2.status == NOT_STARTED:
                # Show stim2
                stim2.setAutoDraw(True)
                stim2.status = STARTED
                if self.params["EEG"]:
                    val_type = 0
                    if trial_type == "Same" :
                        val_type = 10
                    # Trigger identification
                    # 102 Category 1 and same
                    # 112 Category 1 and diff
                    # 202 Category 2 and same
                    # 212 Category 2 and diff
                    self.pport.send_signal((int(stim1_cat)+1)*100 + val_type+1)
            elif t > self.primer_time + self.stimulus_time*2 + self.between_stim_time and stim2.status == STARTED:
                # Hide stim2
                stim2.setAutoDraw(False)
                stim2.status = STOPPED
                continueRoutine = False
            self.win.flip()

        score = self.sj_answer()#Get rating
        return score
