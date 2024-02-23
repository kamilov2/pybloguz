# import random
# import string

# def generate_password(length=12):
#     characters = string.ascii_letters + string.digits + string.punctuation
#     password = ''.join(random.choice(characters) for i in range(length))
#     return password

# if __name__ == "__main__":
#     password_length = int(input("Введите длину пароля: "))
#     password = generate_password(password_length)
#     print("Сгенерированный пароль:", password)


# from collections import Counter
# import re

# def most_common_words(text, num_words=5):
#     words = re.findall(r'\b\w+\b', text.lower())
#     word_counts = Counter(words)
#     return word_counts.most_common(num_words)

# if __name__ == "__main__":
#     text = input("Введите текст: ")
#     num_words = int(input("Введите количество самых часто встречающихся слов: "))

#     common_words = most_common_words(text, num_words)
#     print(f"Самые часто встречающиеся слова ({num_words}):")
#     for word, count in common_words:
#         print(f"{word}: {count}")




# import requests
# from PIL import Image
# from io import BytesIO
# import pytesseract

# def recognize_text_from_url(image_url):
#     response = requests.get(image_url)
#     img = Image.open(BytesIO(response.content))
#     text = pytesseract.image_to_string(img)
#     return text

# if __name__ == "__main__":
#     image_url = "https://cdn.beta.qalampir.uz/uploads/UI/f_hBzVNnKRFOK7TCuNYcfXzfN7NxKIif.jpg"
#     recognized_text = recognize_text_from_url(image_url)
#     print("Распознанный текст:")
#     print(recognized_text)

