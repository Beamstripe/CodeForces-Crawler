import hashlib
from typing_extensions import ParamSpec
import requests
import time
Verdictshort={'PARTIAL':'partial','COMPILATION_ERROR':'CE','RUNTIME_ERROR':'RE'
,'WRONG_ANSWER':'WA','PRESENTATION_ERROR':'PE','TIME_LIMIT_EXCEEDED':'TLE','OK':'Accepted','MEMORY_LIMIT_EXCEEDED':'MLE'
,'IDLENESS_LIMIT_EXCEEDED':'IDLE','SECURITY_VIOLATED':'SEC','CRASHED':'crash','INPUT_PREPARATION_CRASHED':'INPUT crash'
,'CHALLENGED':'challenged','SKIPPED':'skip','TESTING':'running','REJECTED':'rej','FAILED':'fail'}
def encode_sha512(key):
    hashObj=hashlib.sha512(key.encode("utf-8"))
    return hashObj.hexdigest()
key='49a7a43da05bd6f8ccf34b5115b942fdfbb44019'
sec='9815d2ebb279a9f49d91be6654d37a47af860a39'

def printMenu():    
    print('Welcome to CodeForces API system!')
    print('User: Beamstripe')
    print('Friends: likely, YoungChigga')
    print('Options:')
    print("'s':status shortcut")
    print('1.contest')
    print('2.problemset')
    print('3.user')
    print('4.blog')
    print("'q':quit")
    op=input()
    return op

def connectRequest(url):
    jsonRequest=requests.get(url)
    rcnt=0
    while not (jsonRequest.status_code==200 and jsonRequest.json()['status']=='OK'):
        jsonRequest=requests.get(url)
        rcnt+=1
        if rcnt>20:
            if jsonRequest.status_code==200:
                print('network error')
            else:
                print('Access denied:',jsonRequest.status_code)
            return (False,jsonRequest)
    return (True,jsonRequest)
def dateFormatted(s):
    if s!=None:
        time_local=time.localtime(s)
        return time.strftime("%Y-%m-%d %H:%M:%S",time_local)
    else:
        return "-"
def timeFormatted(s):
    if s!=None:
        d=s/86400
        h=s%86400/3600
        m=s%3600/60
        if int(d)==0:
            str="%02d:%02d"%(h,m)
        else:
            str="%dD %02d:%02d"%(d,h,m)
    else:
        return "-"
    return str
def stringShrink(s,n):
    if len(s)>=n:
        string=s[0:n-2]
        string=string+".."
    else:
        string=s
    return string
def checkStatus(contestID,scope,Count,From):
    if scope=='all':
        requestURL='https://codeforces.com/api/contest.status?contestId=%s&from=%s&count=%s'%(contestID,From,Count)
    else:
        requestURL='https://codeforces.com/api/contest.status?contestId=%s&handle=%s&from=%s&count=%s'%(contestID,scope,From,Count)
    jsonRequest=connectRequest(requestURL)
    if jsonRequest[0]:
        print('---------------------------------------------status-----------------------------------------------')
        print('SubmissionID   ID             Problem                Lang            Verdict     Time    Memory')
        dic=jsonRequest[1].json()
        Count=len(dic['result'])
        try:
            for i in range(0,Count):
                print("%-12d   %-14s %s:%-20s %-15s %-11s %-4d ms %-6d KB"%(dic['result'][i]['id'],stringShrink(dic['result'][i]['author']['members'][0]['handle'],14),dic['result'][i]['problem']['index'],stringShrink(dic['result'][i]['problem']['name'],20),stringShrink(dic['result'][i]['programmingLanguage'],15),stringShrink(Verdictshort[dic['result'][i]['verdict']],11),dic['result'][i]['timeConsumedMillis'],dic['result'][i]['memoryConsumedBytes']/1000))
        except Exception as e:
            print("Error:",e)
        return

def checkHacks():
    return
def checkStandingNRatings(contestID,scope):
    return
def checkContestList(gym,maxlen):
    if gym == True:
        requestURL='https://codeforces.com/api/contest.list?gym=true'
    else:
        requestURL='https://codeforces.com/api/contest.list'
    jsonRequest=connectRequest(requestURL)
    i=0
    if jsonRequest[0]:
        dic=jsonRequest[1].json()
        print('----------------------------------Upcoming-Contests&Current-Contests----------------------------------')
        print('%6s   %60s   %19s  %9s'%('ID','Contest Name','Start Time','Length'))
        while dic['result'][i]['phase']=='BEFORE':
            print('%6d   %60.60s   %19s  %9s'%(dic['result'][i]['id'],dic['result'][i]['name'],dateFormatted(dic['result'][i].get('startTimeSeconds')),timeFormatted(dic['result'][i].get('durationSeconds'))))
            i+=1
        print('--------------------------------------------Finished-Contests-----------------------------------------')
        # print('%4s %60s %23s %s'%('ID','Contest Name','Start Time','Length'))
        while i<maxlen:
            print('%6d   %60.60s   %19s  %9s'%(dic['result'][i]['id'],dic['result'][i]['name'],dateFormatted(dic['result'][i].get('startTimeSeconds')),timeFormatted(dic['result'][i].get('durationSeconds'))))
            i+=1
def contestOperation():
    print('Contest operations:')
    print('1.View contest list')
    print('2.View gym contest list')
    print('3.Standings and rating changes')
    print("'q':quit")
    option=input()
    if option=='1' or option=='2':
        lent=eval(input('input the max length of the list:'))
        checkContestList(option=='2',lent)
    elif option=='3':
        checkStandingNRatings()
    return

def main():
    while True:
        option=printMenu()
        if option=='q':
            print('Exit')
            break
        elif option=='s':
            str=input('Please input the parameters:')
            (contestid,scope,count,From)=str.split()
            checkStatus(contestid,scope,count,From)
        elif option=='1':
           contestOperation()
        else:
            pass
    return
main()

        