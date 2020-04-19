import FenestrationProject_Backend
from FenestrationProject_Backend import *

while True:
    MenuProjectSelect()
    option = EnterOption()
    if option == "1":
        projectName = input("Project name: ")
        FDataBase = FenestrationDataBase(projectName=projectName)

    elif option == "2":
        projectName = OpenProject()
        FDataBase = FenestrationDataBase(projectName=projectName)

    elif option == "3":
        FenestrationProject_Backend.DeleteProject()
        continue

    elif option == "0":
        Exit()

    else:
        print("\n*****PLEASE ENTER A VALID OPTION*****\n")
        continue

    while True:
        Menu()
        option = EnterOption()
        if option == "1":
            name = input("Name: ")
            name = name.upper()
            quantity, windowHeight, windowWidth = EnterQuantityHeightWidth(name)

            MenuComponentsOptions(name, quantity, windowHeight, windowWidth)

        elif option == "2":
            FDataBase.DeleteWindow()

        elif option == "3":
            FDataBase.EditWindow()

        # elif option == "4":
        # FDataBase.ShowProducts()

        elif option == "4":
            FDataBase.ShowWindowNamesAndQuantities()

        elif option == "5":
            FDataBase.ShowWindowNameAndComponents()

        elif option == "0":
            break

        else:
            print("\n*****PLEASE ENTER A VALID OPTION*****\n")
            continue
