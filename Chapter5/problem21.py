with open('input.txt', encoding='utf8') as f:
    n = int(f.readline().strip())
    coins = [int(x) for x in f.readline().strip().split(',')]
    min_coins = []
    for i in range(n+1):
        def get_min():
            res = [min_coins[i - coin] + 1 for coin in coins if i - coin >= 0]
            return min(res) if len(res) > 0 else 0
        min_coins.append(get_min())
    print(min_coins[-1])