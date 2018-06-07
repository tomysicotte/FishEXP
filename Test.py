from psychopy import visual, event, core, data
from Exp_general_function import get_info_from_dlg


win = visual.Window(fullscr=True, color="white")

win.flip()

core.wait(1)

win.close()

exp_info = get_info_from_dlg({"Exp": ["Fish", "Textures"],"Langage": ["Francais", "English"], 'EEG': ['Yes', 'No']})