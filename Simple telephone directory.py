# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 18:23:21 2018

@author: ARMS COMPUTERS
"""

import csv
import os

phones = []
name_pos = 0
phone_pos = 1
phone_header = [ 'Name', 'Phone Number']

def proper_menu_choice(which):
    if not which.isdigit():
        print("'" +which+ "' needs to be the number of a phone!")
        return False
    which = int(which)
    if which < 1 or which > len(phones):
        print("'" + str(which) + "' needs to be the number of a phone!")
        return False
    return True
    

def show_phones():
    show_phone(phone_header,"")
    index = 1
    for phone in phones:
        show_phone(phone, index)
        index += 1
    print()
     
    
def show_phone(phone, index):
    outputstr = "{0:>3} {1:<20} {2:>16}"
    print(outputstr.format(index, phone[name_pos], phone[phone_pos]))
    
    
def create_phone():
    print("Enter the data for a new phone")
    newname = input("Enter name: ")
    newphone_num = input("Enter phone number: ")
    phone = [newname,newphone_num]
    phones.append(phone)
    print()
    
def delete_phone(which):
    if not proper_menu_choice(which):
        return
    which = int(which)
    del phones[which-1]
    print("Deleted phone # ", which)
    
def edit_phone(which):
    if not proper_menu_choice(which):
        return
    which = int(which)
    phone = phones[which-1]
    
    print("Enter the data for a new phone. Press <enter> to leave unchanged.")
    
    print(phone[name_pos])
    newname = input("Enter phone name to change or press return: ")
    if newname == "":
        newname = phone[name_pos]
    
    print(phone[phone_pos])
    newphone_num = input("Enter new phone number to change or press return: ")
    if newphone_num == "":
        newphone_num = phone[phone_pos]
    
    phone = [newname,newphone_num]
    phones[which-1] = phone
          
def reorder_phones():
    #phones.sort(key = lambda x: x[name_pos])
    phones.sort() 
    
def save_phone_list():
    f = open("myphones.csv", "w", newline = '')
    for item in phones:
        csv.writer(f).writerow(item)
    f.close()
    
def load_phone_list():
    if os.access("myphones.csv",os.F_OK):
        f = open("myphones.csv")
        for row in csv.reader(f):
            phones.append(row)
        f.close()

def menu_choice():
    
    print("Choose one of the following options?")
    
    print("   s) Show")
    print("   n) New")
    print("   d) Delete")
    print("   e) Edit")
    print("   r) Reorder")
    print("   q) Quit")
    
    
    choice = input("Choice: ")
    
    if choice.lower() in ['s','n','d','e','q','r']:
        return choice.lower()
    else:
        print(choice +"?" + " That is an invalid option!!!")
        return None
    
def main_loop():
    
    load_phone_list()
    
    while True:
        choice = menu_choice()
        if choice == None:
            continue
        if choice == 'q':
            print("Exiting...")
            break
        elif choice == 's':
            show_phones()
        elif choice == 'n':
            create_phone()
        elif choice == 'd':
            which = input("Which item you want to delete? ")
            print("which is ", which)
            delete_phone(which)
        elif choice == 'e':
            which = input("Which item you want to edit? ")
            print("which is ", which)
            edit_phone(which)
        elif choice == 'r':
            reorder_phones()
        else:
            print("Invalid Choice.")
            
    save_phone_list()
        
if __name__ == '__main__':
    main_loop()