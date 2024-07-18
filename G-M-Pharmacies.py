from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
from selenium.common.exceptions import NoSuchElementException


# رابط البحث في خرائط جوجل
link = f"https://www.google.com/maps/search/%D8%B5%D9%8A%D8%AF%D9%84%D9%8A%D8%A7%D8%AA+%D9%85%D8%AD%D8%A7%D9%81%D8%B8%D8%A9+%D8%A7%D9%84%D8%B3%D9%88%D9%8A%D8%B3%E2%80%AD%E2%80%AD%E2%80%AD%E2%80%AD/@29.9943795,32.5510241,13z?hl=en&entry=ttu"
try:
    # إنشاء جلسة متصفح جديدة باستخدام Chrome
    driver = webdriver.Chrome()
    driver.get(link)  # فتح الرابط
    time.sleep(3)  # انتظار تحميل الصفحة

    # العثور على العنصر الذي يحتوي على قائمة العناصر
    scrollable_div = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")

    # التمرير لأسفل داخل قائمة العناصر لتحميل كل البيانات
    SCROLL_PAUSE_TIME = 4
    last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)

    while True:
        # العثور على جميع العناصر الحالية داخل القائمة
        containers = driver.find_elements(By.CLASS_NAME, "Nv2PK")
        if containers:
            # حفظ عدد العناصر الحالية
            num_items = len(containers)
            
            # التمرير إلى العنصر الأخير
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            
            # انتظار حتى يتم تحميل المزيد من العناصر
            time.sleep(SCROLL_PAUSE_TIME)
            
            # التحقق من إذا تم تحميل المزيد من العناصر
            new_containers = driver.find_elements(By.CLASS_NAME, "Nv2PK")
            if len(new_containers) == num_items:
                break
        else:
            break

        # تحديث ارتفاع القائمة
        new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
        if new_height == last_height:
            break
        last_height = new_height

    time.sleep(2)

    # استخراج أسماء الصيدليات مباشرة باستخدام Selenium
    name_list = []
    starslist = []
    locationlist = []
    phonelist = []
    # البحث عن كل العناصر التي تحتوي على بيانات الصيدليات
    containers = driver.find_elements(By.CLASS_NAME, "Nv2PK")

    for container in containers:
        try:
            name = container.find_element(By.CSS_SELECTOR, "a.hfpxzc").get_attribute("aria-label")
            if "," in name:
                name = name.replace("،", "")
            if "," in name:
                name = name.replace(",", "")
            if "·" in name:
                name = name.replace("·", "")

            name_list.append(name)

        except AttributeError:
            name_list.append("not found")
        except Exception as er:
            print(f"Error: {type(er)}: {er}")
            name_list.append("not found")

        try:
            stars = container.find_element(By.CLASS_NAME, "bfdHYd ").find_element(By.CLASS_NAME, "lI9IFe ").find_element(By.CLASS_NAME, "ZkP5Je").get_attribute("aria-label")
            if "," in stars:
                stars = stars.replace(",", "")
            if "،" in stars:
                stars = stars.replace("،", "")

            starslist.append(stars)

        except AttributeError:
            starslist.append("not rated")
        except Exception as er:
            print(f"Error: {type(er)}: {er}")
            starslist.append("not rated")

        try:
            location = container.find_element(By.CLASS_NAME, "bfdHYd ").find_element(By.CLASS_NAME, "lI9IFe ").find_elements(By.CLASS_NAME, "W4Efsd")[1].find_element(By.CLASS_NAME, "W4Efsd").text.strip()     
            
            if "\uf54a" in location:
                location = location.replace("\uf54a", "")
            if "." in location:
                location = location.replace(".", "")
            if "·" in location:
                location = location.replace("·", "")
            if "،" in location:
                location = location.replace("،", "")
            if "," in location:
                location = location.replace(",", "")
            if "\ue934" in location:
                location = location.replace("\ue934", "")
            if "\u002E" in location:
                location = location.replace("\u002E", "")
            locationlist.append(location)

        except AttributeError:
            locationlist.append("not found")
        except Exception as er:
            print(f"Error: {type(er)}: {er}")
            locationlist.append("not found")
        try:
            phone_element = container.find_element(By.CLASS_NAME, "UsdlK").text.strip()
            if "," in phone_element:
                phone_element = phone_element.replace("،", "")

            phonelist.append(phone_element)

        except Exception as er:
            print(f"Error: {type(er)}: {er}")
            phonelist.append("not found")

        # try:
        #     container.click() 
        #     time.sleep(3)
        #     ph_scroll = driver.find_elements(By.XPATH, "//div[@class='m6QErb DxyBCb kA9KIf dS8AEf XiKgde ']")[0]
        #     driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", ph_scroll)
        #     time.sleep(4)
        #     phone_element = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[9]/div[6]/div[2]/div/div[2]/a').get_attribute("href")
        #     print(phone_element)
        #     phonelist.append(phone_element)
        # except NoSuchElementException:
        #     try:
        #         phone_element = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[9]/div[5]/div[2]/div/div[2]/a').get_attribute("href")
        #         phonelist.append(phone_element)
        #     except NoSuchElementException:
        #         try:
        #             phone_element = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[8]/div[5]/div[2]/div/div[2]/a').get_attribute("href")
        #             phonelist.append(phone_element)
        #         except NoSuchElementException:
        #             try:
        #                 phone_element = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[5]/div[2]/div/div[2]/a').get_attribute("href")
        #                 phonelist.append(phone_element)
        #             except NoSuchElementException:
        #                 phone_element = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[9]/div[4]/div[2]/div/div[2]/a').get_attribute("href")
        #                 phonelist.append(phone_element)
        #             except AttributeError:
        #                 print("AttributeError")
        #                 phonelist.append("not found")
        #             except Exception as er:
        #                 print(f"Error: {type(er)}: {er}")
        #                 phonelist.append("not found")

    print(name_list)
    print(starslist)
    print(locationlist)
    print(phonelist)
    time.sleep(10)
finally:
    driver.quit()  # إغلاق المتصفح
with open('data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Stars', 'Location', 'Phone'])
    writer.writerows(zip(name_list, starslist, locationlist, phonelist))
    
    # writer.writerow(['Name', 'Stars', 'Location', 'Phone'])
    # for x in range(len(name_list)):
    #     writer.writerow(name_list[x], starslist[x], locationlist[x], phonelist[x])
    
file = open("data.txt", "w", encoding="utf-8")
file.write("Name, Stars, Location, Phone\n")
for x in range(len(name_list)):
    file.write(f"Name: {name_list[x]}\nStars: {starslist[x]}\nLocation: {locationlist[x]}\nPhone: {phonelist[x]}\n"+ '*'*70 +'\n')
file.close()