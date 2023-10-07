from os import system


def clear(): #shell clearen
   _ = system('clear')

def mph_zu_kmh():
    clear()
    val = float(input("Geschwindigkeit in mp/h eingeben: "))
    print ((str(val * 1.61) + " km/h"))

def kmh_zu_mph():
    clear()
    val = float(input("Geschwindigkeit in km/h eingeben: "))
    print ((str(val * 1/1.61)) + " mp/h")
    


if __name__ == "__main__":

    clear()
    a = float(input("\n" + "Funktionswahl:" + "\n" + "(1) mp/h zu km/h " + "\n" + "(2) km/h zu mp/h " + "\n"))

    match a:
        case 1:
            mph_zu_kmh()
        case 2: 
            kmh_zu_mph()
        case _:
            raise Exception("Falsche Eingabe")

    assert type(a) is float


# passt soweit