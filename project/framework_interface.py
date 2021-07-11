from os import walk, path, sep
from blessed import Terminal

# local modules
import binary_file_library

# file system imports
from fs.fs_dir import Dir
fs = Dir.FromPath("OS", None, 7, 0, 0)
this_dir = fs

term = Terminal()


class User:
    """temporary user class"""
    uid = 0


cl = ["│", "─", "┌", "┬", "┐", "├", "┼", "┤", "└", "┴", "┘"]
START_PATH = "OS/game_files/"
BLANK_LINES = 50  # number of characters each line should be
print(term.home + term.clear + term.move_y(term.height // 2))

def printtree(header, location):
    print(term.green_on_black(f'┌─ /{header}/' + ('─' * (BLANK_LINES - 6 - len(header))) + '┐'))
    for root, dirs, files in walk(location):
        level = root.replace(START_PATH, '').count(sep)
        indent = '─' * 4 * level
        # finds the length of the directory that is going to be printed
        # takes away the length from the constant variable to find
        # the amount of extra blank spaces needed
        current_line_length = len('├'+'{}{}/'.format(indent, path.basename(root)))
        extra_blank_needed = (BLANK_LINES - current_line_length - 1) * " "  # -1 used to make space for edge of box
        print(term.green_on_black(f'├{indent}{path.basename(root)}/{extra_blank_needed}│'))
        sub_indent = '├' + '─' * 4 * (level + 1)
        for f in files:
            # does the same as above but with the files
            current_line_length = len('{}{}'.format(sub_indent, f))
            extra_blank_needed = (BLANK_LINES - current_line_length - 1) * " "  # -1 used to make space for edge of box
            print(term.green_on_black(f'{sub_indent}{f}{extra_blank_needed}│'))
    print(term.green_on_black(f'└─ /{header}/' + ('─' * (BLANK_LINES - 6 - len(header))) + '┘'))


def print_box(header, textl):
    def print_box_str(ret_string, words):
        # if fits in one line
        if len(words) <= BLANK_LINES - 2:
            ret_string += str(cl[0] + " " + words + " " * int(BLANK_LINES - 3 - len(words)) + cl[0] + "\n")
        # if longer than one line
        else:
            rows = len(words) // (BLANK_LINES - 2) + (len(words) % (BLANK_LINES - 2) != 0)
            startpos = [(BLANK_LINES - 4) * row for row in range(rows + 1)]
            for row in range(rows):
                # for last row of long line
                if row == rows - 1:
                    ret_string += str(cl[0] + " " + words[startpos[-2]:-1] +
                    " " * int(BLANK_LINES - 3 - len(words[startpos[-2]:-1])) + cl[0] + "\n")
                # for other rows of long line
                else:
                    ret_string += str(cl[0] + " " + words[startpos[row]:startpos[row + 1]] + " " + cl[0] + "\n")
        return ret_string

    ret_string = str(cl[2] + cl[1] + f" /{header}/ " + cl[1] * int(BLANK_LINES - 7 - len(header)) + cl[4] + "\n")
    for words in textl:
        if type(words) == list:
            for word in words:
                ret_string = print_box_str(ret_string, word)
        elif type(words) == str:
            ret_string = print_box_str(ret_string, words)
        else:
            print("error in printhelp: second input should be a list containing strings and/or lists of strings")
    ret_string += str(cl[8] + cl[1] * (BLANK_LINES - 2) + cl[10])
    return ret_string


def start():
    printtree("System", START_PATH)
    user_input_cmd()


def user_input_cmd():
    print(term.green_on_black(""))
    showing_input_menu = True
    while showing_input_menu:
        user_input = input(">>>  ").lower()
        # commands list V
        if user_input[:4] == "help" or user_input[:1] == "h":
            start_help(user_input)
            showing_input_menu = False
        if user_input[:3] == "add":
            start_add(user_input)
            showing_input_menu = False
        if user_input[:3] == "dir":
            start_dir(user_input)
            showing_input_menu = False
        if user_input[:10] == "quickcrypt":
            start_quickcrypt(user_input)
            showing_input_menu = False
        if user_input[:4] == "read":
            start_read(user_input)
            showing_input_menu = False
        if user_input == "ls":
            for i in this_dir.ls(User).keys():
                print(i)
        if user_input[:2] == "cd":
            try:
                this_dir = this_dir.getDir(User(), user_input[3:])
            except Exception as e:
                print(e)
        if user_input[:5] == "mkdir":
            try:
                this_dir.mkdir(User, user_input[6:])
            except Exception as e:
                print(e)
        if user_input[:5] == "touch":
            try:
                this_dir.touch(User, user_input[6:])
            except Exception as e:
                print(e)
        if user_input[:2] == "rm":
            try:
                this_dir.rm(User, user_input[3:])
            except Exception as e:
                print(e)

def start_help(user_input):
    print(term.home + term.clear + term.move_y(term.height // 2))
    user_input += " 1 2 3 "  # place holder inputs which stops the user from entering errors
    user_input = "help add"
    user_input = user_input.split()
    user_input_dir = {
        "add": ["Help", ["add [file path]", "- creates a new file with a specified name in specified directory"]],
        "remove" : ["Help", ["remove [file path]", "- removes a new file with a specified name in specified directory"]],
        "dir": ["Help", ["dir", "- shows full user directory"]],
        "help" : ["Help", ["help (command)", "- explains what the specific command does"]],
        "quickcrypt": ["Help", ["quickcrypt (file path) (password)", "- file encryption tool"]],
        "read":["Help", ["read (file path)", "- reads a files content"]]
    }
    if user_input[1] in user_input_dir:
        for heade, lis in user_input_dir[user_input[1]]:
            print(term.green_on_black(print_box(heade, lis)))
    else:
        print(term.green_on_black(print_box("Help", ["help (command)",
                                                     "add [name]",
                                                     "remove [name]",
                                                     "dir",
                                                     "read [file path]",
                                                     "quickcrypt [file path] [password]"
                                                     ])))
    user_input_cmd()


def start_dir(user_input):
    user_input += " 1 1 1 "
    user_input = user_input.split()
    print(term.home + term.clear + term.move_y(term.height // 2))
    if user_input[1] == "1":
        printtree("System", START_PATH)
    else:
        printtree("System", f"OS/game_files/{user_input[1]}")
    user_input_cmd()


def start_add(user_input):
    # print(term.home + term.clear + term.move_y(term.height // 2))
    # user_input = input.split()
    # path_l = input[1].split("/")
    # if not os.path.isdir(path_l[0]):
    #     os.makedirs(path_l[0])
    #     open(os.path.join(path_l[0], path_l[1])).close()
    # else:
    #     if "." in path_l[0]:
    #         open(path_l[0]).close()
    #     else:
    #         open(os.path.join(path_l[0], path_l[1])).close()
    #
    # start_dir("dir")
    user_input_cmd()


def start_read(user_input):
    user_input = user_input.split()


def start_quickcrypt(user_input):
    # "quickcrypt [file path] [password]"
    user_input += " 1 2 3 "  # place holder inputs which stops the user from entering errors
    user_input = user_input.split()
    binary_file_library.decrypt_file(user_input[1], user_input[2])


if __name__ == "__main__":
    start()
