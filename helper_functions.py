from bs4 import BeautifulSoup
import csv
import datetime as dt
from typing import Optional
from replit import db
import os
import requests
import time
import traceback

BASE_URL = "https://www.national.co.uk/tyres-search/"
website = "national.co.uk"
searchCriteria = ["205-55-16", "225-50-16", "185-16-14"]
headers = {
    "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}


def storeSearchCriteria(searchList: list[str]) -> None:
  """
  Stores list of search criteria strings in db.

  :param searchList: list of tyre search criteria
  :type searchList: list[str]

  :example:
  >>> storeSearchCriteria(["205-55-16", "225-50-16"])
  """
  db["searchCriteria"] = searchList


def clearConsole() -> None:
  os.system("clear")


def logError(log: str, error: Exception) -> None:
  """
  Logs errors to log.txt and outputs to console.
  
  :param log: log message to write to file
  :type log: str
  :param error: exception object that occurred
  :type error: Exception
  """

  print(
      f"An error occurred: {type(error).__name__}: {str(error)}, {traceback.format_exc()}"
  )
  try:
    with open("log.txt", "a") as f:
      f.write(log + "\n")
  except Exception as e:
    print(f"An error occurred logging an error: {type(e).__name__}: {str(e)}")


def mainMenu() -> str:
  """
  Returns main menu string to get search type.

  :returns: menu string with options
  :rtype: str
  """
  clearConsole()
  return """Automatic or manual tyre inputs?
  
  1. Automatic
  2. Manual
  3. Exit
  """


def saveMenu() -> Optional[bool]:
  """
  Returns save menu string to save CSV or not.

  :returns option: Y/N
  :rtype option: bool 
  """
  option = input("Would you like to save data to CSV? (Y/N): ")
  if option[0].lower() == "y":
    return True
  elif option[0].lower() == "n":
    return False
  else:
    clearConsole()
    saveMenu()


def getManualSearchInputs() -> str:
  """
  Prompts user to enter tyre information. Returns formatted str to concatenate to BASE_URL if valid.

  :returns: formatted search criteria with postcode
  :rtype: str 

  :example:
  >>> getManualSearchInputs()
  "205-55-16?pc=SW1A1AA"
  """

  clearConsole()
  print("Enter the following information: \n")
  width = input("Tyre width: ")
  profile = input("Tyre profile: ")
  size = input("Tyre size: ")
  return f"{width}-{profile}-{size}"


def tyreInputsAreValid(value: str) -> bool:
  """
  Checks if manual inputs are valid.

  :param value: tyre info string
  :type value: str

  :example:
  >>> inputIsValid("225-55-16")
  True

  """
  return True if value.replace("-", "").isdigit() else False


def scrapeData(tyreInfo: str, postcode: str) -> bool:
  """
  Main function to scrape tyre data for given criteria.

  :param tyreInfo: Tyre search criteria
  :type tyreInfo: str
  :param postcode: postcode
  :type postcode: str
  
  """
  print(f"REQUESTING DATA FOR {tyreInfo}...")
  productPage = getTyreData(tyreInfo, postcode)

  if not productPage:
    print("No data received from the server.")
    return False

  products = parseHTML(productPage)
  if not products:
    print("0 products found.")
    time.sleep(3)
    return False

  if products:
    print(f"{len(products)} product(s) found.")

    for i, product in enumerate(products):
      try:
        button = product.select_one("button")
        id = button.get("data-partcode") if button else f"{i+1}"
        site = website
        brand = isElement(product.select_one(".details img").get("alt"))
        pattern = isElement(
            product.select_one("div.tyreresult .details .pattern_link").text)
        size = isElement(
            product.select_one("div.details p:nth-child(3)").text.strip())
        season = ""
        price = isElement(product.select_one(".price strong").text.strip())
        dataList = [site, brand, pattern, size, season, price]
        updateDb(id, dataList, tyreInfo)
      except Exception as e:
        logError(f"{dt.datetime.today()}: error {e}", e)

  return True


def isElement(element: str) -> str:
  """
  Checks if element exists. Return element contents if true, "n/a" if false.

  :param element: html element, text or attribute
  :type tyreInfo: str
  :return: True or False:
  :rtype: bool

  :example:
  >>> isElement(product.select_one(".details img").get("alt"))
  "Avon Tyres"

  """
  return element if element else "n/a"


def getTyreData(tyreInfo: str, postcode: str) -> Optional[str]:
  """
  Requests data from webpage url (BASE_URL + tyreinfo). Returns html string.

  :param tyreInfo: string of tyre criteria 
  :type tyreInfo: str
  :returns: webpage html or None if request fails
  :rtype: Optional[str]

  :example:
  >>> getTyreData("205-55-16")
  "<html>...</html>"
  """
  url = BASE_URL + tyreInfo + "?pc=" + postcode
  try:
    response = requests.get(url, headers=headers)
    if response.ok:
      print("Request successful...")
      html = response.text
      return html
    else:
      error = f"{response.status_code}: {response.text}"
      logError(f"{dt.datetime.today()}: error {error}", Exception(error))
  except Exception as e:
    logError(f"{dt.datetime.today()}: error {e}", e)


def parseHTML(html: str) -> Optional[list]:
  """
  Parses html into list of div elements.

  :param html: html string
  :type html: str
  :returns: list of product elements or None if parsing fails
  :rtype: Optional[list]

  :example:
  >>> parseHTML("<html>...</html>")
  [<div class="tyreresult">...</div>, <div class="tyreresult">...</div>]
  """
  try:
    soup = BeautifulSoup(html, "html.parser")
    products = soup.find_all("div", {"class": "tyreresult"})
    return products
  except Exception as e:
    logError(f"{dt.datetime.today()}: error {e}", e)


def updateDb(id: str, dataList: list, tyreInfo: str) -> None:
  """
  Adds each new dataList to db. Key = id, Value = dataList.

  :param id: product id
  :type id: str
  :param dataList: tyre info
  :type dataList: list[str]
  :param tyreInfo: tyre width, profile and size
  :type tyreInfo: str

  :example:
  >>> updateDb("2055516GY02V", ["national", "Avon Tyres", "ZV7", "205/55R16", "", "£45.00"], "205-55-16")
  # Stores data in db["products"][tyreInfo][id] and db["tyres"][tyreInfo][id]
  
  """
  if tyreInfo not in db['products']:
    db['products'][tyreInfo] = {}

  try:
    db['products'][tyreInfo][id] = dataList
    print(f"{id}: {dataList} added to db.")
  except Exception as e:
    logError(f"{dt.datetime.today()}: error {e}", e)


def exportToCSV(tyreInfo: str = "") -> None:
  """
  Calls writeCSV() function depending on automatic or manual selection. Asks for and passes filename.

  :param tyreInfo: tyre search criteria
  :type tyreInfo: str
  """
  clearConsole()
  filename = input("Enter file name: ")
  if tyreInfo:
    writeCSV(tyreInfo, filename)
  else:
    for i, key in enumerate(db['products'].keys()):
      writeCSV(key, filename, i)


def writeCSV(tyreInfo: str, filename: str, i: int = 0) -> None:
  """
  Exports tyre product data to CSV from db with product ID as first column followed by product details.

  :param tyreInfo: tyre search criteria used as database key
  :type tyreInfo: str
  :param filename: userdefined file name
  :type filename: str
  :param tyreInfo: iterator limits writing headings to csv to one occurence.
  :type tyreInfo: int

  :example:
  >>> writeCSV("250-55-16", tyre_data, 0) 
  
  """
  try:
    products = db['products'][tyreInfo]
    headings = [
        "id", "site", "brand", "pattern", "size", "season", "price per tyre"
    ]
    with open(f"{filename}.csv", 'a', newline='') as f:
      writer = csv.writer(f)
      if i == 0:
        writer.writerow(headings)
      for k, v in products.items():
        writer.writerow([k] + list(v))
      print(f"Data exported to {filename}.csv for {tyreInfo}")
      time.sleep(2)
      clearConsole()
  except KeyError as e:
    print(f"No data found for {tyreInfo}")
    logError(
        f"{dt.datetime.today()}: error exporting CSV - key not found: {e}", e)
  except Exception as e:
    logError(f"{dt.datetime.today()}: error exporting CSV: {e}", e)
