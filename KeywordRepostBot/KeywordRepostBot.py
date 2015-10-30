import time
import praw
import sys

#this script will search for certain keywords in the titles of posts
#in a list of subreddits you define, and then reposts those
#posts to a repository subreddit that you define.

AGENT = '' #Tell the reddit admins what this bot does, and who owns it

#Reddit Account Info
USERNAME = ""   #Reddit Account Username
PASSWORD = ""   #Reddit Account Password
SOURCES = [""] #Subreddit to be search
REPOSITORY = "" #Subreddit for links to be posted

KEYWORDS = [] #Keywords to search for

    
def searchAndRepostBot():
    r = praw.Reddit(user_agent = AGENT)
    print("Logging in to Reddit...")
    try:
        
        r.login(USERNAME, PASSWORD)
    except:
        print("LOGIN FAILED")
        sys.exit()

    for SOURCE in SOURCES:
        subreddit = r.get_subreddit(SOURCE)
        repository = r.get_subreddit(REPOSITORY)
        print("Visiting Subreddit...(" + SOURCE + ")")
    
        submissions = subreddit.get_hot(limit=25)
        repositorySubmissions = subreddit.get_hot(limit=25)
    
        print("Parsing posts...")
    
        for submission in submissions:
            try:
                sbody = submission.selftext.lower()
                stitle = submission.title.lower()
    
                if any(key.lower() in sbody for key in KEYWORDS or key.lower() in stitle for key in KEYWORDS):
                    print("Result found: ")
                    print(submission.url)
                    print("Posting...")
                    r.submit(repository, "[X-Post " + SOURCE + "] " + submission.title, submission.url)
                    time.wait(2)
            except AttributeError:
                    pass
    print("DONE")
searchAndRepostBot()
sys.exit()
