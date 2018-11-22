from selenium import webdriver
import pickle
import time
import sys
import datetime

### script hosted at: https://github.com/susingha/toolx/blob/master/scripts/autochrome.py

### used on dev pc ###
wedriverurl = "C:/Users/Marlinspike/bin/chromedriver.exe"
norecsruntime = 50
waitdef = 3  # seconds

### used on deployment server ###
wedriverurl = "C:/Users/supratik/bin/chromedriver.exe"
norecsruntime = 1000
waitdef = 60 # seconds



print (sys.version)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
driver = webdriver.Chrome(wedriverurl)

driver.get('https://www.youtube.com')

print "Loading cookies"
for cookie in pickle.load(open("QuoraCookies.pkl", "rb")):
    driver.add_cookie(cookie)

driver.refresh()
print "Make sure browser is logged into desired account. If not, login manually using username and password"
x = raw_input("Press Enter to save cookies. x to exit: ")
if x == 'x' or x == 'X' or x == 'q' or x == 'Q':
    exit()

totaldest = 0
totalrecs = 0
norecs = 0
wait = waitdef

scrollpause = 3
scrollerjs = "document.body.scrollHeight || document.documentElement.scrollHeight"

while True:
    print "Current date and time:"
    print str(datetime.datetime.now())
    print
    print "About to remove more recommendations in", wait, "seconds"
    driver.refresh()
    time.sleep(wait)

    print "Saving cookies"
    pickle.dump(driver.get_cookies() , open("QuoraCookies.pkl","wb"))

    print "Scroll page to bottom"
    scroll = True
    lastheight = driver.execute_script("return " + scrollerjs)
    while scroll:
        driver.execute_script("window.scrollTo(0, " + scrollerjs + ")")
        time.sleep(scrollpause)

        newheight = driver.execute_script("return " + scrollerjs)
        if (newheight == lastheight):
            scroll = False
        lastheight = newheight

    print "Finding recommendations"
    destroyrec = driver.find_elements_by_xpath("//button[@id='button' and @class='style-scope yt-icon-button' and @aria-label='Not interested']")
    totalrecs = len(destroyrec)

    if totalrecs == 0:
        print "No recommendations found"
        norecs += 1
        wait += 5
        if norecs >= norecsruntime:
            break
    else:
        norecs = 0
        wait = waitdef

    print totaldest, " recommendations removed. Removing", totalrecs, "more."
    for i in xrange(totalrecs):
        destroyrec[i].click()
        totaldest += 1
        time.sleep(1)

driver.close()
print "Removed", totaldest, "recommendations"
print "Congarts, you have defeated Youtube and Google"
print
print "Current date and time:"
print str(datetime.datetime.now())