
class Rotore:

    def __init__(self,number,reflector,cyphers,prev=None,alphabeth="qwertzuioasdfghjkpyxcvbnml",initial_rotors=None):
        self.alphabeth = alphabeth
        self.reflector = reflector
        self.prev = prev
        self.hasMoved = False
        self.number = 4-number
        self.rotation = 0
        self.movement = 0
        self.cypher = cyphers[number-1]
        if(initial_rotors is not None):
            while(self.alphabeth[0]!=initial_rotors[3-number]):
                self.alphabeth = self.alphabeth[1:] + self.alphabeth[0]
                self.cypher = self.cypher[1:] + self.cypher[0]

        if(number != 1):
            self._next = Rotore(number-1,self.reflector,cyphers,self,initial_rotors=initial_rotors)
        else:
            self._next = None

    def crypt(self,index):

        # Cripto col rotore
        letter = self.alphabeth[index]
        index = self.cypher.find(letter)
        
        if(self._next is None):
            # Ultimo Rotore Passato
            # Ora entra in gioco il riflettore
            index = self.alphabeth[index]
            index = self.reflector.find(index)
        else:
            # Non ho raggiunto l'ultimo rotore
            # Quindi invio la lettera al successivo
            index = self._next.crypt(index)

        # Passaggio al contrario nei rotori
        letter = self.cypher[index]
        index = self.alphabeth.find(letter)

        if(self.prev is None or self.prev.hasMoved):
            if(self.prev is not None):
                self.prev.hasMoved = False
            self.alphabeth = self.alphabeth[1:] + self.alphabeth[0]
            self.cypher = self.cypher[1:] + self.cypher[0]
            self.movement += 1
            if(self.movement == 26):
                self.rotation += 1
                #print(f'rotore {self.number} has moved for the {self.rotation} time')
                self.hasMoved = True
                self.movement = 0

        return index
     
class Enigma:

    rotors_cyphers = [
            "stiofmyzeqdlbckjgvpurwnxah",
            "yufhxzmnjgopaqirldtwvksbce",
            "avoeyfwldqcbsptkrgijuhxzmn",
            ]
    
    def __init__(self,rotori=3,alphabeth="qwertyuiopasdfghjklzxcvbnm",reflector="kmihugtevjclxzraqnbfsoypwd",initial_rotors=None,cyphers=None):
        self.rotor_number = rotori
        self.rotori = Rotore(rotori,cyphers=self.rotors_cyphers,reflector=reflector,initial_rotors=initial_rotors)
        self.alphabeth = alphabeth
        self.reflector = reflector  
        if(cyphers is not None):
            self.rotors_cyphers = cyphers
        
         
    def info(self):
        string = f"""#############################
#    Welcome in Enigma Machine
#    This Machine have {self.rotor_number} rotors,
#    The following informations is about its rotors:
#    """
        r = self.rotori
        for x in range(self.rotor_number):
            cypher = r.cypher
            string += f"""
#    - Rotor n° {x+1} :
#    alphabeth = {r.alphabeth}
#    cypher = {cypher}
#    """
            r = r._next

        string += f"""
#    The Reflector following the seguent schema:
#    alphabet =  {self.alphabeth}
#    reflector = {self.reflector}
#########################################        """
        return string

    def crypt(self,message):
        message = message.replace(" ","")
        result = ""
        for char in message:
            result += self.alphabeth[self.rotori.crypt(self.alphabeth.find(char))]
        return result

# Settings
#######################

initial_rotors_letter = [   
    # Start letter of rotors's alphabet
    'q',    # First Rotor
    'q',    # Second Rotor
    'q',    # Third Rotor
]
rotors_cyphers = [  
    # Rotors Cypher
    "stiofmyzeqdlbckjgvpurwnxah",   # First Rotor
    "yufhxzmnjgopaqirldtwvksbce",   # Second Rotor
    "avoeyfwldqcbsptkrgijuhxzmn",   # Third Rotor
]
reflector = "kmihugtevjclxzraqnbfsoypwd" # Reflector Change Set
alphabeth = "qwertyuiopasdfghjklzxcvbnm" # Standard Alphabeth

#######################
# End Setting

if __name__ == "__main__":
    e = Enigma(alphabeth=alphabeth, initial_rotors=initial_rotors_letter, cyphers=rotors_cyphers, reflector=reflector)
    print(e.info())
    while(True):
        e = Enigma(alphabeth=alphabeth, initial_rotors=initial_rotors_letter, cyphers=rotors_cyphers, reflector=reflector)
        
        res = e.crypt(input("Inserisci Messaggio Da Criptare o Decriptare : \n"))
        print("Il Messaggio Criptato/Decriptato è : \n" + res)
        print("Restarting Enigma Machine...\n")
