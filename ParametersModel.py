params = {
    # Needed for all exp

    # "True" or "False"
    "Orientation" : "True",
    # List of folder where there is all the stimulus name for each version (list of string)
    "Stim_list_folder": ["C:\\Users\\tsico\\Fish\\Hardest - 1 feature\\ResizedBouche\\5\\"],
    # List of path to texture (before orientation or categories folder if there is) (list of string)
    "Path_texture": ["C:\\Users\\tsico\\Fish\\Hardest - 1 feature\\ResizedBouche\\"],
    # Category folder name (list of string)
    "Cat_folder": ["K\\","L\\"],
    # Path to practice stimuli (String)
    "Practice_path" : "C:\\Exp\\Textures3inv\\PRATIQUE\\",
    # Primer time in float (s)
    "Primer_time": 0.5,
    # Files for instruction in the desired language (String)
    "Francais_ins" : "Instruction_Fish_Francais.json",
    "English_ins" : "Instruction_Fish_English.json",


    # Specific to categorization

    # Path to data folder (String)
    "Cat_saving_path":"C:\\Users\\tsico\\Cat_data\\",
    # Number of block wanted (int)
    "N_block": 4,
    # Number of trial by block (int)
    "Trial_per_block" : 20,
    # Number of trials in practice routine (int)
    "N_Cat_Practice" : 4,
    # Expected answer for category 1 and 2 (string lowercase)
    "Key_answer" : ["k","l"],
    # Duration of stimulus (float)
    "Cat_stim_time": 0.75,
    # Maximum time after the appearance of the stimulus to answer (float)
    "Maxanswer_time": 1.5,
    # Duration of the feedback (float)
    "Feedback_time" : 1.0,


    # Specific to Similarity judgement

    # Path to data folder (String)
    "SJ_saving_path":"C:\\Users\\tsico\\SJ_data\\",
    # Number of trials "Should be an even number for balance" (Int)
    "SJ_trial" : 8,
    # Number of trials in practice routine (int)
    "N_SJ_Practice" : 4,
    # Duration of stimulus (float)
    "SJ_stim_time" : 0.75,
    # Time between first and second stimulus (float)
    "SJ_between_stim_time" : 0.5,


    # Specific to Oddball

    # Target either "cross" or an image (string)
    "Oddball_target" : "Cross",
    # Number of time a deviant will appear, determine the number of img to be shown *10 (int)
    "N_deviant": 54,
    # Determine stimulus duration length, multiply by (1/screen frequency) to know duration (int)
    # Ex : 60 Hz screen, 1/60 = 16.6666, 12 frames = 12*16.666 = 200 ms
    "Frames_by_odd_stim" :12,
    # Determine variance of frames between 2 stimulus (int)
    "Variance_by_odd_trial":5,
    # Determine minimum time between the beginning of a stimulus and the beginning of the next one
    # Should always be bigger than Frames_by_odd_stim (int)
    "Min_frames_by_odd_trial": 30
}