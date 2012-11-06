
import requests
import webbrowser
import time

def print_top(subreddit='all'):
    url = "http://www.reddit.com/r/"+subreddit+".json"

    r = requests.get(url)
 
    stories = {}

    stories['data'] = r.json['data']['children']
    print "\nTop %s stories for %s\n" %(len(r.json['data']['children']), colorize(subreddit, "blue"))  

    for index, x in enumerate(r.json["data"]["children"]):
        data = x['data']
        index = str(index+1)

        if data['selftext'] != "":
            print colorize("[%s] " %index, "green"), "%s" % (data['title'].strip())
            
            story_data = "\nTitle: " + data['title'] + "\n\n" + data['selftext'] + "\n"
            stories[index] = story_data

        else:
            print "[%s]  %s" %(index, data['title'].strip())

    print "\n"

    return stories

color = ['gray', 'red', 'green', 'yellow', 'blue', 'magenta' ,'cyan', 'white', 'crimson']
colors = {}
for index, c in enumerate(color):
    colors[c] = index+30

def load_url(post, kind="comments"):
    if kind == "comments":
        url = 'http://www.reddit.com' + post['data'].get('permalink')
    elif kind == "post":
        url = post['data'].get('url')
    webbrowser.open_new_tab(url)

def colorize(text, color='white'):
    color = colors.get(color, 'white')
    return '\033[1;%sm%s\033[1;m' %(color, text)

if __name__ == "__main__":

    print "\nThe", colorize("reddit", "red"), "command line loader"
    print "Enter", colorize("exit", "red"), "to quit"
    print "Enter a ", colorize("subreddit", "blue"), "to load a specific subreddit"
    print "Enter blank to reload"
    print "Enter '10c' to see the comments for the tenth post (any numbers will do)"
    print "Enter multiple values to load multiple posts in new tabs"

    stories = print_top()
    subreddit = "all"

    digits = [str(x) for x in range(100)]

    question = "Which " + colorize("self post", "green") + " would you like to view? > "

    while True:

        st = raw_input(question)
        
        if st == 'exit':
            print "Goodbye!"
            exit()

        if " " in st:
            sts = st.strip().split(" ")
            for st in sts:
                load_url(stories['data'][int(st)-1], kind="post")


        elif len(st) == 0:
            subreddit = st.strip("/r/") if st != "" else subreddit
            stories = print_top(subreddit)

        elif st[-1] == 'c':
            if st[0:-1] in digits:
                prev = st[0:-1]
                print ""
                load_url(stories['data'][int(prev)-1], kind="comments")

            elif len(st) > 1:
                subreddit = st.strip("/r/") if st != "" else subreddit

            time.sleep(0.5)
            stories = print_top(subreddit)

        elif len(st) > 2:
            subreddit = st.strip("/r/") if st != "" else subreddit
            stories = print_top(subreddit)

        elif st[0] in digits if len(st) < 2 else st[0:2]:
            if stories.get(st):
                prev = st
            data = stories.get(st, None)
            if data == None:
                load_url(stories['data'][int(st)-1], kind="post")
                time.sleep(0.5)
                stories = print_top(subreddit)
            else:
                print stories.get(st)
        time.sleep(0.5)