import random
from functools import reduce
from typing import List, Dict, Callable

# 1. Звичайні функції
def calculate_kda(kills: int, deaths: int, assists: int) -> float:
    """Розраховує KDA (Kills, Deaths, Assists)."""
    if deaths == 0:
        return float(kills + assists)
    return (kills + assists) / deaths

def print_match_info(match: Dict) -> None:
    """Виводить інформацію про один матч."""
    status = "Перемога" if match['win'] else "Поразка"
    print(f"ID: {match['match_id']} | Герой: {match['hero']:<14} | "
          f"KDA: {match['kills']:>2}/{match['deaths']:>2}/{match['assists']:>2} | "
          f"Тривалість: {match['duration']} хв | {status}")

# 2. Функція з параметром за замовчуванням
def filter_by_hero(matches: List[Dict], hero: str = "Pudge") -> List[Dict]:
    """Фільтрує матчі за певним героєм (за замовчуванням Pudge)."""
    return [m for m in matches if m['hero'] == hero]

# 3. Функція зі змінною кількістю аргументів (*args)
def average_duration(*durations: int) -> float:
    """Обчислює середню тривалість довільної кількості матчів."""
    if not durations: return 0.0
    return sum(durations) / len(durations)

# 4. Лямбда-функції
# Лямбда для визначення, чи матч виграний
is_win = lambda match: match['win'] == True
# Лямбда для підрахунку загального відсотка перемог
winrate_calc = lambda wins, total: (wins / total) * 100 if total > 0 else 0.0

# 5. Рекурсивна функція
def find_max_kills_recursive(matches: List[Dict], start: int, end: int) -> int:
    """Рекурсивно знаходить максимальну кількість вбивств у масиві матчів."""
    if start == end:
        return matches[start]['kills']
    
    mid = (start + end) // 2
    left_max = find_max_kills_recursive(matches, start, mid)
    right_max = find_max_kills_recursive(matches, mid + 1, end)
    
    return max(left_max, right_max)

# 6. Функція вищого порядку
def apply_metric_to_matches(matches: List[Dict], metric_func: Callable[[Dict], float]) -> List[float]:
    """Застосовує передану функцію-метрику до всіх матчів."""
    return [metric_func(m) for m in matches]

# Генерація набору даних (мінімум 20 елементів)
def generate_dota_matches(count: int = 20) -> List[Dict]:
    heroes = ["Pudge", "Juggernaut", "Invoker", "Crystal Maiden", "Axe", "Sniper", "Anti-Mage"]
    matches = []
    for i in range(1, count + 1):
        matches.append({
            'match_id': 1000 + i,
            'hero': random.choice(heroes),
            'kills': random.randint(0, 25),
            'deaths': random.randint(0, 15),
            'assists': random.randint(0, 30),
            'duration': random.randint(20, 60),
            'win': random.choice([True, False])
        })
    return matches

def main():
    print("=== Аналізатор статистики Dota 2 ===")
    # Створюємо 25 матчів
    match_history = generate_dota_matches(25)
    
    while True:
        print("\nМеню:")
        print("1. Показати всі матчі")
        print("2. Показати тільки переможні матчі (filter)")
        print("3. Розрахувати загальний Winrate (лямбда + reduce)")
        print("4. Знайти рекорд по кіллах (рекурсія)")
        print("5. Розрахувати середню тривалість ігор (*args)")
        print("6. Показати KDA для всіх матчів (функція вищого порядку)")
        print("7. Вийти")
        
        try:
            choice = int(input("\nВаш вибір: "))
            
            if choice == 1:
                print("\nІсторія матчів:")
                for match in match_history:
                    print_match_info(match)
                    
            elif choice == 2:
                # Використання filter
                won_matches = list(filter(is_win, match_history))
                print(f"\nЗнайдено {len(won_matches)} перемог:")
                for match in won_matches:
                    print_match_info(match)
                    
            elif choice == 3:
                # Використання reduce
                total_wins = reduce(lambda acc, m: acc + (1 if m['win'] else 0), match_history, 0)
                wr = winrate_calc(total_wins, len(match_history))
                print(f"\nЗагальний Winrate: {wr:.1f}% ({total_wins} перемог з {len(match_history)} ігор)")
                
            elif choice == 4:
                # Виклик рекурсії
                max_k = find_max_kills_recursive(match_history, 0, len(match_history) - 1)
                print(f"\nАбсолютний рекорд вбивств за матч: {max_k}")
                
            elif choice == 5:
                # Розпакування списку в *args
                durations = [m['duration'] for m in match_history]
                avg_dur = average_duration(*durations)
                print(f"\nСередня тривалість матчу: {avg_dur:.1f} хвилин")
                
            elif choice == 6:
                # Використання функції вищого порядку
                kda_wrapper = lambda m: calculate_kda(m['kills'], m['deaths'], m['assists'])
                kdas = apply_metric_to_matches(match_history, kda_wrapper)
                print("\nKDA у кожному матчі:")
                for i, kda in enumerate(kdas):
                    print(f"Матч {match_history[i]['match_id']} ({match_history[i]['hero']}): KDA {kda:.2f}")
                    
            elif choice == 7:
                print("ГГ ВП! Вихід з програми.")
                break
                
            else:
                print("Невірний вибір. Введіть число від 1 до 7.")
                
        except ValueError:
            print("Помилка: введіть коректне число.")

if __name__ == "__main__":
    main()