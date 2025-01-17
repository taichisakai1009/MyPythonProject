'''
Created on 2025/01/14

@author: Anali
'''
from sympy import symbols, Rational, divisors, isprime, gcd, bernoulli, binomial, mod_inverse, factorint
import pickle

# シンボルの作成
x, a, b, c, m = symbols('x a b c m')

import time

# mは偶数 aとbは互いに素
# faulhaber_cache = {}  # m 乗和の公式を作ったら保存する辞書


# 辞書の内容をファイルに保存する関数
def save_dict_to_file(filename, data):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


# ファイルから辞書の内容を読み込む関数
def load_dict_from_file(filename):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}


# m 乗和の公式を出力。辞書になかったら一から作る。
def createFaulhaber(m):
        formura = sum(Rational(binomial(m + 1, k), m + 1) * bernoulli(k) * x ** (m + 1 - k) for k in range(0, (m + 1)))
        print(m, "乗和の公式作成")
        return formura


# S_m(x)の値を計算
def S(m, value):
    # キャッシュファイルの名前
    cache_file = "faulhaber_cache.pickle"
    # キャッシュを読み込む
    faulhaber_cache = load_dict_from_file(cache_file)
    if m in faulhaber_cache:
        # print(f"{m} 乗和の公式はキャッシュから読み込みました")
        formula = faulhaber_cache[m] 
    else:
        formula = createFaulhaber(m)
        faulhaber_cache[m] = formula
        save_dict_to_file(cache_file, faulhaber_cache)
        
    return formula.subs(x, value)

S(1,1)


# mの約数のうち、+1したら素数になるリストを返す
def bernoulliDenominator(m):
    denominatorList = [d + 1 for d in divisors(m) if isprime(d + 1)]
    return denominatorList


# bernoulliDenominatorのうち、x の約数を返す
def sumRange(m, x):
    return [p for p in bernoulliDenominator(m) if p in divisors(x)]


# 合同式の左辺を算出する
def calculateLeft(m, a, b, c):
    baseNumber = a - b * c
    if(abs(baseNumber) == 1):  # mod 1 のときは逆元を指定できないらしい
        N = 1
    else: 
        actualS = S(m, Rational(a, b))  # S_m(a/b) の厳密な値
        numerator = actualS.as_numer_denom()[0]  # 分子
        denominator = actualS.as_numer_denom()[1]  # 分母    
        inverse = mod_inverse(denominator, baseNumber)  # 逆数の剰余を計算   
        N = numerator * inverse % baseNumber
    
    left = a * S(m, c) - b * c * N  # 左辺  
    return left  


# 合同式の右辺を算出する
def calculateRight(m, a, b, c):
    baseNumber = a - b * c
    mod = c * (a - b * c)
    first_sum = sum(Rational(mod, p) for p in sumRange(m, baseNumber))
    second_sum = sum(Rational(mod, p) for p in sumRange(m, c))
    right = first_sum - second_sum
    return right


# 合同式の検証を行います。理論上はmが偶数なら成り立ちます。
def checker(m, a, b, c):
    
    baseNumber = a - b * c  # a - b c
    mod = c * baseNumber
    print("a=", a, " b=", b, " c=", c)
    print("mod", abs(mod))
    
    checkNum = calculateLeft(m, a, b, c) - calculateRight(m, a, b, c)
    modular = checkNum % mod
    
    if modular == 0:
        print("合同式は成り立ちます。")
        return True
    else:
        print("合同式は成り立ちません。mod=", modular)  
        return False 


# 指定されたm,a,b に対し、c の値を-n からn-1まで試します。
def allChecker(m, a, b , n):
    for k in range(-n, n):
        if k != 0:
            if not checker(m, a, b, k):
                print("合同式はc=", k, "で成り立ちませんでした。")
                return False
    print("合同式は成り立っています。")
    return True

# allChecker(3, 14, 43, 100)


# S_m(a/b) = 0 とした場合に、合同式が成り立たないことを示します。
# 理論上はaが素因数を持っていれば合同式は成り立ちません。        
def ProofNotZero (m, a, b):  # S_m(a/b) に 対して c を算出
    if gcd(a, b) != 1 or a == 0:
        print("a,b は互いに素,かつ a≠0 としてください")
        return False
    else:
        if abs(a) != 1: 
            factors = factorint(a)
            p = next(iter(factors))  # a の素因数を一つ取得
            j = factors.get(p)  # p の数を取得
            k = factorint(S(m, p ** j)).get(p, 0)  # S_m(p^j)の素因数pの個数
            inverseB = mod_inverse(b, p ** (k + 1))  # +1 という一番厳しい値を取っている
            subC = Rational(a, p ** j) * inverseB 
            c = subC * p ** j  # 理論上の c の設定
            print("c = ", c)
            mod = c * (a - b * c)
            NotInteger = Rational(a * S(m, c) - calculateRight(m, a, b, c), mod)
            denominator = NotInteger.as_numer_denom()[1]  # 分母  
            if denominator == 1: 
                print("NotInteger が整数になっています。cの設定を見直してください。")
                return False
            else:
                # print("NotInteger = ", NotInteger)
                print("S _", m, "(", a, "/", b, ") ≠ 0")
                return True               
        else:
            print("a = ± 1")
            return False


# a-bc=0 になる例はそもそも合同式の範囲外なのでb=1とかは避ける
def test_proofZero(m):
    for a in range(-100, 100):
        if abs(a) != 1 and a != 0:
            for b in range(-100, 100):
                if gcd(a, b) == 1 and b != 1:
                    if not ProofNotZero(m, a, b):
                        print("m=", m, "a=", a, "b=", b, "で検証が失敗しました。")
                        return False
    print("検証が成功しました。")
    return True
                         
# test_proofZero(36) 


# j が p　の倍数でない時に、 S_m(p^k) と S_m(jp^k) のpの素因数の数に変化がないか判定します。
# これは ProofNotZero () メソッドで c の値を決める根拠にもなっています。
# すぐに処理が重くなって余り使えない          
def defindC (m, p, k, n):
    baseNum = factorint(S(m, p ** k)).get(p, 0)
    for j in range(-n, n):
        if p not in divisors(j) and j != 0:
            Num = factorint(S(m, j * p ** k)).get(p, 0)
            checker = Num - baseNum 
            print("checker=", checker)
            if checker != 0:
                print("指数の増減:", checker)
                print("m=", m, "p=", p, "k=", k, "j=", j)
                return False
    print("指数の数に変化なし")
    print("m=", m, "p=", p, "k=", k, "j=", -n, "～", n - 1)
    return True


# 結果、すべてTrueが返されました               
def test_defindC():
    for m in range(2, 10):
        for p in [2, 3, 5, 7, 11]:
            for k in range(1, 10):
                if not defindC(m, p, k, 10):
                    print("m={m},p={p},k={k}")
                    return False
    print("すべてTrueが返されました。")
    return True

# test_defindC()


# S_m(P^k) の素因数の数を実際に出力 kは1からjまで
def countP (m, p, j):
    for l in range(1, j + 1):
        start_time = time.time()
        Num = factorint(S(m, p ** l)).get(p, 0)
        end_time = time.time()
        print("S_", m, "(", p, "^", l, ")→", Num,)
        print("処理時間：", end_time - start_time)
    print("出力終了")

# countP(14, 5 , 10)

# S_M(p) のpの個数をmごとに出力
def countFirstP (p, j):
    for k in range(1, j + 1):
        Num = factorint(S(k, p)).get(p, 0)
        print("S_", k, "(", p, ")→", Num,)
    print("出力終了")
        
# countFirstP (7, 100)
# import time
#
# def timed_S(m, x):
#     start = time.time()
#     result = S(m, x)
#     end = time.time()
#     print(f"S(m={m}, x={x}) took {end - start:.5f} seconds")
#     return result
#
# timed_S(10, 100)
# timed_S(10, 100)
# timed_S(10, 101)
