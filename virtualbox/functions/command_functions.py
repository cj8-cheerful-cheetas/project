from .blessed_functions import print_box
from .blessed_functions import print_tree
from .generalfunctions import inAny
from virtualbox.argssystem.functions import expand_args
from virtualbox.argssystem.classes import Keyword, Optional, Flag
from virtualbox.exceptions import NoSuchFileOrDirectory
from virtualbox.exceptions import CommandNotFound
from virtualbox.unicode import encode
from virtualbox.vulnerabilities import VULNERABILITIES, add_failure, add_vulnerabillity, remove_vulnerabillity
from virtualbox.cryptology import encrypt
from config import MAIN_PATH
import random
import time

# COMMAND LIST
functions_list = []
user_commands = {}


# wrappers
def add_function(names, *args):
    def add(function):
        for i in names:
            user_commands[i] = len(functions_list)
        functions_list.append((function, args))
        return function
    return add


# getcommands
def get_entry(name):
    try:
        return functions_list[user_commands[name]]
    except KeyError:
        raise CommandNotFound()


def get_command(name):
    return get_entry(name)[0]


def get_command_args(name):
    return get_entry(name)[1]


def get_command_doc(name):
    return get_command(name).__doc__


# COMMANDS
@add_function(("ls", "dir"), "fs", "user")
def ls(fs, user):
    """ls [NoArgs]
    [EXTEND]
    ls - list files and directories in current directory
    """
    print_box("ls", fs.stringList(user))


def random_test():
    print_box("OS SECURITY",
            ["SECURITY BREACH DETECTED",
            """         ____,'`-, """,
            """         _,--'   ,/::.; """,
            """      ,-'       ,/::,' `---.___        ___,_ """,
            """      |       ,:';:/        ;'"``--./ ,-^.;--. """,
            """       |:     ,:';,'         '         `.   ;`   `-. """,
            """        \:.,:::/;/ -:.                   `  | `     `-. """,
            """         \:::,'//__.;  ,;  ,  ,  :.`-.   :. |  ;       :. """,
            """          \,',';/O)^. :'  ;  :   '__` `  :::`.       .:' ) """,
            """          |,'  |\__,: ;      ;  '/O)`.   :::`;       ' ,' """,
            """               |`--''            \__,' , ::::(       ,' """,
            """               `    ,            `--' ,: :::,'\   ,-' """,
            """                | ,;         ,    ,::'  ,:::   |,' """,
            """                |,:        .(          ,:::|   ` """,
            """                ::'_   _   ::         ,::/:| """,
            """               ,',' `-' \   `.      ,:::/,:| """,
            """             | : _  _   |   '     ,::,' ::: """,
            """              | \ O`'O  ,',   ,    :,'   ;:: """,
            """               \ `-'`--',:' ,' , ,,'      :: """,
            """                ``:.:.__   ',-','        ::' """,
            """                       |:  ::::.       ::' """,
            """                       |:  ::::::    ,::' """
            ])
    print("enter animal above...")
    user_input = input(">>>  ")
    if user_input.lower() == "dog":
        print("correct")
        add_failure()
    else:
        print("incorrect")


@add_function(("cd", ), 'user_input', "fs", "user")
@expand_args(0, "path")
def cd(path: str, fs, user):
    """cd [path:string]
    [EXTEND]
    cd - change directory to specified path
    """
    fs.copy(fs.getDir(user, path.split("/")))
    print_box("getdir", fs.stringList(user))


@add_function(("tree", ), 'fs', 'user')
def dir_cat(fs, user):
    """dir
    [EXTEND]
    dir = print file structure
    """
    print_tree("dir", fs, user)


@add_function(("mkdir", "makedirectory"), 'user_input', 'fs', 'user')
@expand_args(0, "path")
def mkdir(path: str, fs, user):
    """mkdir [path:string]
    [EXTEND]
    mdkir - creates direcotry that will have specified path
    """
    tmp = path.split("/")
    fs.getDir(user, "" if len(tmp) == 0 else tmp[:-1]).mkdir(user, tmp[-1])


@add_function(("touch", "add"), 'user_input', 'fs', 'user')
@expand_args(0, "path")
def add(path: str, fs, user):
    """add [path:string]
    [EXTEND]
    add - creates file that will have specified path
    """
    tmp = path.split("/")
    fs.getDir(user, "" if len(tmp) == 0 else tmp[:-1]).touch(user, tmp[-1])


@add_function(("rm", "remove"), "user_input", "fs", "user")
@expand_args(0, "path")
def rm(path: str, fs, user):
    """rm [path:string]
    [EXTEND]
    rm - removes file or folder that have specified path
    """
    tmp = path.split("/")
    fs.get(user, "" if len(tmp) == 0 else tmp[:-1]).rm(user, tmp[-1])


@add_function(("cp", "copy"), "user_input", "fs", "user")
@expand_args(0, "from_path", "to_path")
def cp(from_path: str, to_path: str, fs, user):
    """cp [from:string] [to:string]
    [EXTEND]
    cp - copies file or directory form 1 path to another
    """
    fs.cp(user, from_path.split("/"), to_path.split("/"))


@add_function(("mv", "move"), "user_input", "fs", "user")
@expand_args(0, "from_path", "to_path")
def mv(from_path: str, to_path: str, fs, user):
    """mv [from:string] [to:string]
    [EXTEND]
    mv - moves file or directory form 1 path to another.
    can be used to rename directories
    """
    fs.mv(user, from_path.split("/"), to_path.split("/"))


@add_function(("help", "h"), "user_input")
@expand_args(0, "name", "extend")
def help_function(name: Optional(str, None), extend: Flag(True) = False):
    """help [function:string] [extend if present print more detailed help]
    [EXTEND]
    help - hymmm i wonder what it does?
    """
    if name is None:
        print_box("commands", user_commands.keys())
        return

    to_print = get_command_doc(name).split("[EXTEND]")
    print_box('helper', to_print[0].strip())

    if extend:
        print_box('helper', to_print[1].strip())


@add_function(("encrypt", "enc"), "user_input", "fs", "user")
@expand_args(0, "file", "password", "mode")
def user_encrypt(file: str, password: encode, fs, user, mode: Keyword(int) = 2):
    """encrypt [file:string] [password:string or int(mode 3)] [mode:int default 2]
    [EXTEND]
    encrypt - encrypts file using 1 of 4 encryption algoritms
    """
    fs.getFile(user, file.split("/")).encrypt(user, password, mode)


@add_function(("encryptword", "encword"), "user_input")
@expand_args(0, "phrashe", "password", "mode")
def encryptword(phrashe: encode, password: encode, mode: Keyword(int) = 2):
    """encrypt [phrashe:string] [password:string or int(mode 3)] [mode:int default 2]
    [EXTEND]
    encryptword - encrypts phrahse using 1 of 4 encryption algoritms and prints it back to user
    """
    print(encrypt(phrashe, password, mode=mode))


@add_function(("decrypt", "dec"), "user_input", "fs", "user")
@expand_args(0, "file", "password", "mode")
def decrypt(file: str, password: encode, fs, user, mode: Keyword(int) = 2):
    """decrypt [file:string] [password:string or int(mode 3)] [mode:int default 2]
    [EXTEND]
    decrypt - decrypts file using 1 of 4 decrytpion algorithms and saves result
    """
    fs.getFile(user, file.split("/")).decrypt(user, password, mode)


@add_function(("decryptread", "dread", "decread"), "user_input", "fs", "user")
@expand_args(0, "file", "password", "mode")
def decryptread(file: str, password: encode, fs, user, mode: Keyword(int) = 2):
    """decryptread [file:string] [password:string or int(mode 3)] [mode:int default 2]
    [EXTEND]
    decryptread - decrypts file using 1 of 4 decrytpion algorithms and prints result
    """
    fs.getFile(user, file.split("/")).decrypt(user, password, mode)


@add_function(("cat", "read"), "user_input", "fs", "user")
@expand_args(0, "file", "bin")
def read(file: str, fs, user, bin: Flag(True) = False):
    """read [file:string] [mode:text]
    [EXTEND]
    read - reads file using binary(bin) or text(text) modes
    """
    print(fs.getFile(user, file.split("/")).read(user, bin))


@add_function(("write", ), "user_input", "fs", "user")
@expand_args(0, "file", "content", "bin")
def write(file: str, content: str, fs, user, bin: Flag(True) = False):
    """write [file:string] [content]
    [EXTEND]
    write - overwrites file with specified content"""
    fs.getFile(user, file.split("/")).write(user, " ".join(content), bin)


def search_back(what, walk, piervous):
    result = []
    for i in walk:
        if isinstance(i, tuple):
            if inAny(what, i[0]):
                result.append(piervous + "/" + i[0])
            result += search_back(what, i[1], piervous + "/" + i[0])
        elif inAny(what, i):
            result.append(piervous + "/" + i)
    return result


@add_function(("search", "find"), "user_input", "fs", "user")
@expand_args(0, "what")
def search(what: str, fs, user):
    """search [name:string]
    [EXTEND]
    search - searches for file that contains name in it's name
    """
    "search [name]"
    result = search_back(what, fs.walk(user), "")

    if len(result) == 0:
        raise NoSuchFileOrDirectory

    print_box("search", result)


@add_function(("portscann", "nmap"), "user_input", "fs", "user", "term")
@expand_args(0, "port")
def portscanner(port: Optional(int, None), fs, user, term):
    """portscan [port:int]
    [EXTEND]
    portscan - scans for port in network
    """
    ports = [22, 80, 9929, 8898, 22542, 187, 32312]
    outputs = ['not a hint', 'a hint']
    if port is not None:
        # Different Prints to show user a portscanner experience and show hint/ no hint
        print_box("PortScanner", [f"Scanning Network for Port: {port}"])
        time.sleep(1)
        term.clear
        print_box("PortScanner", ["Found Port in Network:", f"{port}/TCP [State: open]", "Scanning Port..."])
        time.sleep(1)
        term.clear
        term.clear
        output = random.choice(outputs)
        print_box("PortScanner", [f"Port {port} attackable. ", "Attack launchend. ", f"Output: {output}"])
    else:
        # 5-7 to show user a portscanner experience and show hint/ no hint
        for i in range(random.randint(5, 7)):
            port = ports[i]
            print_box("PortScanner", ["Found Port in Network: ", f"{port}/TCP [State: open]", "Scanning Port..."])
            time.sleep(0.4)
        inp = int(input("Select a port to scan: "))
        with term.cbreak():
            if inp in ports:
                output = random.choice(outputs)
                time.sleep(1)
                term.clear
                print_box("PortScanner", [f"Port {inp} attackable. ", "Attack launchend. ", f"Output: {output}"])
            else:
                print_box("PortScanner", ["The Port you entered wasnt found in the Network!"])


@add_function(("devresetintro", ))
def dev_reset():
    """replace docstring if you want help for this function"""
    # script_dir = os.path.dirname(__file__)
    # script_dir = script_dir.replace('functions/', '') it will crash without argumnts
    with open(MAIN_PATH + 'first_game.txt', 'w') as firstgamefile:
        firstgamefile.truncate()
        firstgamefile.write('0')


def add_vulnerabillity(vulnerability):
    VULNERABILITIES.append(vulnerability)


def remove_vulnerabillity(vulnerability):
    VULNERABILITIES.remove(vulnerability)


@add_function(("vscan", ))
def hint():
    """replace docstring if you want help for this function"""
    print_box("vscan", ["Looking for vulnerabilities..."])
    # selects random vulnerability
    chosen_vulnerability = random.choice(VULNERABILITIES)
    # display our selected vulnerability.
    print_box("vscan", [f"Vulnerability found: {chosen_vulnerability}"])
    # removes vulnerability from the list.
    remove_vulnerabillity(chosen_vulnerability)
    # add 1 failure point.
    add_failure()
