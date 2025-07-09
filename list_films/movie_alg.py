import pandas as pd
import csv
import os
import numpy as np

# Ожидаемое количество столбцов во всех CSV
EXPECTED_COLUMNS = 6

def fix_row(row):
    """Объединяет первые столбцы, пока не получится EXPECTED_COLUMNS столбцов"""
    if len(row) <= EXPECTED_COLUMNS:
        return row
    extra_columns = len(row) - EXPECTED_COLUMNS + 1
    fixed_row = [",".join(row[:extra_columns])]
    fixed_row.extend(row[extra_columns:])
    return fixed_row

def load_genre_data(file_path):
    """Загружает данные жанра с обработкой запятых в названиях"""
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            
            # Обрабатываем заголовок
            header = next(reader)
            if len(header) > EXPECTED_COLUMNS:
                header = fix_row(header)
            data.append(header)
            
            # Обрабатываем остальные строки
            for row in reader:
                if len(row) > EXPECTED_COLUMNS:
                    row = fix_row(row)
                elif len(row) < EXPECTED_COLUMNS:
                    # Дополняем недостающие колонки
                    row += [''] * (EXPECTED_COLUMNS - len(row))
                data.append(row)
                
    except Exception as e:
        print(f"Ошибка при чтении {file_path}: {e}")
        return None
    
    # Создаем DataFrame
    if len(data) < 2:  # Только заголовок или пусто
        return pd.DataFrame(columns=range(EXPECTED_COLUMNS))
    
    return pd.DataFrame(data[1:], columns=data[0])

def get_top5(df, priority_weights):
    """Возвращает топ-5 фильмов по комбинированной релевантности"""
    if df.empty:
        return []
    
    # Сортируем по релевантности и рейтингу
    df_sorted = df.sort_values(by=['relevance', df.columns[5]], ascending=[False, False])
    return df_sorted.head(5)[df_sorted.columns[0]].tolist()

def recommend_movies(user_input):
    if not user_input or len(user_input) == 0:
        return []
    
    # Определяем жанр и путь к файлу
    genre = user_input[0]
    base_path = r"E:\Movies (csv)"
    file_path = os.path.join(base_path, f"{genre}.csv")
    
    # Загружаем данные с обработкой запятых
    df = load_genre_data(file_path)
    if df is None or df.empty:
        return []
    
    # Проверяем структуру данных
    if len(df.columns) < EXPECTED_COLUMNS:
        return []
    
    # Веса характеристик (чем левее - тем важнее)
    priority_weights = [1000, 100, 10, 1]
    
    # Рассчитываем релевантность для каждой строки
    df['relevance'] = 0
    df['exact_matches'] = 0  # Счетчик полных совпадений
    
    # Для каждой характеристики
    for i in range(1, min(len(user_input) + 1, 5)):
        col_idx = i
        user_val = user_input[i-1]
        
        # Полные совпадения
        exact_match = df[df.columns[col_idx]] == user_val
        df.loc[exact_match, 'relevance'] += priority_weights[i-1]
        df.loc[exact_match, 'exact_matches'] += 1
        
        # Частичные совпадения (только для предыдущих характеристик)
        if i > 1:
            for prev_i in range(i-1):
                prev_col_idx = prev_i + 1
                prev_user_val = user_input[prev_i]
                
                # Частичное совпадение: соответствует предыдущей характеристике, но не текущей
                partial_match = (
                    (df[df.columns[prev_col_idx]] == prev_user_val) &
                    (df[df.columns[col_idx]] != user_val)
                )
                df.loc[partial_match, 'relevance'] += priority_weights[prev_i] * 0.1
    
    # Преобразуем рейтинг к числовому типу
    rating_col = df.columns[5]
    try:
        df[rating_col] = df[rating_col].str.replace(',', '.').astype(float)
    except:
        pass
    
    # Сначала сортируем по количеству полных совпадений, затем по релевантности, затем по рейтингу
    df_sorted = df.sort_values(
        by=['exact_matches', 'relevance', rating_col],
        ascending=[False, False, False]
    )
    
    '''
    # Выводим все фильмы для отладки
    print("\nВсе фильмы, отсортированные по релевантности:")
    print(f"{'Название':<50} | {'Полных совпад.':>14} | {'Релевантность':>12} | {'Рейтинг':>6}")
    print("-" * 90)
    for idx, row in df_sorted.iterrows():
        print(f"{row[df_sorted.columns[0]]:<50} | {row['exact_matches']:>14} | {row['relevance']:>12.1f} | {row[rating_col]:>6}")
    '''

    # Возвращаем топ-5 фильмов
    return df_sorted.head(5)[df_sorted.columns[0]].tolist()

# Пример запроса
user_selection = [
    "Ужасы",
    "Фантастика",
    "Сверхъестественные",
    "Классика (до 2000 года)"
]

# Получаем рекомендации
recommended = recommend_movies(user_selection)
print(recommended)
