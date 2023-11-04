# |======================================================================|
# |=| Program to find an element on a group XML files inside of        |=|
# |=| .\data\files\<XML files> folder and the list of orders that we   |=|
# |=| are looking for inside of .\data\list.txt file.                  |=|
# |======================================================================|

# |==| Importing modules |==|
import os
import sys
import xml.etree.ElementTree as ET

# |==| Global variables  |==|
path = os.getcwd()
path = path + "\\data"
orders = []
xml_files = []

# |==| Main function |==|

# |==| Reading the list of orders |==|
# |==| and saving it into a list  |==|
# |==| by using try and except    |==|
try:
    with open(path + "\\list.txt", "r") as file:
        for line in file:
            orders.append(line.rstrip())
except:
    print("Error: The file list.txt doesn't exist")
    sys.exit()

# |==| Reading the XML files and   |==|
# |==| saving it into a list by    |==|
# |==| using try and except        |==|
try:
    for file in os.listdir(path + "\\files"):
        xml_files.append(file)
except:
    print("Error: The folder files doesn't exist or it's empty")
    sys.exit()

# |==| Creating the folder to save |==|
# |==| the XML files that we found |==|
# |==| and pass if exists          |==|
try:
    os.mkdir(path + "\\found")
except:
    pass
# |==| Creating log.csv            |==|
# |==| and pass if exists          |==|
try:
    with open(path + "\\found\\log.csv", "w") as file:
        file.write("Order,Found\n")
except:
    pass

# |==| Finding the orders one by   |==|
# |==| one creating a new folder   |==|
# |==| for each one of them.       |==|
for order in orders:
    # We define not found as default at the log file
    with open(path + "\\found\\log.csv", "a") as file:
        file.write("{0},False\n".format(order))
    try:
        # |==| Reading the XML files one by one |==|
        for file in xml_files:
            tree = ET.parse(path + "\\files\\" + file)
            # |==| Searching the order on the current XML file |==|
            for element in tree.iter(tag='WorkOrderCompleted'):
                for child in element:
                    if child.tag == 'WorkOrder':
                        if child.attrib['WorkOrderNbr'] == order:
                            # |==| Copying the file to the new folder |==|
                            # print("Order {0} found on file {1}".format(order, file))
                            # os.system("copy {0} {1}".format(path + "\\files\\" + file, path + "\\" + order))
                            print("File {0} copied to folder {1}".format(file, order))
                            # Moving the file to the found folder
                            os.system("move {0} {1}".format(path + "\\files\\" + file, path + "\\found"))
                            # Removing the file from the list of XML files
                            xml_files.remove(file)
                            # Modify the log file to true
                            with open(path + "\\found\\log.csv", "r") as file:
                                lines = file.readlines()
                            with open(path + "\\found\\log.csv", "w") as file:
                                for line in lines:
                                    if line.split(',')[0] == order:
                                        file.write("{0},True\n".format(order))
                                    else:
                                        file.write(line)
                            # Break the loop
                            break

    except:
        print("Error: The file {0} doesn't exist or it's empty".format(file))
        sys.exit()

print("Process finished")