def SpellNumber(myNumber):
    # Validate input
    try:
        myNumber = float(myNumber)
        if myNumber < 0:
            return ValueError("Input cannot be negative")
    except ValueError:
        return ValueError("Input must be a number")


    pesos = ''
    centavos = ''
    place = [''] * 10
    place[2] = ' Mil '
    place[3] = ' Millón '
    place[4] = ' Mil Millones '
    place[5] = ' Billones '
    
    # String representation of amount.
    myNumber = str(myNumber).strip()
    
    # Position of decimal place 0 if none.
    decimal_place = myNumber.find('.')
    
    # Convert Centavos and set myNumber to Peso amount.
    if decimal_place > 0:
        centavos = str(int(myNumber[decimal_place + 1: decimal_place + 3])).zfill(2)
        myNumber = myNumber[:decimal_place].strip()
    
    count = 1
    while myNumber != '':
        temp = get_hundreds(myNumber[-3:])
        if temp != '':
            pesos = temp + place[count] + pesos
        if len(myNumber) > 3:
            myNumber = myNumber[:-3]
        else:
            myNumber = ''
        count += 1
    
    
    if pesos == '':
        pesos = 'No Pesos'
    elif pesos == 'Uno':
        pesos = 'Un Peso'
    else:
        pesos = pesos.strip() #+ ' Pesos' 
    
    # Cents
    if centavos == '':
        centavos = ' y 00/100'
    else:
        centavos = ' y ' + centavos + '/100'
    
    return pesos + centavos
    

# Converts a number from 100-999 into text
def get_hundreds(myNumber):
    result = ''
    if int(myNumber) == 0:
        return result
    
    myNumber = myNumber.zfill(3)
    if myNumber == "100":
        result = "Cien"
    elif myNumber == "200":
        result = "Dosciento"
    elif myNumber == "300":
        result = "Tresciento"
    elif myNumber == "400":
        result = "Cuatrociento"
    elif myNumber == "500":
        result = "Quinciento"
    elif myNumber == "600":
        result = "Seisciento"
    elif myNumber == "700":
        result = "Seteciento"
    elif myNumber == "800":
        result = "Ochociento"
    elif myNumber == "900":
        result = "Nuevociento"
    else:
        # Convert the hundreds place.
        if myNumber[0] != '0':
            if myNumber[0] == '1':
                result = 'Ciento '
            elif myNumber[0] == '2':
                result = 'Doscientos '
            elif myNumber[0] == '3':
                result = 'Trescientos '
            elif myNumber[0] == '4':
                result = 'Cuatrocientos '
            elif myNumber[0] == '5':
                result = 'Quinientos '
            elif myNumber[0] == '6':
                result = 'Seiscientos '
            elif myNumber[0] == '7':
                result = 'Setecientos '
            elif myNumber[0] == '8':
                result = 'Ochocientos '
            elif myNumber[0] == '9':
                result = 'Novecientos '
    
    # Convert the tens and ones place.
    if myNumber[1] != '0':
        result += GetTens(myNumber[1:])
    else:
        result += GetDigit(myNumber[2])
    return result
    

def GetTens(Digit):
    Result = ""  # Null out the temporary function value.
    if int(Digit[:1]) == 1 and int(Digit) != 10:  # If value between 10-19...
        Result = ["Diez", "Once", "Doce", "Trece", "Catorce",
                  "Quince", "Dieciséis", "Diecisiete", "Dieciocho",
                  "Diecinueve"][int(Digit[1:])]
    else:  # If value between 20-99...
        case_value = int(Digit[:1])
        Result = ["", "Diez", "Veinte ", "Treinta ", "Cuarenta ", "Cincuenta ",
                  "Sesenta ", "Setenta ", "Ochenta ", "Noventa "][case_value]
        if int(Digit[1:]) != 0:
            Result += GetDigit(int(Digit[1:]))  # Retrieve ones place. 
    return Result


# Converts a number from 1 to 9 into text.
def GetDigit(Digit):
    result = ''
    case_value = int(Digit)
    if case_value == 1:
        result = 'Uno'
    elif case_value == 2:
        result = 'Dos'
    elif case_value == 3:
        result = 'Tres'
    elif case_value == 4:
        result = 'Cuatro'
    elif case_value == 5:
        result = 'Cinco'
    elif case_value == 6:
        result = 'Seis'
    elif case_value == 7:
        result = 'Siete'
    elif case_value == 8:
        result = 'Ocho'
    elif case_value == 9:
        result = 'Nueve'
    return result
    
'''number = ""
while number != 0:
    number = SpellNumber(input("Please enter a number "))
    print (f"\n{number}")
    print ("Enter 0 to close\n")'''