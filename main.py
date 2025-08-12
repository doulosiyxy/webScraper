import helper_functions as fc
from replit import db
import time


def main() -> None:
  """
  Calls functions and contains program flow.
  
  Displays main menu and handles user input for automatic or manual tyre search.
  """
  print(fc.mainMenu())
  mainMenuOption = input("Select 1, 2 or 3: ")
  while True:
    if mainMenuOption == "1":
      postcode = input("\nEnter your postcode: ").replace(" ", "")
      for tyreInfo in db["searchCriteria"]:
        fc.scrapeData(tyreInfo, postcode)
      fc.clearConsole()
      if fc.saveMenu():
        fc.exportToCSV()
      break
    elif mainMenuOption == "2":
      tyreInfo = fc.getManualSearchInputs()
      while not fc.tyreInputsAreValid(tyreInfo):
        tyreInfo = fc.getManualSearchInputs()
      postcode = input("Postcode: ").replace(" ", "")
      isSuccess = fc.scrapeData(tyreInfo, postcode)
      if isSuccess:
        time.sleep(2)
        fc.clearConsole()
        if fc.saveMenu():
          fc.exportToCSV(tyreInfo)
      else:
        pass
      break
    elif mainMenuOption == "3":
      exit()
    else:
      fc.clearConsole()
      print(fc.mainMenu())
      mainMenuOption = input("Select 1 or 2: ")


if __name__ == '__main__':
  while True:
    main()
