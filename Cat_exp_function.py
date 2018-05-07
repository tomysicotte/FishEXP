from psychopy import data, gui, core, visual, event


def get_info_from_dlg(dict_info) :
    "Return answer as expInfo(dict) for keys in dict_info"
    my_dlg = gui.Dlg(title="Exp Info")
    for key in dict_info :
        my_dlg.addField(key + " :", choices=dict_info[key])
    dlg = my_dlg.show()
    expInfo = {}
    for i,key in enumerate(dict_info) :
        expInfo[key] = dlg[i]
    expInfo['date'] = data.getDateStr()
    return expInfo


def write_instruction(sentence, win, color):
    """

    Fonction qui affiche un texte et attend pour qu'on appuie sur une touche
    Il y aura une indication d'appuyer sur une touche pour continuer dans le bas.

    """
    win = win
    instruction = visual.TextStim(win, text=sentence, pos=(0.0, 0.2), color=color)
    instruction.draw()
    continuer = visual.TextStim(win, text="Appuyer sur une touche pour continuer", pos=(0.0, -0.6), height=0.07,
                                color=str(color))
    continuer.draw()
    win.flip()
    thisResp = None
    while thisResp == None:
        allKeys = event.waitKeys()
        for thisKey in allKeys:
            if thisKey == "q":
                core.quit()
            thisResp = 1


def countdown(directive, temps, win, color):
    """
    Fonction qui cree un decompte d'une duree (temps) en secondes
    Explication sera le texte qui apparait au dessus des secondes,
    exemple : "L'experimentation commmence dans :"
    """

    win = win
    seconds = temps
    directive_text = directive
    while seconds > 0:
        directive_countdown = visual.TextStim(win, text=directive_text, pos=(0.0, 0.2), color=color)
        directive_countdown.draw()
        time_countdown = visual.TextStim(win, text=str(seconds), pos=(0.0, -0.1), height=0.5, color=color)
        time_countdown.draw()
        seconds -= 1
        win.flip()
        core.wait(1)