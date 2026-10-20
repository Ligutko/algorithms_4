"""Лабораторна робота № 4. Динамічне програмування. Жадібні алгоритми.

Мета (дослівно): набуття практичних вмінь і навичок розробляти жадібні
алгоритми та використовувати принципи динамічного програмування.

Частина I, задача 2 (динамічне програмування), дослівно:
    «Кенгуру хоче перебратися на іншу сторону річки. Він знає, що через
    річку є стежка з n рівновіддалених купин (2 <= n <= 30). Кенгуру може
    стрибати на наступну купину або через одну купину. Визначте максимальну
    кількість маршрутів, якими кенгуру може подолати річку.»

Частина II, задача 2 (жадібний алгоритм), дослівно:
    «Є k (k <= 100) куп піску з дорогоцінних каменів. Купи мають ваги (у
    кілограмах) m1, m2, ..., mk (1 <= mi <= 100) та вартості (у гривнях)
    одиниці піску v1, v2, ..., vk (1 <= vi <= 1000) відповідно. У Вас є
    рюкзак, що може вмістити n кілограмів ваги. Визначте, як заповнити
    рюкзак піском із цих куп так, щоб вартість піску виявилася максимальною.
    Примітка: для спрощення вважайте, що Ви можете покласти до рюкзака
    будь-яку вагу піску, іншими словами не у дискретних значеннях (тобто
    кратну чомусь), а безперервну.»

Варіант 2. Виконав: студент групи СА-24б Лігутко А.А.
"""
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

N_MIN, N_MAX = 2, 30       # обмеження з умови: 2 <= n <= 30 купин


# ───────────────────────── Частина I. Кенгуру ─────────────────────────
#
# Модель. Позиції: 0 - берег, з якого стартує кенгуру; 1..n - купини;
# n+1 - протилежний берег. З позиції i кенгуру стрибає в i+1 або в i+2.
# shliakhy(i) - кількість різних маршрутів з позиції 0 у позицію i.
# В i можна потрапити лише з i-1 або з i-2, тому
#     shliakhy(i) = shliakhy(i-1) + shliakhy(i-2),   i >= 2,
# а базові значення задаються окремо: shliakhy(0) = 1 (порожній маршрут),
# shliakhy(1) = 1 (єдиний шлях: стрибок з 0 в 1). Це послідовність
# Фібоначчі зі зсувом: shliakhy(i) = F(i+1), де F(1) = F(2) = 1.
#
# Відповідь на задачу - маршрути з берега на протилежний берег, тобто
# shliakhy(n + 1). Маршрути, що закінчуються на останній купині, - це
# shliakhy(n); вони показані окремо для порівняння.

def shliakhy_rekursiya(i, lichylnyk):
    """Пряма рекурсія без запам'ятовування. lichylnyk[0] - кількість викликів."""
    lichylnyk[0] += 1
    if i <= 1:
        return 1
    return shliakhy_rekursiya(i - 1, lichylnyk) + shliakhy_rekursiya(i - 2, lichylnyk)


def shliakhy_memo(i, memo, lichylnyk):
    """Рекурсія із запам'ятовуванням: кожне значення рахується один раз."""
    lichylnyk[0] += 1
    if i <= 1:
        return 1
    if i not in memo:
        memo[i] = (shliakhy_memo(i - 1, memo, lichylnyk)
                   + shliakhy_memo(i - 2, memo, lichylnyk))
    return memo[i]


def perevirka_n(n):
    """Перевіряє обмеження з умови: 2 <= n <= 30."""
    if not isinstance(n, int) or not N_MIN <= n <= N_MAX:
        raise ValueError(f'кількість купин n має бути цілим від {N_MIN} до {N_MAX}')


def shliakhy_tablytsia(n):
    """Цикл знизу вгору: масив a[0..n+1]; a[i] = a[i-1] + a[i-2]."""
    perevirka_n(n)
    a = [0] * (n + 2)
    a[0] = a[1] = 1
    for i in range(2, n + 2):
        a[i] = a[i - 1] + a[i - 2]
    return a


def vsi_marshruty(n):
    """Усі маршрути перебором (для перевірки на малих n): список послідовностей
    позицій від 0 до n+1."""
    kinets = n + 1
    rezultat = []

    def dfs(poz, shliakh):
        if poz == kinets:
            rezultat.append(shliakh)
            return
        for krok in (1, 2):
            if poz + krok <= kinets:
                dfs(poz + krok, shliakh + [poz + krok])

    dfs(0, [0])
    return rezultat


def _pokaz_marshrut(shliakh, n):
    nazva = {0: 'бер', n + 1: 'бер'}
    return ' -> '.join(nazva.get(p, str(p)) for p in shliakh)


def print_kenguru():
    print('ЧАСТИНА I, ЗАДАЧА 2. КЕНГУРУ (динамічне програмування)')
    print()
    print('Рекурентне співвідношення: a[i] = a[i-1] + a[i-2], i >= 2;')
    print('базові значення: a[0] = 1, a[1] = 1. Позиція 0 - початковий берег,')
    print('1..n - купини, n+1 - протилежний берег.')
    print()

    print('1. Перевірка співвідношення перебором усіх маршрутів, n = 3 купини')
    marshruty = vsi_marshruty(3)
    for k, m in enumerate(marshruty, 1):
        print(f'   маршрут {k}: {_pokaz_marshrut(m, 3)}')
    a3 = shliakhy_tablytsia(3)
    print(f'   перебір знайшов {len(marshruty)} маршрутів; '
          f'формула a[n+1] = a[4] = {a3[4]}')
    print()

    print('2. Результати для кількох довільних n (таблиця / рекурсія / '
          'перебір збігаються)')
    print('     n   a[n+1] (через річку)   a[n] (до останньої купини)   перебір')
    for n in (2, 3, 5, 10, 20, 30):
        a = shliakhy_tablytsia(n)
        memo, lm = {}, [0]
        r_memo = shliakhy_memo(n + 1, memo, lm)
        pereb = len(vsi_marshruty(n)) if n <= 20 else None
        zbih = '-' if pereb is None else ('так' if pereb == a[n + 1] else 'НІ')
        assert r_memo == a[n + 1]
        print(f'   {n:>3}   {a[n + 1]:>20}   {a[n]:>26}   {zbih:>7}')
    print()

    print('3. Ціна запам\'ятовування: кількість викликів функції, n = 30')
    lr, lm, memo = [0], [0], {}
    r1 = shliakhy_rekursiya(31, lr)
    r2 = shliakhy_memo(31, memo, lm)
    print(f'   пряма рекурсія:      {lr[0]:>10} викликів, відповідь {r1}')
    print(f'   з запам\'ятовуванням: {lm[0]:>10} викликів, відповідь {r2}')
    print(f'   різниця: у {lr[0] // lm[0]} разів менше викликів')
    print()

    print('4. Перевірка вхідного обмеження 2 <= n <= 30')
    for n in (1, 31, 2.5):
        try:
            shliakhy_tablytsia(n)
            print(f'   n = {n}: ПРИЙНЯТО (помилка перевірки)')
        except ValueError as e:
            print(f'   n = {n}: відхилено - {e}')


# ───────────────────────── Частина II. Пісок ─────────────────────────
#
# Модель. Купа i має масу m[i] кг і ціну v[i] грн за 1 кг. Рюкзак вміщує n кг.
# Пісок ділиться на довільні частини, тому x[i] - скільки кг з купи i беремо,
# 0 <= x[i] <= m[i]; потрібно: максимізувати sum(x[i] * v[i]) за умови
# sum(x[i]) <= n.
#
# Жадібний вибір: брати спершу пісок з найбільшою ціною за кілограм. Купу
# беруть повністю, поки вона вміщується; першу купу, що не вміщується,
# беруть частково (скільки лишилось місця), після чого рюкзак повний.
# Це оптимально, бо будь-який кілограм дешевшого піску, взятий замість
# кілограма дорожчого, лише зменшує суму. Час: O(k log k) (сортування).

K_MAX, M_MIN, M_MAX, V_MIN, V_MAX = 100, 1, 100, 1, 1000


def perevirka_vkhodu(kupy, n):
    """Перевіряє обмеження з умови: k <= 100, 1 <= m <= 100, 1 <= v <= 1000, n > 0."""
    if not 1 <= len(kupy) <= K_MAX:
        raise ValueError(f'кількість куп k має бути від 1 до {K_MAX}')
    for m, v in kupy:
        if not M_MIN <= m <= M_MAX:
            raise ValueError(f'маса купи {m} поза межами {M_MIN}..{M_MAX}')
        if not V_MIN <= v <= V_MAX:
            raise ValueError(f'ціна за кг {v} поза межами {V_MIN}..{V_MAX}')
    if n <= 0:
        raise ValueError('місткість рюкзака n має бути додатною')


def pisok_zhadibnyj(kupy, n):
    """Жадібний алгоритм. kupy - список пар (маса, ціна за кг).

    Повертає (вартість, взято, кроки): взято[i] - кг з купи i (в початковому
    порядку), кроки - протокол для друку."""
    perevirka_vkhodu(kupy, n)
    poriadok = sorted(range(len(kupy)), key=lambda i: -kupy[i][1])
    vzyato = [0] * len(kupy)
    lyshylos = n
    vartist = 0
    kroky = []
    for i in poriadok:
        if lyshylos <= 0:
            break
        m, v = kupy[i]
        x = min(m, lyshylos)
        vzyato[i] = x
        lyshylos -= x
        vartist += x * v
        kroky.append((i + 1, m, v, x, lyshylos, x * v))
    return vartist, vzyato, kroky


def _pokaz_kroky(kroky):
    print('   крок  купа  маса, кг  ціна/кг  взято, кг  лишилось місця  внесок, грн')
    for k, (nomer, m, v, x, lysh, vn) in enumerate(kroky, 1):
        print(f'   {k:>4}  {nomer:>4}  {m:>8}  {v:>7}  {x:>9}  {lysh:>14}  {vn:>11}')


def tochnyj_rozviazok_lp(kupy, n):
    """Незалежна перевірка: та сама задача як лінійна програма (scipy)."""
    from scipy.optimize import linprog
    c = [-v for _, v in kupy]
    r = linprog(c, A_ub=[[1] * len(kupy)], b_ub=[n],
                bounds=[(0, m) for m, _ in kupy], method='highs')
    return -r.fun


def rjukzak_dp(predmety, w):
    """Дискретний рюкзак 0/1 (динамічне програмування): predmety - (маса, вартість),
    K[i][j] - найбільша вартість з перших i предметів при місткості j."""
    nn = len(predmety)
    K = [[0] * (w + 1) for _ in range(nn + 1)]
    for i in range(1, nn + 1):
        m, c = predmety[i - 1]
        for j in range(w + 1):
            K[i][j] = K[i - 1][j]
            if m <= j and K[i - 1][j - m] + c > K[i][j]:
                K[i][j] = K[i - 1][j - m] + c
    return K[nn][w]


def rjukzak_zhadibnyj_0_1(predmety, w):
    """Жадібний за ціною на одиницю ваги для неподільних предметів: бере
    предмет цілим, якщо він ще вміщується."""
    vartist, lyshylos = 0, w
    for m, c in sorted(predmety, key=lambda p: -p[1] / p[0]):
        if m <= lyshylos:
            vartist += c
            lyshylos -= m
    return vartist


def rjukzak_dribnyj(predmety, w):
    """Той самий набір, але предмети можна ділити (пісок): жадібний."""
    vartist, lyshylos = 0.0, w
    for m, c in sorted(predmety, key=lambda p: -p[1] / p[0]):
        chastka = min(m, lyshylos)
        vartist += c * chastka / m
        lyshylos -= chastka
    return vartist


def print_pisok():
    import random
    print('ЧАСТИНА II, ЗАДАЧА 2. ПІСОК (жадібний алгоритм)')
    print()
    print('Алгоритм: відсортувати купи за ціною за кг від більшої до меншої;')
    print('брати купи повністю, поки вміщується; останню - частково.')
    print()

    pryklady = [
        ('1. Рюкзак 50 кг, три купи', [(20, 5), (30, 9), (40, 7)], 50),
        ('2. Рюкзак більший за весь пісок (60 кг, але піску 45)',
         [(10, 100), (15, 40), (20, 250)], 60),
        ('3. Рівні ціни (результат не залежить від порядку), рюкзак 25 кг',
         [(10, 8), (20, 8), (30, 8)], 25),
        ('4. Дорога купа більша за рюкзак, рюкзак 15 кг',
         [(100, 900), (5, 1000), (50, 10)], 15),
    ]
    for nazva, kupy, n in pryklady:
        vartist, vzyato, kroky = pisok_zhadibnyj(kupy, n)
        print(nazva)
        print(f'   купи (маса, ціна/кг): {kupy}')
        _pokaz_kroky(kroky)
        print(f'   взято по купах, кг: {vzyato}; усього {sum(vzyato)} кг; '
              f'ВАРТІСТЬ = {vartist} грн')
        print()

    print('5. Перевірка вхідних обмежень з умови (некоректні дані відхиляються)')
    nekorektni = [
        ('k = 101 куп', [(1, 1)] * 101, 10),
        ('маса купи 0', [(0, 5)], 10),
        ('ціна за кг 1001', [(5, 1001)], 10),
        ('місткість рюкзака 0', [(5, 5)], 0),
    ]
    for opys, kupy, n in nekorektni:
        try:
            pisok_zhadibnyj(kupy, n)
            print(f'   {opys}: ПРИЙНЯТО (помилка перевірки)')
        except ValueError as e:
            print(f'   {opys}: відхилено - {e}')
    print()
    print('6. Перевірка оптимальності: 1000 випадкових задач у межах умови '
          '(k <= 100, m <= 100, v <= 1000) проти точного розв\'язку (лінійна '
          'програма)')
    random.seed(2)
    rozbizhnosti, maks_k = 0, 0
    for _ in range(1000):
        k = random.randint(1, 100)
        kupy = [(random.randint(M_MIN, M_MAX), random.randint(V_MIN, V_MAX))
                for _ in range(k)]
        n = random.randint(1, sum(m for m, _ in kupy))
        z, _, _ = pisok_zhadibnyj(kupy, n)
        if abs(z - tochnyj_rozviazok_lp(kupy, n)) > 1e-6:
            rozbizhnosti += 1
        maks_k = max(maks_k, k)
    print(f'   розбіжностей з точним розв\'язком: {rozbizhnosti} з 1000 '
          f'(найбільше k у тесті: {maks_k})')
    print()
    print('7. Контрприклад: ті самі предмети, але НЕПОДІЛЬНІ (злитки), '
          'рюкзак 50 кг')
    predmety = [(10, 60), (20, 100), (30, 120)]
    print(f'   предмети (маса, вартість): {predmety}; ціна за кг: 6, 5, 4')
    zh = rjukzak_zhadibnyj_0_1(predmety, 50)
    dp = rjukzak_dp(predmety, 50)
    dr = rjukzak_dribnyj(predmety, 50)
    print(f'   жадібний, предмети цілі:        {zh}')
    print(f'   динамічне програмування (0/1):  {dp}   <- оптимум для злитків')
    print(f'   жадібний, предмети діляться:    {dr:g}   <- оптимум для піску')
    print()
    print('8. Як часто жадібний помиляється на неподільних предметах: '
          '1000 випадкових наборів (до 8 предметів, маса 1..40, вартість '
          '1..100, місткість 10..100)')
    random.seed(2)
    pomylok, maks_vtrata = 0, 0
    for _ in range(1000):
        pr = [(random.randint(1, 40), random.randint(1, 100))
              for _ in range(random.randint(2, 8))]
        w = random.randint(10, 100)
        a, b = rjukzak_zhadibnyj_0_1(pr, w), rjukzak_dp(pr, w)
        if a < b:
            pomylok += 1
            maks_vtrata = max(maks_vtrata, b - a)
    print(f'   жадібний не знайшов оптимум у {pomylok} з 1000 наборів; '
          f'найбільша втрата {maks_vtrata}')


def print_usi():
    print_kenguru()
    print()
    print('=' * 72)
    print()
    print_pisok()


if __name__ == '__main__':
    argv = sys.argv[1:]
    if argv == ['kenguru']:
        print_kenguru()
    elif argv == ['pisok']:
        print_pisok()
    else:
        print_usi()
