
def xor(a, b):
    if len(a)<=0 or len(b)<=0 or len(a)!=len(b):
        return ""

    result = ""
    for i in range(0, len(a)):
        if a[i]==b[i]:
            result+='0'
        else:
            result+='1'

    return result

def crc(dataword, crcgen, side):
    final = []

    if side=='s':
        dw = dataword + '0' * (len(crcgen) - 1)
    else:
        dw = dataword

    chunk = dw[dw.index('1'):len(crcgen)]

    result = xor(chunk, crcgen)

    recResult = result

    if all(v == '0' for v in result) == False:
        result = result[result.index('1'):]
    else:
        result = ""
    dw = dw[len(crcgen):]

    while (len(dw) > 0):
        borrower = len(crcgen) - len(result)
        chunk = result + dw[:borrower]
        if len(chunk)<len(crcgen):
            break
        result = xor(chunk, crcgen)
        recResult = result
        dw = dw[borrower:]
        if all(v == '0' for v in result) == False:
            if len(crcgen) > len(result[result.index('1'):] + dw):
                result =  str(result + dw)[-(len(crcgen) - 1):]
                if side=='r':
                    recResult=result
                    final.append(recResult)
                    final.append(dataword)
                    return tuple(final)
                final.append(result)
                final.append(dataword+result)
                return tuple(final)
            else:
                recResult = result
                result = result[result.index('1'):]
        else:
            recResult=result
            result = ""

    if side == 'r':
        final.append(recResult)
        final.append(dataword)
        return tuple(final)
    final.append(result)
    final.append(dataword+result)
    return tuple(final)

def banner(message, border='*'):
    print(border*len(message))
    print(message)
    print(border*len(message))


def fancySeparator(message, symbol='-'):
    print("\n")
    print(message)
    print(symbol*len(message))

def main():

    banner("Cyclic Redundancy check in python")

    dataword  = str(input("Enter the dataword:"))
    crcgen = str(input("Enter the crc:"))

    remainder, transmittedCodeWord = crc(dataword, crcgen, 's')

    fancySeparator("Sender side:", "-")

    print("Remainder = ", remainder)
    print("Transmitted codeword = ",transmittedCodeWord)

    fancySeparator("Reciever side:", "-")

    remainder, rcw  = crc(transmittedCodeWord, crcgen, 'r')

    print("Received codeword = ", rcw)
    print("Remainder = ", remainder)

    if all(v=='0' for v in remainder):
        print("No Error")




if __name__ == "__main__":
    main()