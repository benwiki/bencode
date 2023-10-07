from os import system


def clear(): #shell clearen
    system('clear')

def bmi(größe: float, gewicht: float):
    bmi = (gewicht/(größe * 2)) * 100
    print(f"Dein BMI ist {round(bmi,2)}.")

    if bmi < 18.5:
        print("Das entspricht Untergewicht.")
    elif 18.5 > bmi > 25.0:
        print("Das entspricht Normalgewicht.")
    elif bmi > 25.0:
        print("Das entspricht Übergewicht.")     
   

if __name__ == "__main__":
    clear()
    bmi(180, 62.5) #Aufruf