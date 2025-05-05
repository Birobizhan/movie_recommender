from environs import Env
from openai import OpenAI
import time
import re
from openai.types.chat import ChatCompletion
from typing import Callable, TypeVar

# Аннотация типа для возвращаемого значения функции
T = TypeVar('T')


class Retry:
    def __init__(self, max_retries: int):
        if max_retries < 1:
            raise ValueError("Количество попыток должно быть не меньше 1.")
        self.max_retries = max_retries

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            for attempt in range(self.max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Попытка {attempt + 1} из {self.max_retries} завершилась с ошибкой: {e}")
            raise Exception(f"Все {self.max_retries} попыток завершились ошибкой")
        return wrapper


class prompter:
    def __init__(self, client: OpenAI):
        self.client = client

    def prompt(self, user_query: str) -> ChatCompletion:
        response = self.client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[{"role": "user", "content": user_query}]
        )
        return response


def swap_title(title_film: str) -> str:
    with open('prompt1.txt', 'r', encoding='utf-8') as file_prompt_read:
        content = file_prompt_read.readlines()
        part = content[0].split(': ')
        part = [part[0], ' '.join(part[1:])]
        part[1] = f': {title_film}'
        content[0] = ''.join(part)
    with open('prompt1.txt', 'w', encoding='utf-8') as file_prompt_write:
        file_prompt_write.writelines(content)
    return part[1][2:-1].rstrip()


def add_to_csv_file(result, part_title, information) -> bool:
    print(result[0] == part_title)
    if result[0] == part_title:
        with open(f'genre_csv/{result[1]}.csv', 'a', encoding='utf-8') as file_add:
            file_add.write(f"\n{information}")
        with open('count.txt', 'a', encoding='utf-8') as file_add:
            file_add.write(f'{part_title}\n')
        print(part_title, i)
        return True
    else:
        return False


@Retry(max_retries=5)
def process(film) -> list[str]:
    part_title_swap = swap_title(film)
    with open("prompt1.txt", "r", encoding="utf-8") as file_for_prompt:
        request_prompt = file_for_prompt.read()
    answer = client_user.prompt(request_prompt)
    information_ans = answer.choices[0].message.content.split('\n')[1]
    res = re.split(r',(?=\S)', information_ans)
    print(res)
    print(part_title_swap)
    print(information_ans)
    responds = add_to_csv_file(res, part_title_swap, information_ans)
    if responds is False:
        raise ValueError('Не совпадают названия на входе и выходе')
    else:
        return res


env = Env()
env.read_env()
api_key = env("API_KEY")
client_user = prompter(OpenAI(
     base_url="https://openrouter.ai/api/v1",
     api_key=api_key))
with open('right_top1000.txt', 'r', encoding='utf-8') as file:
    films_list = file.readlines()
for i in range(len(films_list)):
    resulting = process(films_list[i])
    print(resulting, i)
    time.sleep(2)
