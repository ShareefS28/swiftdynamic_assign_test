"""
เขียบนโปรแกรมหาจำนวนเลข 0 ที่ออยู่ติดกันหลังสุดของค่า factorial โดยห้ามใช้ function from math

[Input]
number: as an integer

[Output]
count: count of tailing zero as an integer

[Example 1]
input = 7
output = 1

[Example 2]
input = -10
output = number can not be negative
"""

"""
ลงท้ายศูนย์เกิดจากคูณ 10 แยกตัวประกอบ --> 2 x 5 = 10
"""
class Solution:

    def find_tailing_zeroes(self, number: int) -> int | str:
        if number < 0:
            return "factorial ค่าที่ใช้ต้องไม่น้อยกว่า 0"

        count = 0

        while number > 0:
            number //= 5
            count += number

        return count

answer = Solution()
print(answer.find_tailing_zeroes(7))
print(answer.find_tailing_zeroes(-10))
