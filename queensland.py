import urllib
url = 'https://data.qld.gov.au/api/action/datastore_search?limit=5&q=title:jones'
fileobj = urllib.urlopen(url)
print (fileobj.read())