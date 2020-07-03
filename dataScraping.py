from bs4 import BeautifulSoup
import requests
import re
import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def get_financial_statements(code):
    # Disable flag warning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    re_enc = re.compile("encparam: '(.*)'", re.IGNORECASE)
    re_id = re.compile("id: '([a-zA-Z0-9]*)' ?", re.IGNORECASE)

    url = "https://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd={}".format(code)
    html = requests.get(url, verify=False).text
    encparam = re_enc.search(html).group(1)
    encid = re_id.search(html).group(1)

    url = "https://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd={}&fin_typ=0&freq_typ=A&encparam={}&id={}".format(
        code, encparam, encid)
    headers = {"Referer": "HACK"}
    html = requests.get(url, headers=headers, verify=False).text

    soup = BeautifulSoup(html, "html5lib")
    dividend = soup.select("table:nth-of-type(2) tr:nth-of-type(33) td span")
    years = soup.select("table:nth-of-type(2) th")

    dividend_dict = {}
    for i in range(len(dividend)):
        dividend_dict[years[i + 3].text.strip()[:4]] = dividend[i].text

    return dividend_dict

def get_estimated_dividend_yield(code):
    dividend_yield = get_financial_statements(code)
    if len(dividend_yield) == 0:
        return "0"

    dividend_yield = sorted(dividend_yield.items())[-1]
    return dividend_yield[1]


def get_3year_treasury():
    # Disable flag warning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    url = "http://index.go.kr/strata/jsp/showStblGams3.jsp?stts_cd=107301&idx_cd=1073&freq=Y&period=1997:2019"
    html = requests.get(url, verify=False).text
    soup = BeautifulSoup(html, 'html5lib')
    td_data = soup.select("tr#tr_107301_1 td")

    treasury_3year = {}
    start_year = 1998

    for x in td_data:
        treasury_3year[start_year] = x.text
        start_year += 1

    return treasury_3year

def get_current_3year_treasury():
    # Disable flag warning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    url = "http://finance.naver.com/marketindex/interestDailyQuote.nhn?marketindexCd=IRR_GOVT03Y&page=1"
    html = requests.get(url, verify=False).text

    soup = BeautifulSoup(html, 'html5lib')
    td_data = soup.select("tr td")
    return td_data[1].text

def get_previous_dividend_yield(code):
    dividend_yield = get_financial_statements(code)

    now = datetime.datetime.now()
    cur_year = now.year

    previous_dividend_yield = {}

    for year in range(cur_year-5, cur_year):
        if str(year) in dividend_yield.keys():
            previous_dividend_yield[year] = dividend_yield[str(year)]

    return previous_dividend_yield

def get_dividend_yield(code):
    # Disable flag warning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    re_enc = re.compile("encparam: '(.*)'", re.IGNORECASE)
    re_id = re.compile("id: '([a-zA-Z0-9]*)' ?", re.IGNORECASE)

    url = "http://companyinfo.stock.naver.com/company/c1010001.aspx?cmp_cd=" + code
    html = requests.get(url, verify=False).text

    search = re_enc.search(html)
    if search is None:
        return {}

    encparam = re_enc.search(html).group(1)
    encid = re_id.search(html).group(1)

    soup = BeautifulSoup(html, 'html5lib')
    dt_data = soup.select("td dl dt")

    dividend_yield = dt_data[-2].text
    dividend_yield = dividend_yield.split(' ')[1]
    dividend_yield = dividend_yield[:-1]

    return dividend_yield


#if __name__ == "__main__":
    # dividend_dict = get_financial_statements("035720")
    # print(dividend_dict)
    # get_3year_treasury()
    # dividend_yield = get_dividend_yield('058470')
    # print(dividend_yield)
    # print(get_current_3year_treasury())
    # print(get_previous_dividend_yield('058470'))

