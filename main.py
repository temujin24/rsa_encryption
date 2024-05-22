from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.properties import StringProperty
from random import randint
from math import gcd



def Ascii(text):
    """takes in text, a string, and returns a list where each item is
    the ascii decimal value for each character in text"""

    new_text = []
    for character in text:
        new_text.append(ord(character))
    return new_text


def Character(numbers):
    """takes in numbers, a list of numbers, and returns a list where each item is
    the ascii charater for each value in numbers"""

    new_text = []
    for number in numbers:
        new_text.append(chr(number))
    return new_text


def IsPrime(n):
    """takes in n, an integer, and returns True if n is prime"""

    for i in range(2, n//2+1):
        if n%i == 0:
            return False
    return True


def GenRandPrime(min, max):
    """takes in min and max, 2 integers, and returns 2 random
    prime integers less than max and greater than min"""
    
    number = randint(min,max)
    if IsPrime(number):
        return number
    else:
        return GenRandPrime(min, max)


def CoPrime1(a, b):
    """takes in a and b, 2 integers, and returns
    whether true if they are Co-prime"""

    return gcd(a, b) == 1


def CoPrime2(e, modulus, phifunction):
    """takes in e, modulus, and phifunction, 3 integers, and 
    returns true if e and modulus are Co-prime and if e and
    phifunction are Co-prime"""

    if CoPrime1(e, modulus) and CoPrime1(e, phifunction):
        return True
    else:
        return False


def gen_public_key(modulus, phifunction):
    """takes in modulus and phifunction, 2 integers, and generates a
    random integer e which is less than phifunction and is Co-prime
    with modulus and phifunction"""

    e = randint (1, phifunction)
    if CoPrime2(e, modulus, phifunction):
        return e
    else:
        return gen_public_key(modulus, phifunction)


def gen_private_key(public_key, phifunction):
    """takes in public_key and phifunction, 2 integers, and
    returns private_key such that
    (private_key*public_key)%phifunction == 1"""

    for i in range(phifunction * 100):
        if (i * public_key) % phifunction == 1:
            random_factor = randint(1, 5)
            private_key = i * ((phifunction * random_factor) + 1)
            return private_key


def Encrypt(message, key, modulus):
    """takes in message, key, and modulus, 3 integers,
    and encrypts message using RSA encryption"""

    return (message ** key) % modulus


def GenerateKeys():
    """generates a valid public key, private key, and modulus for
    RSA encryption, the private key must be greater than 1000 and 
    less than 100000 for performance"""

    global Public_Key_Actual
    global Private_Key_Actual
    global Modulus_Actual
    Prime1 = GenRandPrime(2, 50)
    Prime2 = GenRandPrime(2, 50)
    Modulus_Actual = Prime1 * Prime2
    Phi_Funcion = (Prime1 - 1) * (Prime2 - 1)
    Public_Key_Actual = gen_public_key(Modulus_Actual, Phi_Funcion)
    Private_Key_Actual = gen_private_key(Public_Key_Actual, Phi_Funcion)
    if 1000 > Private_Key_Actual or Private_Key_Actual > 100000:
         GenerateKeys()


class MainWindow(Screen):
    pass


class EncryptionScreen(Screen):

    def __init__(self, **kwargs):
        super(EncryptionScreen, self).__init__(**kwargs)
        GenerateKeys()
        self.Privato_key = Private_Key_Actual
        self.Publuco_key = Public_Key_Actual
        self.Modululo = Modulus_Actual


    def nw_kyst(self):
        GenerateKeys()
        self.Privato_key = Private_Key_Actual
        self.Publuco_key = Public_Key_Actual
        self.Modululo = Modulus_Actual
        self.key.text = 'The private\nkey will be\n{},{}'.format(self.Privato_key, self.Modululo)


    def update_rect(self, *args):
        self.rect.pos = 0, self.height*.5
        self.rect.size = self.width*1, self.height*.4


    def dismiss_popup(self):
        self._popup.dismiss()


    def encrypt(self):
        self.file_contents = self.inputo.text
        self.file_contents = Ascii(self.file_contents)
        for i in range(len(self.file_contents)):
            self.file_contents[i] = str(Encrypt(self.file_contents[i], self.Publuco_key, self.Modululo))
        self.file_contents = ','.join(self.file_contents)
        self.Ecrypted_File = open('secret.txt', 'w')
        self.Ecrypted_File.write(self.file_contents)
        self.Ecrypted_File.close()
        self.inputo.text = ''

class DecryptionScreen(Screen):

    label_text = StringProperty()

    def SetText(self):
        self.encryptido = open('secret.txt', 'r')
        self.encryptidoo = self.encryptido.read()
        self.encryptido.close()
        self.e = []
        for i in range(len(self.encryptidoo)):
            if (i + 1) % 44 == 0:
                num = self.encryptidoo[i] + '\n'
            else:
                num = self.encryptidoo[i]
            self.e.append(num)
        self.encryptidoo = ''.join(self.e)
        self.label_text = self.encryptidoo



    def private_key_ask(self):
        
        self.private_key = Label(text='What is\nthe private\nkey?',
         color=[130/255, 120/255, 98/255, 1], size_hint=(1, .5), pos_hint={'y':.45},
         font_name='LemonMilk', font_size=50, halign="center")

        with self.private_key.canvas.before:
            Color(218/255, 193/255, 151/255, 1)
            self.rect = Rectangle(size=(self.width*1, self.height*.4), pos=(0, self.height*.5))
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.private_key_input = TextInput(multiline=False, size_hint=(1, .4), pos_hint={'y': .1})

        self.submit = Button(text='Submit', size_hint=(1, .1), 
         font_name='LemonMilk', font_size=65, halign="center")
        self.submit.bind(on_press=self.decrypt)

        self.decryption.add_widget(self.submit)
        self.decryption.add_widget(self.private_key)
        self.decryption.remove_widget(self.select)
        self.decryption.add_widget(self.private_key_input)
    

    def restore(self):
        self.decryption.remove_widget(self.submit)
        self.decryption.remove_widget(self.private_key)
        self.encryptido = open('secret.txt', 'r')
        self.encryptidoo = self.encryptido.read()
        self.encryptido.close()
        self.label_text = self.encryptidoo
        self.decryption.remove_widget(self.private_key_input)
        self.decryption.add_widget(self.select)


    def decrypt(self, instance):
        self.privato_key = self.private_key_input.text
        self.privato_key = self.privato_key.split(',')
        for i in range(len(self.file_contents)):
            self.file_contents[i] = Encrypt(int(self.file_contents[i]), int(self.privato_key[0]), int(self.privato_key[1]))
        self.file_contents = Character(self.file_contents)
        self.file_contents = ''.join(self.file_contents)
        self.Decrypted_File = open('secret.txt', 'w')
        self.Decrypted_File.write(self.file_contents)
        self.Decrypted_File.close()
        self.restore()


    def update_rect(self, *args):
        self.rect.pos = 0, self.height*.5
        self.rect.size = self.width*1, self.height*.4


    def load(self):
        self.file_contents = open('secret.txt', 'r')
        self.file_contents = self.file_contents.read()
        self.file_contents = self.file_contents.split(',')

        self.private_key_ask()



class WindowManager(ScreenManager):
    pass


class FileSelector(GridLayout):
    pass


kv = Builder.load_file('Kivy_file.kv')



class MyMainApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    MyMainApp().run()
