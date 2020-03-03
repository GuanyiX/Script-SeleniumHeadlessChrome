###############################################################
# Derrick Xiao (2019)
# The purpose of the repository is to collect the input stream
# from a website called TVM. An API called Selenium and the
# headless driver are utilized to automatically visit the
# website, click the play button and obtain one live stream.
# After successfully collecting the stream, it facilitates to
# save the stream in a .txt file for further utilizations.
###############################################################

from browsermobproxy import Server

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time



def stream_collector():

    server = Server("/root/xhprof/browsermob-proxy-2.1.4/bin/browsermob-proxy")
    server.start()
    proxy = server.create_proxy()
    chrome_options = Options()

    # Avoid the bug "DevToolActivePort file doesn't exist"
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Use headless browser to implement web automation
    chrome_options.add_argument('--headless')

    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))

    # Turn on the chrome driver
    chrome_driver = "/usr/bin/chromedriver"

    driver = webdriver.Chrome(executable_path = chrome_driver, chrome_options=chrome_options)

    # Provide the url of the target website
    # The link is found in the source code of the website and it is embedded in a static page
    base_url = "https://media.tvm.com.mt/16958960.ihtml/player.html?source=embed&live_id=16966825&tvm_location=tvm1_live"
    proxy.new_har("tvm.com.mt/mt/live", options={'captureHeaders': True, 'captureContent': True})
    driver.get(base_url)
    print("Connecting to the website(TVM)...")


    try:
        # Locate the corresponding element of the button and click it.
        # In this case, we would like to implement the automation because no visible browser is available.
        # Hence, this section faciliates to click the play button in order to obtain the live streams.
        driver.find_element_by_xpath("//*[@class='big-play-button']").click()
        time.sleep(5)
        print("Click the button!")
        time.sleep(5)
        result = proxy.har

        for entry in result['log']['entries']:
            _url = entry['request']['url']
            # Filter the urls based on three key elements, "m3u8" , "chunklist" and "b2"
            # because we aim to find the stream which is in high quality.
            if "m3u8" in _url and "chunklist" in _url:
                print("Congrats! The live stream is shown in the following!")
                print(_url)
                # Save the stream
                save_stream(_url)
                # Once obtaining the target url, stop the server and quit the driver.
                server.stop()
                driver.quit()
                break

    except:
        # Some errors happened and it takes too much time
        print("Sorry, it's not working!")

    server.stop()
    driver.quit()


def save_stream(collected_stream):
    # Every update will cover the previous content.
    f = open('/root/streams/TVM1LiveStream.txt','w')
    f.write(collected_stream)
    f.close()
    print("Saved successfully!")




if __name__ == "__main__" :

    # Collect the live streams
    stream_collector()
