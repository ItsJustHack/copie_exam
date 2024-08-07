class Chiffreur:
    """ This class represents an operation, if the latter is not valid, it raises an ValueError Exception """
    def __init__(self, operation):
        """
            Chiffreur("ROTn") represents an operation of rotation n times (where n is a positive integer)
            Chiffreur("TRAn") represents an operation of translation n times (where n is a positive integer)
            Chiffreur("MIR")  represents an operation of mirroring
            Anything else result in a ValueError
        """

        if operation == "MIR":
            self.__operation = miroir
            self.__number_of_operations = 1
        elif "ROT" in operation:
            try:
                (_, value) = operation.split("ROT")
                value = int(value)
                self.__operation = rotation_n_letters
                self.__number_of_operations = value
            except:
                raise ValueError
        elif "TRA" in operation:
            try:
                (_, value) = operation.split("TRA")
                value = int(value)
                self.__operation = translation
                self.__number_of_operations = value
            except:
                raise ValueError
        else: 
            raise ValueError

    def eval(self, input):
        """ This method evaluates the input with the operation associated to the instance """
        if self.__operation == miroir:
            return miroir(input)
        else: 
            return self.__operation(input, self.__number_of_operations) # self.__operation is a "reference" to a function 

    def get_operation(self):
        """ Getter of operation """
        return self.__operation 

    def get_number_of_operations(self):
        """ Getter of number_of_operations """
        return self.__number_of_operations


def rotation_n_letters(input: str, offset : int) -> str:
    """ Does an elementary rotation of n letters on input
        input : the input
        offset : the number of times the leementary rotation will be applied
    """
    coded_string = ""
    for lettre in input:
        assert(126 >= ord(lettre) >= 32)
        if (ord(lettre) + offset) // 127 == 1:
            coded_string += chr(32 + (ord(lettre) + offset) % 127)
        else: 
            coded_string += chr(ord(lettre) + offset)
    return coded_string

def miroir(input: str) -> str:
    """
        Does a reflection of the word in the ASCII table
        input: the input
    """
    coded_string = ""
    for lettre in input:
        assert(126 >= ord(lettre) >= 32)
        if ord(lettre) > 79: # 79 is the result of (126 + 32) // 2, so it's the index of the "mirror"
            coded_string += chr(79 - (ord(lettre) - 79))
        else: 
            coded_string += chr((79 - ord(lettre) + 79))
    return coded_string

def translation(input: str, offset: int) -> str : 
    """ Apply the elementary translation to the input 
        input : the input
    """

    def unique_translation(input: str):
        return  input[1:] + input[0]

    assert unique_translation("test") == ("estt")

    word = input 
    for _ in range(offset):
        word = unique_translation(word)
    return word

def parse_command(command: str):
    """ This function returns the value of the parsed command of the 'chiffre' function """
    (rot, tra, mir) = command.split(";")

    if rot == "ROT":
        rot = 1
    else: 
        (_, rot) = rot.split("ROT")

    if mir == "MIR":
        mir = 1
    else: 
        (_, mir) = mir.split("MIR")

    if tra == "TRA":
        tra = 1
    else: 
        (_, tra) = tra.split("TRA")

    return (int(rot), int(tra), int(mir))


def chiffre(input : str, command: str):
    (rot, tra, mir) = parse_command(command)

    # Apply rotation 
    word = rotation_n_letters(input, rot)

    # Apply translation
    word = translation(word, tra)


    # Apply mirroring
    for _ in range(mir):
        word = miroir(word)


    return word


def simplify(transformations : list[Chiffreur]) -> list[Chiffreur]:

    """ This function simplify a list of Chiffreur"""
    # It seems to not work as the final print is invalid

    if transformations == []:
        return []
    previous_transformation = transformations[0]
    list_of_transformations = []
    for chiffreur in transformations[1:]:

        list_of_transformations.append(previous_transformation)
        chiffreur_operation = chiffreur.get_operation()

        if chiffreur_operation == previous_transformation.get_operation():

            if chiffreur_operation == miroir:
                list_of_transformations.remove(previous_transformation)
                continue; 

            elif chiffreur_operation == rotation_n_letters:
                print("here")
                list_of_transformations.remove(previous_transformation)
                list_of_transformations.append(Chiffreur("ROT" + str(previous_transformation.get_number_of_operations() + chiffreur.get_number_of_operations())))

            else:
                list_of_transformations.remove(previous_transformation)
                list_of_transformations.append(Chiffreur("TRA" + str(previous_transformation.get_number_of_operations() + chiffreur.get_number_of_operations())))

        previous_transformation = chiffreur

    return list_of_transformations








if __name__ == "__main__":
    print(rotation_n_letters("La licorne n'a pas voulu regarder le lac", 10))

    print(miroir("La licorne n'a pas voulu regarder le lac"))

    print(translation("La licorne n'a pas voulu regarder le lac", 12))

    assert parse_command("ROT10;TRA5;MIR") == (10, 5, 1)
    print(chiffre("La licorne n'a pas voulu regarder le lac", "ROT10;TRA5;MIR"))


    print(Chiffreur("MIR").eval("La licorne n'a pas voulu regarder le lac"))
    print(Chiffreur("ROT10").eval("La licorne n'a pas voulu regarder le lac"))
    print(Chiffreur("TRA12").eval("La licorne n'a pas voulu regarder le lac"))
    
    try: 
        Chiffreur("ROT12,TRA12")
    except ValueError:
        print("L'exception est ici normale, tout va bien")

    print(simplify([Chiffreur("MIR"), Chiffreur("MIR"), Chiffreur("ROT13"), Chiffreur("ROT12")]))




