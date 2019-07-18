import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import re
import pyperclip
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import requests
import json
import pprint
import csv
from klases import Threat_klass

# kintamieji
pp = pprint.PrettyPrinter(indent=0)
# Cloudo
agentid = 22922683  # input('Iveskite agento ID: ') pakeisti agentid arba ivesti
username = 'xx'  # Your username
password = 'xx'  # Your password
cloudurl = 'https://admin.cujo.io/'

# webdriver
driver = webdriver.Chrome()

# elastiko requestu
apiurl = "http://xx.xx.xx:9200/threats-*/_search?size=5000"
header = {
    'Content-Type': "application/json",
    'Accept': 'application/json',
}
custurl = "http://xx.xx.xx:11000/subscription/agent/"


# funkc
def elastic_q_threats(agentid):
    payload = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "agentId": agentid
                        }
                    },
                    {
                        "match": {
                            "blocking": "true"
                        }
                    }
                ]
            }
        }
    }

    rekvestas = requests.request("GET", apiurl, data=json.dumps(payload), headers=header)
    pranesimas = json.loads(rekvestas.text)

    return pranesimas


def getcustid(agentid):




    rekvestas = requests.get(custurl+agentid)
    rekvestas1 = rekvestas.text
    custid = json.loads(rekvestas1)



    return custid['customerId']


def lentelesElkiekis():
    lentele = driver.find_elements_by_tag_name('tr')
    x = len(lentele) - 1
    return x


def opencloud(url, username, password):
    driver.get(url)
    time.sleep(1)
    login(username, password)


def login(usr, passw):
    driver.find_element_by_name('username').send_keys(usr)  # login
    driver.find_element_by_name('password').send_keys(passw)  # login
    driver.find_element_by_class_name('pull-right').click()  # submit


def threat_filter(paieska):
    driver.get('https://admin.cujo.io/threat')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="threatsTable_filter"]/label/input').send_keys(paieska)


def getthreatip():
    elements = driver.find_elements_by_xpath('//*[@id="threatsTable"]')
    vieta = elements
    ip = []
    for element in elements:
        if re.match(
                pattern='\b(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\b',
                string=vieta):
            element = ip.append(elements)
        else:
            print('klaida nusiurbent ip getthreatip funcijoje 83eil')

    return element

    # ip = re.match(pattern='\b(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\b', string=vieta)
    # ipdata.append(ip)
    # print(vieta)


def getthreatid(list):
    threat_id_list = []
    list_a = list["hits"]
    list_b = list_a["hits"]

    for threat in list_b:

        threat_id_list.append(threat['_id'])
        threat_id_list.append(threat['_source']['detailedDescription'])
    return threat_id_list


def getthreatdisc(id):
    pass


def main():
    # nusiurbiam threatus is elastik
    threatu_list = elastic_q_threats(agentid)

    id_list = getthreatid(threatu_list)
    pp.pprint(id_list)

    # suskaiciuojam kiek threatu lsite
    threat_kiekis = len(id_list)/2
    print(threat_kiekis)

    # atidarom cloud
    #opencloud(cloudurl, username, password)
    # Buildinam lentele




    time.sleep(5)


if __name__ == '__main__':
    main()




