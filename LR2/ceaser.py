class CaesarCipher:
    def __init__(self, shift):
        self.shift = shift % 26

    def encrypt(self, text):
        return self._transform(text, self.shift)

    def decrypt(self, text):
        return self._transform(text, -self.shift)

    def _transform(self, text, shift):
        result = ""
        for char in text:
            if char.isalpha():
                new_char = chr(((ord(char.lower()) - ord('a') + shift) % 26) + ord('a'))
                if char.isupper():
                    new_char = new_char.upper()
                result += new_char
            else:
                result += char
        return result


try:
    shift = int(input("Введите сдвиг: "))
    mode = input("Выберите режим (1 - шифрование, 2 - дешифрование): ")
    file_path = input("Введите путь к файлу для чтения: ")
    
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    
    cipher = CaesarCipher(shift)
    
    if mode == "1":
        result = cipher.encrypt(text)
    elif mode == "2":
        result = cipher.decrypt(text)
    else:
        print("Неверный режим")
        exit()
    
    save_path = input("Введите путь для сохранения результата: ")
    with open(save_path, "w", encoding="utf-8") as file:
        file.write(result)
    
    print("Результат сохранен в файл.")
    
except ValueError as e:
    print("Ошибка ввода:", e)
