
def exo1(n):
    n=n+4
    n=n**3
    return n

a = exo1(1)
print(a)

def exo2(HT, TVA):
    TVA = HT * TVA
    TTC = HT + TVA
    return TTC

TTC = exo2(10,0.1)
print(TTC)


annee = int(input("Entrez l annee a verifier:"))
if(annee%4==0 and annee%100!=0 or annee%400==0):
    print("L'annee est une annee bissextile!")
else:
    print("L'annee n'est pas une annee bissextile!")




degree = int(input("Entrez la température à convertir:"))
degree_bool = int(input("Convertir en Fahrenheit tapez 0, en Celsius tapez 1:"))
if(degree_bool=="0"):
    fahrenheit= 9./5.*degree+32
    print(fahrenheit+" Fahrenheit")
else:
    celsius= degree-32./9./5
    print (celsius," Celsius")



def cCelToFah(celsius) :
    fahrenheit= 9./5.*celsius+32
    return fahrenheit



print("FIN de laconversion")

print("EXO 5")

mot="test"

mot=input("Rentrez un mot (sans accent) : ")

mot_min=mot.lower()

liste_voyelles=["a","e","i","o","u","y"]

nb_voyelles = 0

for lettre in mot_min :
    if lettre in liste_voyelles :
        nb_voyelles+=1

if   nb_voyelles == 0 :
    print("Il n'y a pas de voyelles dans le mot \"" + mot + "\".\n")
elif  nb_voyelles == 1 :
    print("Il y a une seule voyelle dans le mot \"" + mot + "\".\n")
else :
    print("Le mot \"" + mot + "\" contient " + str(nb_voyelles) + " voyelles.\n")

print("\n\n")


