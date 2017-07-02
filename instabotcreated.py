import requests, urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

APP_ACCESS_TOKEN = "2177183342.405fc93.c82eb79788b248f2bfe5792b9d04e685"
#HERE WE DEFINE THE APP ACCESS TOKEN.

BASE_URL = "https://api.instagram.com/v1/"


#DEFINING A FUNCTION TO GET THE INFO ABOUT THE TOKEN OWNER.


def self_info():
    request_url = (BASE_URL + "users/self/?access_token=%s") %(APP_ACCESS_TOKEN)
    print "GET request url : %s" %(request_url)
    user_info = requests.get(request_url).json()

    if user_info["meta"]["code"] == 200:
        if len(user_info["data"]):
            print "Username: %s" %(user_info['data']['username'])
            print "Your followers: %s" % (user_info["data"]["counts"]["followed_by"])
            print "Number of people followed by you: %s" % (user_info["data"]["counts"]["follows"])
            print "Total number of posts: %s" % (user_info["data"]["counts"]["media"])
        else:
            print "User does not exist!"
    else:
        print "Status code other than 200 received!"


#DEFINING A FUNCTION TO GET ID OF OTHER USER WITH THE HELP OF ITS USERNAME.


def get_user_id(insta_username):
    request_url = (BASE_URL + "users/search?q=%s&access_token=%s") %(insta_username, APP_ACCESS_TOKEN)
    print "GET request url : %s" %(request_url)
    user_info = requests.get(request_url).json()

    if user_info["meta"]["code"] == 200:
        if len(user_info["data"]):
            return user_info["data"][0]["id"]
        else:
            return None
    else:
        print "Status code other than 200 received!"
        exit()


#DEFINING A FUNCTION TO GET INFO ABOUT A USER USING ITS USERNAME.

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)

    if user_id == None:
        print "User does not exist!"
        exit()

    request_url = (BASE_URL + "users/%s?access_token=%s") %(user_id, APP_ACCESS_TOKEN)
    print "GET request url : %s" %(request_url)
    print user_id + " is the user ID."
    user_info = requests.get(request_url).json()

    if user_info["meta"]["code"] == 200:
        if len(user_info['data']):
            print "Username: %s" %(user_info["data"]["username"])
            print "Your followers: %s" %(user_info["data"]["counts"]["followed_by"])
            print "Number of people followed by you: %s" %(user_info["data"]["counts"]["follows"])
            print 'Total number of posts: %s' %(user_info["data"]["counts"]["media"])
        else:
            print "No data available."
    else:
        print "Status code other than 200 received!"


#DEFINING A FUNCTION TO GET THE LATEST POST OF THE TOKEN OWNER.


def get_own_post():
    request_url = (BASE_URL + "users/self/media/recent/?access_token=%s") % (APP_ACCESS_TOKEN)
    print "GET request url : %s" % (request_url)
    own_media = requests.get(request_url).json()

    if own_media["meta"]["code"] == 200:
        if len(own_media["data"]):
            image_name = own_media["data"][0]["id"] + ".jpeg"
            image_url = own_media["data"][0]["images"]["standard_resolution"]["url"]
            urllib.urlretrieve(image_url, image_name)
            print "Your image with post id " + own_media["data"][0]["id"] + " has been downloaded!"
        else:
            print "No posts.!"
    else:
        print "Status code other than 200 received!"


#DEFINING A FUCTION TO GET THE LATEST POST OF OTHER USER USING A USERNAME.


def get_user_post(insta_username):
    user_id = get_user_id(insta_username)

    if user_id == None:
        print "User does not exist!"
        exit()

    request_url = (BASE_URL + "users/%s/media/recent/?access_token=%s") %(user_id, APP_ACCESS_TOKEN)
    print "GET request url : %s" %(request_url)
    user_media = requests.get(request_url).json()

    if user_media["meta"]["code"] == 200:
        if len(user_media["data"]):
            image_name = user_media["data"][0]["id"] + '.jpeg'
            image_url = user_media["data"][0]["images"]["standard_resolution"]["url"]
            urllib.urlretrieve(image_url, image_name)
            print "Your image with id " + user_media["data"][0]["id"] + " has been downloaded!"
        else:
            print "Post does not exist!"
    else:
        print "Status code other than 200 received!"


#FUNCTION TO GET ID OF THE RECENT POST OF A USER.


def get_post_id(insta_username):
    user_id = get_user_id(insta_username)

    if user_id == None:
        print "User does not exist!"
        exit()

    request_url = (BASE_URL + "users/%s/media/recent/?access_token=%s") %(user_id, APP_ACCESS_TOKEN)
    print "GET request url : %s" %(request_url)
    user_media = requests.get(request_url).json()

    if user_media["meta"]["code"] == 200:
        if len(user_media["data"]):
            return user_media["data"][0]["id"]
        else:
            print "There is no recent post of the user!"
            exit()
    else:
        print "Status code other than 200 received!"
        exit()


#DEFINING A FUNCTION TO LIKE A LATEST POST OF A USER.


def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/likes") %(media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print "POST request url : %s" %(request_url)
    post_a_like = requests.post(request_url, payload).json()

    if post_a_like["meta"]["code"] == 200:
        print "Like was successful!"
    else:
        print "Your like was unsuccessful. Try again!"


#DEFINING A FUNCTION TO POST A COMMENT ON OTHER USER'S POST.


def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + "media/%s/comments") %(media_id)
    print "POST request url: %s" % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment["meta"]["code"] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


#DEFINING A FUNCTION TO VIEW THE LIST OF THE COMMENTS.


def view_comments(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/comments?access_token=%s") %(media_id, APP_ACCESS_TOKEN)
    print "GET request URL: %s" %(request_url)
    user_comments = requests.get(request_url).json()

    if user_comments["meta"]["code"] == 200:
        if len(user_comments["data"]):
            print user_comments["data"][1]["text"]
        else:
            print "There are no comments on the post!"
            exit()
    else:
        print "Status code other than 200 received!"
        exit()
#FUNCTION TO GET A LIST OF LIKES.

def liked_media():
    request_url = (BASE_URL + "v1/users/self/media/liked?access_token=%s") %(APP_ACCESS_TOKEN)
    print "GET request URL: %s" %(request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][2]['id']
            print image_name
        else:
            print "No media liked."
            exit()
    else:
        print "Status code other than 200 received!"
        exit()


def get_tag_info():
    request_url


def start_bot():
    while True:
        print '\n'
        print "INSTABOT SUCCESSFULLY EVOLVED"
        print "Select from the following MENU"
        print "a. Get your own details\n"
        print "b. Get details of a user by username\n"
        print "c. Get your own recent post\n"
        print "d. Get the recent post of a user by username\n"
        print "e. Like the recent post.\n"
        print "f. Comment on the recent post.\n"
        print "g. View recent comments. \n"
        print "h. Get the recently liked media. \n"
        print "i. Exit"

        choice = raw_input("Enter you choice: ")

        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice == "e":
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)
        elif choice == "f":
            insta_username = raw_input("Enter the username:")
            post_a_comment(insta_username)
        elif choice == "g":
            insta_username = raw_input("Enter the username: ")
            view_comments(insta_username)
        elif choice == "h":
            liked_media()
        elif choice == "i":
            exit()
        else:
            print " thats a wrong choice"

start_bot()