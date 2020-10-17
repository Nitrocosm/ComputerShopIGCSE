import csv
# import pprint

# import time
# import sys

md = {}
ad = {}

#  Compares MandatoryFlags categories to PartsList categories and if there is an error knows that there is extra data in MandatoryFlags
matchFlag = False
with open('MandatoryFlags.csv') as csv_flags:
    with open('PartsList.csv') as csv_parts:
        flags = csv.reader(csv_flags, delimiter=',')
        parts = csv.reader(csv_parts, delimiter=',')
        line_countFlags = 0
        line_countParts = 0
        for flags_row in flags:
            if line_countFlags == 0:
                line_countFlags += 1
            else:
                for parts_row in parts:
                    if line_countParts == 0:
                        line_countParts += 1
                    else:
                        if parts_row[0] == flags_row[0]:
                            matchFlag = True
                            break
                        else:
                            line_countParts += 1
                if matchFlag:
                    csv_parts.seek(0)
                    line_countParts = 0
                    matchFlag = False
                    line_countFlags += 1
                else:
                    print(
                        "Category from MandatoryFlags.csv not found in PartsList.csv! Please add entries in PartsList.csv or remove category from MandatoryParts.csv!")
                    exit()

#  Same thing as before, but vice versa
matchFlag = False
with open('MandatoryFlags.csv') as csv_flags:
    with open('PartsList.csv') as csv_parts:
        flags = csv.reader(csv_flags, delimiter=',')
        parts = csv.reader(csv_parts, delimiter=',')
        line_countFlags = 0
        line_countParts = 0
        for parts_row in parts:
            if line_countParts == 0:
                line_countParts += 1
            else:
                for flags_row in flags:
                    if line_countFlags == 0:
                        line_countFlags += 1
                    else:
                        if flags_row[0] == parts_row[0]:
                            matchFlag = True
                            break
                        else:
                            line_countFlags += 1
                if matchFlag:
                    csv_flags.seek(0)
                    line_countFlags = 0
                    matchFlag = False
                    line_countParts += 1
                else:
                    print(
                        "Category from PartsList.csv not found in MandatoryFlags.csv! Please add the category in MandatoryFlags.csv or remove category entries from MandatoryParts.csv!")
                    exit()

# Scan mandatory categories
with open('MandatoryFlags.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    mct = 1  # Mandatory Count
    act = 1  # Additional Count
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            if str(row[1]) == "Y":
                md["MCat{0}".format(mct)] = row[0]
                mct += 1
            elif str(row[1]) == "N":
                ad["ACat{0}".format(act)] = row[0]
                act += 1
            else:
                print("""Incorrect Boolean Type! Please use Y or N when referring to a category and if it is mandatory or not!
You can find the file in the same directory as this program, called MandatoryFlags.csv, and fix any errors!""")
                exit()
            line_count += 1

# GUI Option Setup

catd = {}
itemd = {}
holder = ()

# Pairs the Item Codes of mandatory categories with their respective categories
with open('PartsList.csv') as csv_file:
    mct = 1
    csv_reader = csv.reader(csv_file, delimiter=',')
    for x in range(0, len(md)):
        line_count = 0
        catd[str(md["MCat{0}".format(mct)])] = ()
        for row in csv_reader:
            if md['MCat{0}'.format(mct)] == row[0]:
                holder = list(catd[str(md["MCat{0}".format(mct)])])
                holder.append(str(row[1]))
                catd[str(md['MCat{0}'.format(mct)])] = tuple(holder)
            else:
                line_count += 1
        holder = ()
        mct += 1
        csv_file.seek(0)

#  Same thing as before, but with the optional categories
with open('PartsList.csv') as csv_file:
    act = 1
    csv_reader = csv.reader(csv_file, delimiter=',')
    for x in range(0, len(ad)):
        line_count = 0
        catd[str(ad['ACat{0}'.format(act)])] = ()
        for row in csv_reader:
            if ad['ACat{0}'.format(act)] == row[0]:
                holder = list(catd[str(ad["ACat{0}".format(act)])])
                holder.append(str(row[1]))
                catd[str(ad['ACat{0}'.format(act)])] = tuple(holder)
            else:
                line_count += 1
        holder = ()
        act += 1
        csv_file.seek(0)

#  Pairs up the item codes with their price and description
with open('PartsList.csv') as csv_file:
    line_count = 0
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            holder = [row[2], row[3]]
            itemd["{0}".format(row[1])] = tuple(holder)
            line_count += 1


#  It's time for the GUI! yay, kill me!
choices = {}
for i in range(0, len(md)):
    print("Choices for mandatory category: " + str(md["MCat{0}".format(i + 1)]))
    print("")
    matchFlag = False
    for x in range(0, len(catd[str(md["MCat{0}".format(i + 1)])])):
        itemcodeBuffer = str(catd[str(md["MCat{0}".format(i + 1)])][x])
        print("\t" + catd[str(md["MCat{0}".format(i + 1)])][x] + ": " + itemd[str(itemcodeBuffer)][0] + ", " +
              itemd[str(itemcodeBuffer)][1])
    print("")
    while 1 == 1:
        itemcodeInput = input("Enter the item code of the item you want: ").upper()
        for x in range(0, len(catd[str(md["MCat{0}".format(i + 1)])])):
            if itemcodeInput == str(catd[str(md["MCat{0}".format(i + 1)])][x]):
                matchFlag = True
            else:
                continue
        if matchFlag:
            break
        else:
            print("Invalid Input! Please enter a valid item code!")
    choices[str(md["MCat{0}".format(i + 1)])] = itemcodeInput
    print('\n')

print("The total of the cart right now:")
print("\tBase Components: Needed for the computer to function, $200")
cBuffer = list(choices.items())
cIterate = iter(cBuffer)
cPrice = 200
for x in range(0, len(choices)):
    cPair = next(cIterate)
    cPairList = list(cPair)
    print('\t' + ''.join("{}: {}".format(cPairList[0], cPairList[1])) + ", " + itemd[str(cPair[1])][0] + ", $" + itemd[str(cPair[1])][1])
    cPrice += float(itemd[str(cPair[1])][1])
print("")
print("Price: $" + str(cPrice))
print("")
print("")
print("The additional components are: " + ', '.join("{}".format(v) for v in ad.values()))
while True:
    addBool = input("Would you like to choose additional parts? Y/N: ").upper()
    if addBool == 'Y':
        addFlag = True
        break
    elif addBool == 'N':
        addFlag = False
        break
    else:
        print("Invalid Input! Please enter Y for yes or N for no!")
print("\n")

if addFlag:
    for i in range(0, len(ad)):
        print("Choices for additional category: " + str(ad["ACat{0}".format(i + 1)]))
        print("")
        nullFlag = False
        matchFlag = False
        for x in range(0, len(catd[str(ad["ACat{0}".format(i + 1)])])):
            itemcodeBuffer = str(catd[str(ad["ACat{0}".format(i + 1)])][x])
            print("\t" + catd[str(ad["ACat{0}".format(i + 1)])][x] + ": " + itemd[str(itemcodeBuffer)][0] + ", " + itemd[str(itemcodeBuffer)][1])
        print("\tor skip this category by typing 'null'.")
        print("")
        while 1 == 1:
            itemcodeInput = input("Enter the item code of the item you want: ").upper()
            for x in range(0, len(catd[str(ad["ACat{0}".format(i + 1)])])):
                if itemcodeInput == str(catd[str(ad["ACat{0}".format(i + 1)])][x]):
                    matchFlag = True
                elif itemcodeInput == "NULL":
                    nullFlag = True
                else:
                    continue
            if matchFlag:
                break
            elif nullFlag:
                break
            else:
                print("Invalid Input! Please enter a valid item code!")
        if matchFlag:
            choices[str(ad["ACat{0}".format(i + 1)])] = itemcodeInput
        else:
            print("")
            continue
        print('')

print("The final total of the cart:")
print("\tBase Components: Needed for the computer to function, $200")
cBuffer = list(choices.items())
cIterate = iter(cBuffer)
cPrice = 200
for x in range(0, len(choices)):
    cPair = next(cIterate)
    cPairList = list(cPair)
    print('\t' + ''.join("{}: {}".format(cPairList[0], cPairList[1])) + ", " + itemd[str(cPair[1])][0] + ", $" + itemd[str(cPair[1])][1])
    cPrice += float(itemd[str(cPair[1])][1])
print("")
if len(choices) - len(md) >= 2:
    print("Normal Price: $" + str(cPrice))
    print("Because you chose " + str(len(choices)- len(md)) + " additional items, you benefit from a 10% discount!")
    print("\tMoney Saved: $" + str(round(cPrice * 0.1, 2)))
    print("\tFinal Price: $" + str(round(cPrice * 0.9, 2)))

elif len(choices) - len(md) == 1:
    print("Normal Price: $" + str(cPrice))
    print("Because you chose 1 additional item, you benefit from a 5% discount!")
    print("\tMoney Saved: $" + str(round(cPrice * 0.05, 2)))
    print("\tFinal Price: $" + str(round(cPrice * 0.95, 2)))

else:
    print("\tFinal Price: $" + str(cPrice))
