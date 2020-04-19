def imp2dec(a):
    # Ratio: NO//Spaces: NO      (2'-3")
    if a.find("/") == -1:
        if a.find("- ") == -1 and a.find(" -") == -1:
            foot = a[:a.find("'")]
            inch = a[a.find("-") + 1]
        ratio1 = 0
        ratio2 = 0

    # Ratio: NO//Spaces: YES     (2' - 3") or (2' -3") or (2'- 3")
    if a.find("/") == -1:
        foot = a[:a.find("'")]
        if a.find("- ") != -1:
            inch = a[a.find("-") + 2]
        elif a.find(" -") != -1 and a.find("- ") == -1:
            inch = a[a.find("-") + 1]
        ratio1 = 0
        ratio2 = 0

    # Ratio: YES//Spaces: NO
    if a.find("/") != -1:
        foot = a[:a.find("'")]
        if a.find("- ") == -1 and a.find(" -") == -1:
            inch = a[a.find("-") + 1]
        ratio1 = a[a.find("/") - 1]
        ratio2 = a[a.find("/") + 1]
        # Ratio: YES//Space: YES
        if a.find("- ") != -1:
            inch = a[a.find("-") + 2]
        elif a.find(" -") != -1 and a.find("- ") == -1:
            inch = a[a.find("-") + 1]
    decimal = int(foot) * 12 + int(inch)
    if int(ratio1) != 0:
        decimal += int(ratio1) / int(ratio2)

    return decimal


def dec2imp(a):
    # WITH FRACTION
    if (a / int(a)) != 1:
        a_float = round(a - int(a), 9)
        a1 = a - a_float

        a_int = int(a)
        inch = a1 % 12
        foot = (a_int - inch) / 12

        if a_float > 0:
            x = 1
            y = 1
            while abs(x / y - a_float) > .00000001:
                if x / y > a_float:
                    y += 1
                elif x / y < a_float:
                    x += 1
            text = "{}\'-{}\" {}/{}".format(round(foot), round(inch), x, y)
            return text
        else:
            text = "{}\'-{}\"".format(round(foot), round(inch))
            return text
    # WITHOUT FRACTION
    else:
        a_float = round(a - int(a), 1)
        a1 = a - a_float

        a_int = int(a)
        inch = a1 % 12
        foot = (a_int - inch) / 12

        text = "{}\'-{}\"".format(round(foot), round(inch))
        return text


def measures_sum():
    measure1 = input("1. Measure: ")
    measure1 = imp2dec(measure1)
    measure2 = input("2. Measure: ")
    measure2 = imp2dec(measure2)

    return measure1 + measure2


def measures_multiplicate():
    measure1 = input("1. Measure: ")
    measure1 = imp2dec(measure1)
    measure2 = input("2. Measure: ")
    measure2 = imp2dec(measure2)

    print(measure1)
    print(measure2)

    return measure1 * measure2


def menu():
    print("\n\n1-imp2dec")
    print("2-sum")
    print("3-multiplicate")
    print("4-dec2imp")
