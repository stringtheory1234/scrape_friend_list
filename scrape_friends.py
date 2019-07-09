import http.cookiejar
import urllib.request
import requests
import bs4

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)
authentication_url = "https://m.facebook.com/login.php"

payload={
    'email':"your_email",
    'pass':"your_pass"
}

data = urllib.parse.urlencode(payload).encode('utf-8')
req = urllib.request.Request(authentication_url, data)
resp = urllib.request.urlopen(req)
contents = resp.read()
#print(contents)

def check(str):
    lists = ["add friend", "confirm", "delete request", "cancel request"]
    b = True
    if "public" in str:
        b=False
    for list1 in lists:
        if str==list1:
            b=False
    return b

def list_of_friends(url):
    data = requests.get(url, cookies=cj)
    soup = bs4.BeautifulSoup(data.text, 'lxml')
    z = 0
    p=0
    friends=[]
    while url:
        url=""
        z=0
        for i in soup.find_all('a'):
            if i.text.lower()=="see more friends":
                url = i.get('href')
                url = "https://m.facebook.com"+url
                data = requests.get(url, cookies=cj)
                soup = bs4.BeautifulSoup(data.text, 'lxml')
                break
            if i.text=="اردو" :
                break
            if p==0 and z>16 and check(i.text.lower()):
                friends.append(i.text)
            if p>0 and z>8 and check(i.text.lower()):
                friends.append(i.text)
            z=z+1
        p=1
    return friends

def print_list(list):
    for friend in list:
        print(friend)

friend1 = list_of_friends("profile_url/friends")
print(len(friend1))
print_list(friend1)


