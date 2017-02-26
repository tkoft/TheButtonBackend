import urllib2

def req(url):
    print(urllib2.urlopen(url).read())

req("http://localhost:8080/")