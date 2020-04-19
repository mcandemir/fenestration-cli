import sqlite3
from Imperial_Decimal import imp2dec, dec2imp


# ======================================================================================================================


class Fenestration:
    # ------------------------------------------------------------------------------------------------------------------

    # Initializing properties/fields
    def __init__(self, Name, Component, ComponentQuantity, Length, WindowQuantity, WindowHeight, WindowWidth):
        self.Name = Name
        self.Component = Component
        self.ComponentQuantity = ComponentQuantity
        self.Length = Length
        self.WindowQuantity = WindowQuantity
        self.WindowHeight = WindowHeight
        self.WindowWidth = WindowWidth

    # ------------------------------------------------------------------------------------------------------------------


# ======================================================================================================================

class FenestrationDataBase:
    # ------------------------------------------------------------------------------------------------------------------

    # Initializing database
    def __init__(self, projectName):
        self.projectName = projectName
        self.connection = sqlite3.connect("FenestrationDataBase.db")
        self.cursor = self.connection.cursor()
        self.CreateConnection()

        global current_project_name  # Made a special global variable to use outside of the class
        current_project_name = self.projectName

    # ------------------------------------------------------------------------------------------------------------------

    # Create connection with the database
    def CreateConnection(self):

        query = "CREATE TABLE IF NOT EXISTS " + self.projectName + "(Name TEXT, Components TEXT, ComponentQuantity TEXT, " \
                                                                   "Length FLOAT, WindowQuantity INT, WindowHeight FLOAT, WindowWidth FLOAT) "

        self.cursor.execute(query)
        self.connection.commit()

    # ------------------------------------------------------------------------------------------------------------------

    # Adding new products
    def AddWindow(self, fenestration):
        query = "INSERT INTO " + self.projectName + " VALUES(?,?,?,?,?,?,?)"

        self.cursor.execute(query, (
            fenestration.Name, fenestration.Component, fenestration.ComponentQuantity, fenestration.Length,
            fenestration.WindowQuantity, fenestration.WindowHeight, fenestration.WindowWidth))
        self.connection.commit()

    # ------------------------------------------------------------------------------------------------------------------

    # Editing windows in general
    def EditWindow(self):

        # Phase 1: List window names and user will choose one
        while True:
            # Creating a query
            query = "SELECT Name FROM " + self.projectName + " GROUP BY Name ORDER BY Name"

            self.cursor.execute(query)
            products = self.cursor.fetchall()

            # Creating a dictionary
            windowDict = dict()
            windowDict.update({"0": "Back"})

            # Print the list of existing window list and use it as a menu by using dictionary
            print("\n\t\t\tWINDOWS\n\t\t\t========================================")
            count = 1
            for name in products:
                print("\t\t\t{} - {}".format(count, name[0]))
                windowDict.update({str(count): name[0]})
                count += 1
            print("\t\t\t0 - Back")

            # The program will check if the option is valid, and acts by it
            option = input()

            if option in windowDict.keys():
                windowEdit = windowDict[option]
            else:
                print("\n\t\t\t*****PLEASE ENTER A VALID OPTION*****\n")
                continue

            if windowEdit == "Back":
                break

            self.EditCompOrWin(windowEdit)

    # ------------------------------------------------------------------------------------------------------------------

    # Phase 2: After user chooses a window, there will be a selection for editing windows or components
    def EditCompOrWin(self, windowEdit):
        while True:

            # Choose a valid event that given in the menu
            MenuEditCompOrWin()
            option = input()

            if option == "1":
                self.EditWindowAttribute(windowEdit)

            elif option == "2":
                self.EditComponent(windowEdit)

            elif option == "0":
                break

            else:
                print("\n\t\t\t*****PLEASE ENTER A VALID OPTION*****\n")
                continue

    # ------------------------------------------------------------------------------------------------------------------

    # Phase a.1: Editing attributes of window
    def EditWindowAttribute(self, windowEdit):
        while True:
            # Choose a valid event that given in the menu
            MenuEditWindowAttribute()
            option = input()

            # Rename window
            if option == "1":
                query = "UPDATE " + self.projectName + " SET Name = ? WHERE Name = ?"

                windowEditNewName = input("\n\t\t\tNew name: ")

                windowEditNewName = windowEditNewName.upper()

                self.cursor.execute(query, (windowEditNewName, windowEdit))
                self.connection.commit()

                print("\n\t\t\t***NAME UPDATED SUCCESSFULLY: {}***".format(windowEditNewName))

            # Edit window quantity
            elif option == "2":
                query = "UPDATE " + self.projectName + " SET WindowQuantity = ? WHERE Name = ?"

                windowEditNewQuantity = int(input("\n\t\t\tNew quantity: "))

                self.cursor.execute(query, (windowEditNewQuantity, windowEdit))
                self.connection.commit()

                print("\n\t\t\t***QUANTITY UPDATED SUCCESSFULLY: {}***".format(windowEditNewQuantity))

            # Edit window height
            elif option == "3":
                query = "UPDATE " + self.projectName + " SET WindowHeight = ? WHERE Name = ?"

                windowEditNewHeight = input("\n\t\t\tNew height: ")

                self.cursor.execute(query, (imp2dec(windowEditNewHeight), windowEdit))
                self.connection.commit()

                print("\n\t\t\t***HEIGHT UPDATED SUCCESSFULLY: {}***".format(windowEditNewHeight))

            # Edit window width
            elif option == "4":
                query = "UPDATE " + self.projectName + " SET WindowWidth = ? WHERE Name = ?"

                windowEditNewWidth = input("\n\t\t\tNew width: ")

                self.cursor.execute(query, (imp2dec(windowEditNewWidth), windowEdit))
                self.connection.commit()

                print("\n\t\t\t***WIDTH UPDATED SUCCESSFULLY: {}***".format(windowEditNewWidth))

            # Back
            elif option == "0":
                break

            # Invalid option
            else:
                print("\n\t\t\t*****PLEASE ENTER A VALID OPTION*****\n")
                continue

    # ------------------------------------------------------------------------------------------------------------------

    # Phase b.1: Basic component events
    def EditComponent(self, windowEdit):
        while True:

            # Choose a valid event that given in the menu
            MenuEditComponent()
            option = input()

            # Add component
            if option == "1":
                self.AddComponent(windowEdit)

            # Delete component
            elif option == "2":
                self.DeleteComponent(windowEdit)

            # Edit component attributes
            elif option == "3":
                self.EditComponentAttribute(windowEdit)

            # Back
            elif option == "0":
                break

            # Invalid option
            else:
                print("\n\t\t\t*****PLEASE ENTER A VALID OPTION*****\n")
                continue

    # ------------------------------------------------------------------------------------------------------------------

    # Adding new components here
    def AddComponent(self, windowEdit):

        # Declare some global variable to use them in outer scope
        # And create a query to pull attributes of the window that component belongs to
        global windowQuantity, windowHeight, windowWidth
        query = "SELECT Name, WindowQuantity, WindowHeight, WindowWidth FROM " + self.projectName + " WHERE Name = ? GROUP BY Name"

        product = self.cursor.execute(query, (windowEdit,))

        for name, quantity, height, width in product:
            windowQuantity = quantity
            windowHeight = height
            windowWidth = width

        # Send the attributes to commissioned function to create a new component
        self.MenuAddComponents(windowEdit, windowQuantity, windowHeight, windowWidth)

    # ------------------------------------------------------------------------------------------------------------------

    # This is for adding a new component
    def MenuAddComponents(self, windowEdit, window_quantity, window_height, window_width):

        while True:
            MenuComponents()
            option = EnterOption()
            # HEAD
            if option == "1":
                print("\t\t\tHEAD")

                for i in range(EnterQuantityOfTypes()):
                    component = self.GetValidComponentID(windowEdit, "Head")
                    component_quantity = self.EnterQuantityOfComponent_comp_edit(component)
                    length = self.EnterLength_comp_edit(component)
                    SaveComponents(windowEdit, "{}".format(component), component_quantity, length, window_quantity,
                                   window_height, window_width)

            # SILL
            elif option == "2":
                print("\t\t\tSILL")

                for i in range(EnterQuantityOfTypes()):
                    component = self.GetValidComponentID(windowEdit, "Sill")
                    component_quantity = self.EnterQuantityOfComponent_comp_edit(component)
                    length = self.EnterLength_comp_edit(component)
                    SaveComponents(windowEdit, "{}".format(component), component_quantity, length, window_quantity,
                                   window_height, window_width)

            # JAMB
            elif option == "3":
                print("\t\t\tJAMB")

                for i in range(EnterQuantityOfTypes()):
                    component = self.GetValidComponentID(windowEdit, "Jamb")
                    component_quantity = self.EnterQuantityOfComponent_comp_edit(component)
                    length = self.EnterLength_comp_edit(component)
                    SaveComponents(windowEdit, "{}".format(component), component_quantity, length, window_quantity,
                                   window_height, window_width)

            # JAMB
            elif option == "4":
                print("\t\t\tDOOR JAMB")

                for i in range(EnterQuantityOfTypes()):
                    component = self.GetValidComponentID(windowEdit, "D.J.")
                    component_quantity = self.EnterQuantityOfComponent_comp_edit(component)
                    length = self.EnterLength_comp_edit(component)
                    SaveComponents(windowEdit, "{}".format(component), component_quantity, length, window_quantity,
                                   window_height, window_width)

            # H MULLION
            elif option == "5":
                print("\t\t\tH. MULLION")

                for i in range(EnterQuantityOfTypes()):
                    component = self.GetValidComponentID(windowEdit, "H.M.")
                    component_quantity = self.EnterQuantityOfComponent_comp_edit(component)
                    length = self.EnterLength_comp_edit(component)
                    SaveComponents(windowEdit, "{}".format(component), component_quantity, length, window_quantity,
                                   window_height, window_width)

            # V MULLION
            elif option == "6":
                print("\t\t\tV. MULLION")

                for i in range(EnterQuantityOfTypes()):
                    component = self.GetValidComponentID(windowEdit, "V.M.")
                    component_quantity = self.EnterQuantityOfComponent_comp_edit(component)
                    length = self.EnterLength_comp_edit(component)
                    SaveComponents(windowEdit, "{}".format(component), component_quantity, length, window_quantity,
                                   window_height, window_width)

            # DOORHEAD
            elif option == "7":
                print("\t\t\tDOOR HEAD")

                for i in range(EnterQuantityOfTypes()):
                    component = self.GetValidComponentID(windowEdit, "D.H.")
                    component_quantity = self.EnterQuantityOfComponent_comp_edit(component)
                    length = self.EnterLength_comp_edit(component)
                    SaveComponents(windowEdit, "{}".format(component), component_quantity, length, window_quantity,
                                   window_height, window_width)

            # RETURN
            elif option == "0":
                break

            else:
                print("\n\t\t\t*****PLEASE ENTER A VALID OPTION*****\n")
                continue

            print("\n\t\t\t*****Component added successfully\n\n")

    # ------------------------------------------------------------------------------------------------------------------

    # This function is for adding components
    @staticmethod
    def EnterLength_comp_edit(component):
        while True:
            try:
                length = input("Length of {}(x'-y\"): ".format(component))
                length = imp2dec(length)
            except ValueError:
                print("\n\t\t\t*****PLEASE ENTER A VALID VALUE*****\n")
                continue
            else:
                return length

    # ------------------------------------------------------------------------------------------------------------------

    # This function is for adding components
    @staticmethod
    def EnterQuantityOfComponent_comp_edit(component):
        while True:
            try:
                quantity = int(input("How many {}: ".format(component)))
            except ValueError:
                print("\n\t\t\t*****PLEASE ENTER A VALID VALUE*****\n")
                continue
            else:
                return quantity

    # ------------------------------------------------------------------------------------------------------------------

    # Deleting components specified by name and component name
    def DeleteComponent(self, windowEdit):
        while True:

            # Creating a query
            query = "SELECT Components FROM " + self.projectName + " WHERE Name = ? ORDER BY Components"

            self.cursor.execute(query, (windowEdit,))
            products = self.cursor.fetchall()

            # Creating a dictionary for choosing by numbers
            componentDict = dict()
            componentDict.update({"0": "Back"})

            # Print the list of existing component list and use it as a menu by using dictionary
            print("\t\t\t\t\t\tDELETE COMPONENTS\n\t\t\t\t\t\t========================================")
            count = 1
            for component in products:
                print("\t\t\t\t\t\t{} - {}".format(count, component[0]))
                componentDict.update({str(count): component[0]})
                count += 1
            print("\t\t\t\t\t\t0 - Back")

            # The program will check if the option is valid, and acts by it
            option = input()

            if option in componentDict.keys():
                componentDelete = componentDict[option]

            else:
                print("\n\t\t\t\t\t\t*****PLEASE ENTER A VALID OPTION*****\n")
                continue

            if componentDelete == "Back":
                break

            # Creating a query to delete the specified component
            query = "DELETE FROM " + self.projectName + " WHERE Name = ? AND Components = ?"

            self.cursor.execute(query, (windowEdit, componentDelete))
            self.connection.commit()

            print("\n\t\t\t\t\t\t***COMPONENT DELETED SUCCESSFULLY: {}***".format(componentDelete))

    # ------------------------------------------------------------------------------------------------------------------

    # Phase b.2: List the window's components and choose one to edit
    def EditComponentAttribute(self, windowEdit):

        # Create a global variable to use it in outer scope
        global componentEdit
        while True:

            # Create a query to pull components from database
            query = "SELECT Components FROM " + self.projectName + " WHERE Name = ? ORDER BY Components"

            self.cursor.execute(query, (windowEdit,))
            products = self.cursor.fetchall()

            # Create a dictionary
            componentDict = dict()
            componentDict.update({"0": "Back"})

            # Print the list of existing component list and use it as a menu by using dictionary
            print("\t\t\t\t\t\tCOMPONENTS\n\t\t\t\t\t\t========================================")
            count = 1
            for component in products:
                print("\t\t\t\t\t\t{} - {}".format(count, component[0]))
                componentDict.update({str(count): component[0]})
                count += 1
            print("\t\t\t\t\t\t0 - Back")

            # Choose a valid event
            option = input()

            if option in componentDict.keys():
                componentEdit = componentDict[option]

            else:
                print("\n\t\t\t\t\t\t*****PLEASE ENTER A VALID OPTION*****\n")
                continue

            if componentEdit == "Back":
                break

            self.EditComponentAttributeOptions(windowEdit, componentEdit)

    # ------------------------------------------------------------------------------------------------------------------

    # Phase b.3: Edit
    def EditComponentAttributeOptions(self, windowEdit, component_edit):
        # Component attributes edit options
        while True:

            # Choose a valid event that given in the menu
            MenuEditComponentAttribute()
            option = input()

            # Rename component
            if option == "1":
                self.EditComponentAttributeRename(windowEdit, component_edit)

            # Edit component quantity
            elif option == "2":
                self.EditComponentAttributeQuantity(windowEdit, component_edit)

            # Edit component length
            elif option == "3":
                self.EditComponentAttributeLength(windowEdit, component_edit)

            # Back
            elif option == "0":
                break

            # Invalid option
            else:
                print("\n\t\t\t\t\t\t*****PLEASE ENTER A VALID OPTION*****\n")
                continue

    # ------------------------------------------------------------------------------------------------------------------

    # Phase b.3.1: Rename the component
    def EditComponentAttributeRename(self, windowEdit, component_edit):

        # Create a query to specify the component and rename it
        query = "UPDATE " + self.projectName + " SET Components = ? WHERE Components = ? AND Name = ?"

        componentEditRename = input("New name: ")

        self.cursor.execute(query, (componentEditRename, component_edit, windowEdit))
        self.connection.commit()

        print("\n\t\t\t\t\t\t***COMPONENT RENAMED SUCCESSFULLY: {}***\n".format(componentEditRename))

    # ------------------------------------------------------------------------------------------------------------------

    # Phase b.3.2: Edit the quantity
    def EditComponentAttributeQuantity(self, windowEdit, component_edit):

        # Create a query to specify the component and edit it's quantity
        query = "UPDATE " + self.projectName + " SET ComponentQuantity = ? WHERE Components = ? AND Name = ?"

        componentNewQuantity = int(input("New quantity: "))

        self.cursor.execute(query, (componentNewQuantity, component_edit, windowEdit))
        self.connection.commit()

        print("\n\t\t\t\t\t\t***COMPONENT QUANTITY UPDATED SUCCESSFULLY: {}***\n".format(componentNewQuantity))

    # ------------------------------------------------------------------------------------------------------------------

    # Phase b.3.3: Edit the length
    def EditComponentAttributeLength(self, windowEdit, component_edit):

        # Create a query to specify the component and edit it's length
        query = "UPDATE " + self.projectName + " SET Length = ? WHERE Components = ? AND Name = ?"

        componentNewLength = input("New length: ")

        self.cursor.execute(query, (imp2dec(componentNewLength), component_edit, windowEdit))
        self.connection.commit()

        print("\n\t\t\t\t\t\t***COMPONENT LENGTH UPDATED SUCCESSFULLY: {}***".format(componentNewLength))

    # ------------------------------------------------------------------------------------------------------------------

    # This will give us the next component. Such as if we have 'Head 2' as last one, this function will give us 'Head 3'
    def GetValidComponentID(self, windowEdit, component):

        # Get the related components
        query = "SELECT Components FROM " + self.projectName + " WHERE Components LIKE ? AND Name = ? ORDER BY Components"

        self.cursor.execute(query, ('%' + component + '%', windowEdit))
        products = self.cursor.fetchall()

        # The length of the products shows how many same kind of component is there.
        return component + " " + str((len(products) + 1))

    # ------------------------------------------------------------------------------------------------------------------

    # Showing ALL properties
    # def ShowProducts(self):
    #   query = "SELECT*FROM " + self.projectName + " ORDER BY Name"

    #  self.cursor.execute(query)
    #   products = self.cursor.fetchall()

    # for name, component, component_quantity, length, window_quantity in products:
    #      print("""
    #       Name: {}\
    #   Component: {}\
    #    Component Quantity: {}\
    #    Length: {} inches\
    #   Window Quantity: {}\
    #    """.format(name, component, component_quantity, dec2imp(length), window_quantity))

    # Showing product name and it's quantity

    # ------------------------------------------------------------------------------------------------------------------

    def ShowWindowNamesAndQuantities(self):
        query = "SELECT Name, WindowQuantity, WindowHeight, WindowWidth FROM " + self.projectName + " GROUP BY Name ORDER BY Name"

        self.cursor.execute(query)
        products = self.cursor.fetchall()

        print("{}'s WINDOW LIST\n========================================".format(current_project_name))
        for name, window_quantity, window_height, window_width in products:
            print("""
            Name: {}\
            Quantity: {}\
            WindowHeight: {}\
            WindowWidth: {}\
            """.format(name, window_quantity, dec2imp(window_height), dec2imp(window_width)))

    # ------------------------------------------------------------------------------------------------------------------

    def ShowWindowNameAndComponents(self):
        query = "SELECT Name FROM " + self.projectName + " GROUP BY Name ORDER BY Name"

        self.cursor.execute(query)
        products = self.cursor.fetchall()

        while True:
            windowDict = dict()
            windowDict.update({"0": "Back"})

            count = 1
            print("\n\t\t\t{}'s WINDOW LIST\n\t\t\t========================================".format(current_project_name))
            for name in products:
                print("\t\t\t{} - {}".format(count, name[0]))
                windowDict.update({str(count): name[0]})
                count += 1
            print("\t\t\t0 - Back")

            option = input()

            if option in windowDict:
                windowName = windowDict[option]
            else:
                print("\n\t\t\t*****PLEASE ENTER A VALID OPTION*****\n")
                continue

            if windowName == "Back":
                break

            query = "SELECT Name, Components, ComponentQuantity, Length FROM " + self.projectName + " WHERE Name = ? ORDER BY Components"

            self.cursor.execute(query, (windowName,))
            products = self.cursor.fetchall()

            print("\n\t\t\t\t{}'s COMPONENT LIST\n\t\t\t\t========================================".format(windowName))
            for name, component, componentQuantity, componentLength in products:
                print("""
                Name: {}\
                Components: {}\
                Comp. Quantity: {}\
                Comp. Length: {}\
                """.format(name, component, componentQuantity, dec2imp(componentLength)))
                print("\n")
            break

    # ------------------------------------------------------------------------------------------------------------------

    def DeleteWindow(self):
        query = "SELECT Name FROM " + self.projectName + " GROUP BY Name ORDER BY Name"

        self.cursor.execute(query)
        products = self.cursor.fetchall()

        while True:
            windowDict = dict()
            windowDict.update({"0": "Back"})

            count = 1
            for name in products:
                print("{} - {}".format(count, name[0]))
                windowDict.update({str(count): name[0]})
                count += 1
            print("0 - Back")

            option = input()

            if option in windowDict.keys():
                windowDelete = windowDict[option]
            else:
                print("\n*****PLEASE ENTER A VALID OPTION*****\n")
                continue

            if windowDelete == "Back":
                break

            print("You are about to delete {}, are you sure sure (Y/N)?:".format(windowDelete))
            choice = input()

            if choice == "n" or choice == "N":
                break

            elif choice == "y" or choice == "Y":
                query = "DELETE FROM " + self.projectName + " WHERE Name = ?"

                self.cursor.execute(query, (windowDelete,))
                self.connection.commit()

                print("\n*****Window deleted successfully\n\n")
                break

            else:
                print("\n*****PLEASE ENTER A VALID OPTION*****\n")
                continue


# ======================================================================================================================
# FUNCTIONS
# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------

def EnterOption():
    return input("Option: ")


# ----------------------------------------------------------------------------------------------------------------------


def EnterQuantityOfTypes():
    while True:
        try:
            quantity = int(input("Quantity of types: "))
        except ValueError:
            print("\n\t\t\t*****PLEASE ENTER A VALID VALUE*****\n")
            continue
        else:
            return quantity


# ----------------------------------------------------------------------------------------------------------------------


def EnterLength(component, i):
    while True:
        try:
            length = input("Length of {}{}(x'-y\"): ".format(component, i + 1))
            length = imp2dec(length)
        except ValueError:
            print("\n\t\t\t*****PLEASE ENTER A VALID VALUE*****\n")
            continue
        else:
            return length


# ----------------------------------------------------------------------------------------------------------------------


def EnterQuantityHeightWidth(windowName):
    while True:
        try:
            height = input("Height of {}(x'-y\"): ".format(windowName))
            height = imp2dec(height)

            width = input("Width of {}(x'-y\"): ".format(windowName))
            width = imp2dec(width)

            quantity = int(input("Quantity of {}: ".format(windowName)))

        except ValueError:
            print("\n\t\t\t*****PLEASE ENTER A VALID VALUE*****\n")
            continue

        else:
            return quantity, height, width


# ----------------------------------------------------------------------------------------------------------------------


def EnterQuantityOfComponent(component, i):
    while True:
        try:
            quantity = int(input("How many {}{}: ".format(component, i + 1)))
        except ValueError:
            print("\n\t\t\t*****PLEASE ENTER A VALID VALUE*****\n")
            continue
        else:
            return quantity


# ----------------------------------------------------------------------------------------------------------------------

def Exit():
    print("Exiting..")
    exit()


# ----------------------------------------------------------------------------------------------------------------------


def MenuProjectSelect():
    print("""
MAIN MENU
========================================
1 - New project
2 - Open project
3 - Delete project
0 - Exit
""")


# ----------------------------------------------------------------------------------------------------------------------


def Menu():
    print("""
        {}'s WINDOW MENU
        ========================================
        1 - Add new window
        2 - Delete window
        3 - Update component length (will be 'Edit window' soon)
        4 - Show names
        5 - Show names & components
        0 - Back
        """.format(current_project_name))


# ----------------------------------------------------------------------------------------------------------------------


def MenuComponents():
    print("""
            WINDOW COMPONENTS
            ========================================
            1 - Head
            2 - Sill
            3 - Jamb
            4 - Door Jamb (D.J.)
            5 - H. Mullion (H.M.) 
            6 - V. Mullion (V.M.)
            7 - Door Head (D.H.)
            0 - Return
            """)


# ----------------------------------------------------------------------------------------------------------------------


def MenuEditCompOrWin():
    print("""
                EDIT WINDOW OR COMPONENT
                ========================================
                1 - Edit window attributes
                2 - Edit components
                0 - Back
                """)


# ----------------------------------------------------------------------------------------------------------------------


def MenuEditWindowAttribute():
    print("""
                    EDIT WIN. ATTRIBUTES
                    ========================================
                    1 - Rename win.
                    2 - Quantity
                    3 - Height
                    4 - Width
                    0 - Back
                    """)


# ----------------------------------------------------------------------------------------------------------------------


def MenuEditComponent():
    print("""
                    EDIT COMPONENT
                    ========================================  
                    1 - Add component
                    2 - Delete component
                    3 - Edit comp. attributes
                    0 - Back
                    """)


# ----------------------------------------------------------------------------------------------------------------------


def MenuEditComponentAttribute():
    print("""
                            EDIT COMP. ATTRIBUTES
                            ========================================  
                            1 - Rename comp.
                            2 - Quantity
                            3 - Length
                            0 - Back
                            """)


# ----------------------------------------------------------------------------------------------------------------------


# Component saver
def SaveComponents(name, component, component_quantity, length, quantity, window_height, window_width):
    new_product = Fenestration(name, component, component_quantity, length, quantity, window_height, window_width)
    FDataBase = FenestrationDataBase(current_project_name)
    FDataBase.AddWindow(new_product)


# ----------------------------------------------------------------------------------------------------------------------


# Component menu
def MenuComponentsOptions(name, quantity, window_height, window_width):
    while True:
        MenuComponents()
        option = EnterOption()
        # HEAD
        if option == "1":
            print("HEAD")

            for i in range(EnterQuantityOfTypes()):
                component_quantity = EnterQuantityOfComponent("Head ", i)
                length = EnterLength("Head ", i)
                SaveComponents(name, "Head {}".format(i + 1), component_quantity, length, quantity, window_height,
                               window_width)

        # SILL
        elif option == "2":
            print("SILL")

            for i in range(EnterQuantityOfTypes()):
                component_quantity = EnterQuantityOfComponent("Sill ", i)
                length = EnterLength("Sill ", i)
                SaveComponents(name, "Sill {}".format(i + 1), component_quantity, length, quantity, window_height,
                               window_width)

        # JAMB
        elif option == "3":
            print("JAMB")

            for i in range(EnterQuantityOfTypes()):
                component_quantity = EnterQuantityOfComponent("Jamb ", i)
                length = EnterLength("Jamb ", i)
                SaveComponents(name, "Jamb {}".format(i + 1), component_quantity, length, quantity, window_height,
                               window_width)

        # JAMB
        elif option == "4":
            print("DOOR JAMB")

            for i in range(EnterQuantityOfTypes()):
                component_quantity = EnterQuantityOfComponent("Door Jamb ", i)
                length = EnterLength("Door Jamb ", i)
                SaveComponents(name, "D.J. {}".format(i + 1), component_quantity, length, quantity, window_height,
                               window_width)

        # H MULLION
        elif option == "5":
            print("H. MULLION")

            for i in range(EnterQuantityOfTypes()):
                component_quantity = EnterQuantityOfComponent("H. Mullion ", i)
                length = EnterLength("H. Mullion ", i)
                SaveComponents(name, "H.M. {}".format(i + 1), component_quantity, length, quantity, window_height,
                               window_width)

        # V MULLION
        elif option == "6":
            print("V. MULLION")

            for i in range(EnterQuantityOfTypes()):
                component_quantity = EnterQuantityOfComponent("V. Mullion ", i)
                length = EnterLength("V. Mullion ", i)
                SaveComponents(name, "V.M. {}".format(i + 1), component_quantity, length, quantity, window_height,
                               window_width)

        # DOORHEAD
        elif option == "7":
            print("DOOR HEAD")

            for i in range(EnterQuantityOfTypes()):
                component_quantity = EnterQuantityOfComponent("Doorhead ", i)
                length = EnterLength("Doorhead ", i)
                SaveComponents(name, "D.H. {}".format(i + 1), component_quantity, length, quantity, window_height,
                               window_width)

        # RETURN
        elif option == "0":
            break

        else:
            print("\n*****PLEASE ENTER A VALID OPTION*****\n")
            continue

        print("\n*****Component added successfully\n\n")


# ----------------------------------------------------------------------------------------------------------------------


# This will show all existing projects
def ShowTables():
    connection = sqlite3.connect("FenestrationDataBase.db")
    cursor = connection.cursor()

    query = "SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';"

    cursor.execute(query)
    tables = cursor.fetchall()

    tableDict = dict()
    tableDict.update({"0": "Back"})

    count = 1
    print("\n\tCURRENT PROJECTS\n\t================")
    for element in tables:
        print("\t{} - {}".format(str(count), element[0]))
        tableDict.update({str(count): element[0]})
        count += 1

    return tableDict


# ----------------------------------------------------------------------------------------------------------------------


# This will open a project
def OpenProject():
    while True:
        tableDict = ShowTables()
        option = input()
        # Check if it is a valid option. If it is, call the name from the dict
        if option in tableDict.keys():
            if option == "0":
                print("\n*****PLEASE ENTER A VALID OPTION*****\n")
                continue
            projectName = tableDict[option]
        else:
            print("\n*****PLEASE ENTER A VALID OPTION*****\n")
            continue
        return projectName


# ----------------------------------------------------------------------------------------------------------------------


# This will delete a project
def DeleteProject():
    connection = sqlite3.connect("FenestrationDataBase.db")
    cursor = connection.cursor()

    while True:

        print("\n\tDELETE")
        tableDict = ShowTables()
        print("\t0 - Back")
        option = input()

        # Check if it is a valid option. If it is, call the name from the dict
        if option in tableDict.keys():
            projectName = tableDict[option]
        else:
            print("\n*****PLEASE ENTER A VALID OPTION*****\n")
            continue

        if projectName == "Back":
            return

        print("You are about to delete {}, are you sure sure (Y/N)?:".format(projectName))
        choice = input()

        if choice == "n" or choice == "N":
            break

        query = "DROP TABLE " + projectName

        cursor.execute(query)
        connection.commit()

        print("\n*****Project deleted successfully\n\n")

        break
