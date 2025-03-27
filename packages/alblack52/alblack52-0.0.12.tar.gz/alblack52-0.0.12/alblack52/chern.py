import requests

API_URL = "https://api.deepinfra.com/v1/openai/chat/completions"
API_TOKEN = 'jwt:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnaDoxNzIxOTMyNzUiLCJleHAiOjE3NDU2NTM5NDN9.HMGghGZ6DsdpRmQaOhaQ-iPhWgrJk_Nt77gvAMF067Y'

# fjkbsfbkjsbdfs

def ask_phind(messages):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-ai/DeepSeek-R1",
        "messages": messages
    }
    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        response_json = response.json()

        try:
            return response_json["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            return "Error: Unable to extract response content. Please check the response structure."
    else:
        return f"Error: {response.status_code}, {response.text}"


def chat_with_phind():
    conversation_history = [
        {"role": "system", "content": '''
        Ты — эксперт в численных методах. Отвечай только кодом и конкретным решением, без лишних пояснений и обобщений.

Темы:
1. Работа с числами с плавающей точкой: переполнение, потеря точности, ошибки округления, накопление ошибок, потеря значимости. Пример: суммирование по Кахану.
2. Методы численного решения нелинейных уравнений, включая метод дихотомии (бисекции).
3. Методы численного решения систем нелинейных уравнений.
4. Интерполяция: линейная интерполяция и кубическая сплайн-интерполяция.

Примеры заданий:
- Задание 1: Реализуй две функции на Python (с использованием numpy) для суммирования массива платежей (10**6 элементов по 0.01) — обычным способом и по Кахану. Выведи оба результата и кратко сравни их.
- Задание 2: Напиши функцию, реализующую метод бисекции для нахождения x, при котором 50x - 0.5x**2 = 10x + 100 с точностью 0.1. Кратко опиши преимущества и недостатки метода.
- Задание 3: Напиши функцию для линейной интерполяции по точкам (0,15), (1,18), (2,22), (3,25) и найди значение при t=1.5. Кратко объясни разницу между линейной интерполяцией и кубическим сплайном.

Используй только основные библиотеки Python (numpy, matplotlib). В ответе приводи только конкретный код и окончательный результат решения, а так же достаточный ответ на теоретический вопрос.
'''},

    ]

    while True:
        question = input("You: ")
        if question.lower() == 'exit':
            print("Goodbye!")
            break

        conversation_history.append({"role": "user", "content": question})

        answer = ask_phind(conversation_history)

        conversation_history.append({"role": "assistant", "content": answer})

        print("Вика: " + answer)


def start():
    chat_with_phind()


if __name__ == "__main__":
    chat_with_phind()
