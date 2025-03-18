class VigenereCipher:
    def __init__(self, key: str):
        self.key = key

    def _extend_key(self, text: str) -> str:
        key = self.key
        key_extended = ""
        key_index = 0
        
        for char in text:
            if char.isalpha():
                key_extended += key[key_index % len(key)]
                key_index += 1
            else:
                key_extended += char  # Пробелы и другие символы остаются без изменений
                
        return key_extended

    def encrypt(self, text: str) -> str:
        key = self._extend_key(text)
        encrypted_text = ""
        for i in range(len(text)):
            if text[i].isalpha():
                shift = ord(key[i].lower()) - ord('a')
                if text[i].isupper():
                    encrypted_text += chr((ord(text[i]) - ord('A') + shift) % 26 + ord('A'))
                else:
                    encrypted_text += chr((ord(text[i]) - ord('a') + shift) % 26 + ord('a'))
            else:
                encrypted_text += text[i]
        return encrypted_text

    def decrypt(self, text: str) -> str:
        key = self._extend_key(text)
        decrypted_text = ""
        for i in range(len(text)):
            if text[i].isalpha():
                shift = ord(key[i].lower()) - ord('a')
                if text[i].isupper():
                    decrypted_text += chr((ord(text[i]) - ord('A') - shift) % 26 + ord('A'))
                else:
                    decrypted_text += chr((ord(text[i]) - ord('a') - shift) % 26 + ord('a'))
            else:
                decrypted_text += text[i]
        return decrypted_text

key = input("Введите ключ: ")
mode = input("Выберите режим (1 - шифрование, 2 - дешифрование): ")
file_path = input("Введите путь к файлу для чтения: ")

with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()

cipher = VigenereCipher(key)

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
