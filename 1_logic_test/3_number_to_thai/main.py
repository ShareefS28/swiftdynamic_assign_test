"""
เขียบนโปรแกรมแปลงตัวเลยเป็นคำอ่านภาษาไทย

[Input]
number: positive number rang from 0 to 10_000_000

[Output]
num_text: string of thai number call

[Example 1]
input = 101
output = หนึ่งร้อยเอ็ด

[Example 2]
input = -1
output = number can not less than 0
"""


class Solution:

    def number_to_thai(self, number: int) -> str:
        if number < 0:
            return "number can not less than 0"
        if number > 10_000_000:
            return "number can not greater than 10_000_000"

        digit = [
            "ศุนย์",
            "หนึ่ง",
            "สอง",
            "สาม",
            "สี่",
            "ห้า",
            "หก",
            "เจ็ด",
            "แปด",
            "เก้า",
        ]
            
        if number == 0:
            return digit[0]

        result = ""

        # สิบล้าน
        if number >= 10_000_000:
            return "สิบล้าน"

        # ล้าน
        if number >= 1_000_000:
            result += digit[number // 1000000]
            result += "ล้าน"
            number %= 1000000

        # แสน
        if number >= 100_000:
            result += digit[number // 100000]
            result += "แสน"
            number %= 100000

        # หมื่น
        if number >= 10_000:
            result += digit[number // 10000]
            result += "หมื่น"
            number %= 10000

        # พัน
        if number >= 1000:
            result += digit[number // 1000]
            result += "พัน"
            number %= 1000

        # ร้อย
        if number >= 100:
            result += digit[number // 100]
            result += "ร้อย"
            number %= 100

        # สิบ
        if number >= 10:
            tens = number // 10

            if tens == 1:
                result += "สิบ"
            elif tens == 2:
                result += "ยี่สิบ"
            else:
                result += digit[tens] + "สิบ"

            number %= 10

        # หน่วย
        if number > 0:
            if number == 1 and result:
                result += "เอ็ด"
            else:
                result += digit[number]
        
        return result

answer = Solution()
print(answer.number_to_thai(101))
print(answer.number_to_thai(-1))