# Importing necessary libraries.
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
# Import a necessary library to handle specific exceptions to deal with phones but we used another method.
# from selenium.common.exceptions import NoSuchElementException

# رابط البحث في خرائط جوجل
link = f"https://www.google.com/maps/search/%D8%B5%D9%8A%D8%AF%D9%84%D9%8A%D8%A7%D8%AA+%D9%85%D8%AD%D8%A7%D9%81%D8%B8%D8%A9+%D8%A7%D9%84%D8%B3%D9%88%D9%8A%D8%B3%E2%80%AD%E2%80%AD%E2%80%AD%E2%80%AD/@29.9943795,32.5510241,13z?hl=en&entry=ttu"
# The main Try block
try:
    # Create a new browser session using Chrome.
    driver = webdriver.Chrome()
    driver.get(link)  # Open the link.
    time.sleep(4)  # Waiting for the browser to load.

    # Find the scrollable part in the list of elements we want to find.
    scrollable_div = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")

    # Scroll down into the list of items and store the scroll height.
    last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)

    while True:
        # Finding all the items on the list.
        containers = driver.find_elements(By.CLASS_NAME, "Nv2PK")
        if containers:
            # Storing the number of items into a variable.
            num_items = len(containers)
            
            # Scroll down to the last visible item.
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            
            # Waiting for loading more data.
            time.sleep(3)
            
            # Checking if there are more items to load.
            new_containers = driver.find_elements(By.CLASS_NAME, "Nv2PK")
            if len(new_containers) == num_items:
                break
        else:
            break

        # Updating the list height.
        new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
        if new_height == last_height:
            break
        last_height = new_height

    time.sleep(2)

    # Extract the data and store it in lists.
    name_list = []
    starslist = []
    locationlist = []
    phonelist = []
    # Finding the container of the desired data and storing it as a variable (container).
    containers = driver.find_elements(By.CLASS_NAME, "Nv2PK")

    # Loop through the container list to find the desired elements and store them in lists.
    for container in containers:
        try:
            # Finding the name element.
            name = container.find_element(By.CSS_SELECTOR, "a.hfpxzc").get_attribute("aria-label")
            # Removing unnecessary characters from the name.
            if "," in name:
                name = name.replace("،", "")
            if "," in name:
                name = name.replace(",", "")
            if "·" in name:
                name = name.replace("·", "")
            # Storing the data of the names in a list.
            name_list.append(name)

        # Handling the exception if the name element is not found.
        except AttributeError:
            name_list.append("not found")
        except Exception as er:
            print(f"Error: {type(er)}: {er}")
            name_list.append("not found")

        try:
            # Finding the stars element.
            stars = container.find_element(By.CLASS_NAME, "bfdHYd ").find_element(By.CLASS_NAME, "lI9IFe ").find_element(By.CLASS_NAME, "ZkP5Je").get_attribute("aria-label")
            if "," in stars:
                stars = stars.replace(",", "")
            if "،" in stars:
                stars = stars.replace("،", "")
            # Storing the data of the stars in a list.
            starslist.append(stars)
        # Handling the exception if the stars element is not found.
        except AttributeError:
            starslist.append("not rated")
        except Exception as er:
            print(f"Error: {type(er)}: {er}")
            starslist.append("not rated")

        try:
            # Finding the location element.
            location = container.find_element(By.CLASS_NAME, "bfdHYd ").find_element(By.CLASS_NAME, "lI9IFe ").find_elements(By.CLASS_NAME, "W4Efsd")[1].find_element(By.CLASS_NAME, "W4Efsd").text.strip()     
            # Removing unnecessary characters from the location.
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
            # Storing the data of the location in a list.
            locationlist.append(location)
        # Handling the exception if the location element is not found.
        except AttributeError:
            locationlist.append("not found")
        except Exception as er:
            print(f"Error: {type(er)}: {er}")
            locationlist.append("not found")

        try:
            # Finding the phone element.
            phone_element = container.find_element(By.CLASS_NAME, "UsdlK").text.strip()
            if "," in phone_element:
                phone_element = phone_element.replace("،", "")
            # Storing the data of the phone in a list.
            phonelist.append(phone_element)
        # Handling the exception if the phone element is not found.
        except AttributeError:
            phonelist.append("not found")
        except Exception as er:
            print(f"Error: {type(er)}: {er}")
            phonelist.append("not found")

        # You can instead try this method to find the phone number but it is not worthy.
        # ==============================================================================================================================================================================================
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
        # ==============================================================================================================================================================================================
    # checking the data.
    print(name_list)
    print(starslist)
    print(locationlist)
    print(phonelist)
    # Waiting before closing the browser to avoid an IP ban.
    time.sleep(10)

finally:
    # Close the browser.
    driver.quit()  

# Writing and storing data in a CSV file.
with open('data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Stars', 'Location', 'Phone'])
    writer.writerows(zip(name_list, starslist, locationlist, phonelist))

    # Another method to writing and store data in a CSV file
    # ==============================================================================
    # with open('data.csv', 'w', newline='', encoding='utf-8') as file:
    # writer = csv.writer(file)
    # writer.writerow(['Name', 'Stars', 'Location', 'Phone'])
    # for x in range(len(name_list)):
    #     writer.writerow(name_list[x], starslist[x], locationlist[x], phonelist[x])
    # ==============================================================================

# Writing and storing data in a text file.
file = open("data.txt", "w", encoding="utf-8")
file.write("Name, Stars, Location, Phone\n")
for x in range(len(name_list)):
    file.write(f"Name: {name_list[x]}\nStars: {starslist[x]}\nLocation: {locationlist[x]}\nPhone: {phonelist[x]}\n"+ '*'*70 +'\n')
file.close()

