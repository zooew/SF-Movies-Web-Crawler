import urllib2
content = urllib2.urlopen('http://www.boxofficemojo.com/genres/chart/?id=scifiadventure.htm').read()
hfile = open("test.html","w")
hfile.write(content)
hfile.close()
def single_film_info(single_film_url):
    film_info = ""
    return film_info
def single_year_info(year):
    