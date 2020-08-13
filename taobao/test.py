import json

from selenium import webdriver
import time

from selenium.webdriver.support.wait import WebDriverWait

options = webdriver.ChromeOptions()
# wd = webdriver.Chrome("/usr/local/bin/chromedriver")
options.add_argument(r'--user-data-dir=/usr/local/bin/chromedriver Data\Default')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(options=options)
driver.get('https://app.bupt.edu.cn/ncov/wap/default/index')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Referer': 'https://www.taobao.com/'}

main_driver = driver.current_window_handle


def request_page():
    driver.find_element_by_xpath('//*[@id="q"]').send_keys('手机')
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="J_TSearchForm"]/div[1]/button').click()
    time.sleep(3)
    i = 27
    #在这里换页码
    if i > 0:
        j = 1
        while(j<i):
            driver.find_element_by_xpath('//*[@class="item next"]').click()
            j+=1
            time.sleep(2)
    while i < 100:
        file = open('tbphone'+str(i)+'.json', "w", encoding="utf-8")
        all_thing_div = driver.find_element_by_xpath('//*[@id="mainsrp-itemlist"]/div/div/div[1]')
        all_goods = all_thing_div.find_elements_by_xpath('./div')
        for good in all_goods:
            try:
                good_info = good.find_element_by_css_selector('.ctx-box').find_elements_by_xpath('./div')
            except:
                pass

            price = good_info[0].find_element_by_xpath('./div[1]/strong').text
            salad = good_info[0].find_element_by_xpath('./div[@class="deal-cnt"]').text
            store = good_info[2].find_element_by_xpath('./div[1]/a').text

            good_info[1].find_element_by_xpath('./a').click()
            driver.switch_to.window(driver.window_handles[-1])
            js = "window.scrollTo(0,1000)"
            time.sleep(1)
            driver.execute_script(js)
            time.sleep(2)
            try:
                tag_standard = WebDriverWait(driver, 5, 0.2).until(
                    lambda x: x.find_element_by_xpath('//*[@id="J_TabBar"]/li[2]/a'))
            except:

                tag_standard = None

            if tag_standard:
                try:
                    tag_table = driver.find_element_by_xpath('//*[@id="J_AttrUL"]')
                    good_detail = tag_table.text
                    print('单价: ' + price + ' 购买数量: ' + salad + ' 商品详情: ' + good_detail + '店铺名称: ' + store)
                    item = {'单价': price, '购买数量': salad, '商品详情': good_detail, '店铺名称': store}
                    json_str = json.dumps(item, ensure_ascii=False) + "\n"
                    file.write(json_str)
                except:

                    pass
                print(good_info)
                driver.close()
                driver.switch_to.window(main_driver)

        print('第{}页爬取完成'.format(i))
        i+=1
        time.sleep(15)
        driver.find_element_by_xpath('//*[@class="item next"]').click()


if __name__ == '__main__':
    request_page()
    driver.close()


