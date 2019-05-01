#!/home/positipman/fastcampus/server_basic/venv/bin/python
# 로또 예상 번호 5 게임 출력하기


import random
# 1. 랜덤하게 숫자 뽑아서 채우기
# def get_lotto_num():
#     lotto_li = []
#     for _ in range(6):
#         num = randint(1, 46)
#         while num in lotto_li:
#             num = randint(1, 46)
#         lotto_li.append(num)
#     lotto_li.sort()
#     return lotto_li
#
#
# dic = {}
# for i in range(5):
#     dic[chr(i+65)] = get_lotto_num()
#
# for i in range(5):
#     print(chr(i+65), end=' ')
#     for j in range(6):
#         print(dic[chr(i+65)][j], end=' ')
#     print()

# list 대신 set 사용
numbers = set()
while len(numbers) < 6:
    number = random.randint(1, 45)
    numbers.add(number)

# 2. 원본은 만들어 두고 랜덤하게 몇개 뽑는 방법
original_numbers = [x for x in range(1, 46)]

numbers = random.sample(original_numbers, 6)

random.shuffle(original_numbers)

numbers = original_numbers[:6] # 혹은 original_numbers[-6:]

numbers.sort()

print("content-type: text/html\n")
print("<html><head><title>CGI 테스트2</title></head><body>"+str(numbers)+"</body></html>")