import requests

url = "http://127.0.0.1:5000/predict"
image_path = r"C:\Users\kira\Desktop\code\new_captcha\captcha_images_v2\captcha_images_v2\2b827.png"

# Открываем файл и отправляем запрос
with open(image_path, "rb") as image_file:
    files = {"image": image_file}
    response = requests.post(url, files=files)

# Выводим результат
print(response.json())
