import sys
import re


# no_of_states = number of states of given Turing Machine
# final_states = list of final states
# transitions = list of elements of the following type:
#               1st element = current state of the Turing Machine
#               2nd element = current symbol (where the cursor is situated)
#               3rd element = next state (the state the Machine will be after this transition)
#               4th element = new symbol that will be written in place of the current symbol
#               5th element = where the cursor will be moved: L,R,H (left, right, halt)
class Turingmachine:
    no_of_states = 0
    final_states = []
    transitions = []


# Reads the encoding of a Turing Machine from stdin
# Returns a class of type Turingmachine
def read_tm():
    turing_machine = Turingmachine()
    turing_machine.no_of_states = input()
    final_states_line = sys.stdin.readline()
    final_states_line = final_states_line.rstrip()
    turing_machine.final_states = final_states_line.split()
    lines = sys.stdin.readlines()
    for line in lines:
        line = line.rstrip()
        line = line.split(" ")
        curr_state = line[0]
        curr_sym = line[1]
        nxt_state = line[2]
        new_sym = line[3]
        cursor = line[4]
        turing_machine.transitions.append((curr_state, curr_sym, nxt_state, new_sym, cursor))
    return turing_machine


# Takes as input a Turing Machine and a configuration
# Returns the next configuration or None if there isn't any
# Searches in all transitions in the Turing Machine for the symbol and state
# in the configuration given and does the transition:
# changes the current symbol and moves the cursor
def step(turing_machine, configuration):
    for trans in turing_machine.transitions:
        if trans[0] == configuration[1]:
            if trans[1] == configuration[2][0]:
                configuration[1] = trans[2]
                if trans[4] == 'R':
                    configuration[0] = configuration[0] + trans[3]
                    configuration[2] = (configuration[2])[1:]
                    if len(configuration[2]) == 0:
                        configuration[2] = '#'
                elif trans[4] == 'L':
                    configuration[2] = trans[3] + configuration[2][1:]
                    configuration[2] = configuration[0][-1] + configuration[2]
                    configuration[0] = configuration[0][:-1]
                    if len(configuration[0]) == 0:
                        configuration[0] = '#'
                elif trans[4] == 'H':
                    configuration[2] = trans[3] + configuration[2][1:]
                return configuration


# Reads a line of configurations and returns a list
# with the configuration formatted so that it only keeps the numbers
def read_configurations():
    cfg_list = []
    cfg_line = (sys.stdin.readline()).rstrip()
    cfg_line = re.findall('\\([^,]*,[^,]*,[^)]*\\)', cfg_line)
    for cfg in cfg_line:
        cfg = cfg.replace('(', '')
        cfg = cfg.replace(')', '')
        cfg = cfg.split(',')
        cfg_list.append(cfg)
    return cfg_list


# Runs all the configurations in the configuration_list
# Prints the following configuration of given configuration or False
# if there is none for every configuration in the list
def step_print(turing_machine, configuration_list):
    step_message = ""
    for configuration in configuration_list:
        next_cfg = step(turing_machine, configuration)
        if next_cfg is None:
            step_message += "False "
        else:
            step_message += "(" + next_cfg[0] + "," + next_cfg[1] + "," + next_cfg[2] + ") "
    step_message = step_message[:-1]
    print(step_message)


# Runs all the words in word_list in the Turing Machine and prints
# the result (True or False) for every word
# !!!Caution: only works on non-looping Turing Machines!!!
def accept_print(turing_machine, word_list):
    accept_message = ""
    for word in word_list:
        curr_cfg = ["#", "0", word]
        while True:
            curr_cfg = step(turing_machine, curr_cfg)
            if curr_cfg is None:
                accept_message += "False "
                break
            if curr_cfg[1] in turing_machine.final_states:
                accept_message += "True "
                break
    accept_message = accept_message[:-1]
    print(accept_message)


# Runs all the words in word_list in the Turing Machine for k steps
# taken from k_list (each word must have a corresponding k)
# Prints the result (True or False) for all words
def k_accept_print(turing_machine, word_list, k_list):
    k_accept_message = ""
    for i in range(len(word_list)):
        curr_cfg = ["#", "0", word_list[i]]
        if int(k_list[i]) == 0:
            if "0" in turing_machine.final_states:
                k_accept_message += "True"
            else:
                k_accept_message += "False "
            continue
        for j in range(int(k_list[i])):
            curr_cfg = step(turing_machine, curr_cfg)
            if curr_cfg is None:
                k_accept_message += "False "
                break
            if curr_cfg[1] in turing_machine.final_states:
                k_accept_message += "True "
                break
            if j == int(k_list[i]) - 1:
                k_accept_message += "False "
    k_accept_message = k_accept_message[:-1]
    print(k_accept_message)


# Separates words from corresponding k number of steps
# Returns list of words as first parameter and list of
# integer values of the corresponding k value
def separate_words_steps(line):
    word_list = []
    k_list = []
    for word in line:
        word, k = word.split(",")
        word_list.append(word)
        k_list.append(k)
    return word_list, k_list


if __name__ == "__main__":
    command = (sys.stdin.readline()).rstrip()
    if command == "step":
        cfg_l = read_configurations()
        tm = read_tm()
        step_print(tm, cfg_l)
    if command == "accept":
        word_l = (sys.stdin.readline()).rstrip().split()
        tm = read_tm()
        accept_print(tm, word_l)
    if command == "k_accept":
        k_accept_line = (sys.stdin.readline()).rstrip().split()
        word_l, k_l = separate_words_steps(k_accept_line)
        tm = read_tm()
        k_accept_print(tm, word_l, k_l)
