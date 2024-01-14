from requests_html import HTMLSession

url = "https://www.1mg.com/drugs/ivepred-4-tablet-13015"
# url = "https://python.org/"

s = HTMLSession()
r = s.get(url)
r.html.render(timeout=30)
print(r.status_code)
print(type(r))
print(r.html.raw_html)
with open("from_request_html.html", "wb") as outFile:
    outFile.write(r.html.raw_html)
