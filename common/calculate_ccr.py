import datetime
import re


# ccr:内生肌酐清除率 scr：肌酐，根据scr计算ccr（注意肌酐的单位）
# Ccr=(140-年龄)×体重(kg)/72×Scr(mg/dl) 或
# Ccr=[(140-年龄)×体重(kg)]/[0.818×Scr(umol/L)]
# 其中女性按计算结果×0.85
class Ccr:
    def __init__(self,recipe_time_str,birthday_str):
        self.female = {'0M': 3.2,
                       '1M': 4.81,
                       '2M': 5.74,
                       '3M': 6.22,
                       '4M': 7.01,
                       '5M': 7.53,
                       '6M': 8,
                       '8M': 8.65,
                       '10M': 9.09,
                       '12M': 9.52,
                       '15M': 10.09,
                       '18M': 10.65,
                       '21M': 11.25,
                       '2岁': 12.04,
                       '2.5岁': 12.97,
                       '3岁': 14.01,
                       '3.5岁': 14.94,
                       '4岁': 15.81,
                       '4.5岁': 16.8,
                       '5岁': 17.84,
                       '5.5岁': 18.8,
                       '6岁': 20.36,
                       '7岁': 22.32,
                       '8岁': 24.58,
                       '9岁': 27.45,
                       '10岁': 31.11,
                       '11岁': 35.76,
                       '12岁': 40.18,
                       '13岁': 44.45,
                       '14岁': 46.73,
                       '15岁': 48.7,
                       '16岁': 49.97,
                       '17岁': 50.37,
                       '18岁': 50.37}
        self.male = {'0M': 3.3,
                     '1M': 5.1,
                     '2M': 6.16,
                     '3M': 6.74,
                     '4M': 7.56,
                     '5M': 8.02,
                     '6M': 8.62,
                     '8M': 9.19,
                     '10M': 9.65,
                     '12M': 10.16,
                     '15M': 10.7,
                     '18M': 11.25,
                     '21M': 11.83,
                     '2岁': 12.57,
                     '2.5岁': 13.56,
                     '3岁': 14.42,
                     '3.5岁': 15.37,
                     '4岁': 16.23,
                     '4.5岁': 17.24,
                     '5岁': 18.34,
                     '5.5岁': 19.38,
                     '6岁': 20.97,
                     '7岁': 23.35,
                     '8岁': 25.73,
                     '9岁': 28.66,
                     '10岁': 31.88,
                     '11岁': 35.69,
                     '12岁': 39.74,
                     '13岁': 45.96,
                     '14岁': 50.83,
                     '15岁': 54.11,
                     '16岁': 56.8,
                     '17岁': 58.25,
                     '18岁': 58.25}
        self.recipe_time_str = recipe_time_str
        self.birthday_str = birthday_str
        # self.birthday_str = '2019-03-05'   # 3个月
        self.y, self.age = self.calculate_age(self.recipe_time_str, self.birthday_str)

    # 根据出生日期计算年龄
    # 门诊   recipe_time - birthday
    # 住院   run_engine_time（当前时间） - birthday
    def calculate_age(self, recipe_time_str, birthday_str):
        recipe_time = datetime.datetime.strptime(recipe_time_str, '%Y-%m-%d')
        birthday = datetime.datetime.strptime(birthday_str, '%Y-%m-%d')
        y = 0
        age = ''
        if recipe_time.month < birthday.month:
            y = recipe_time.year - birthday.year - 1
            if y == 0:
                if recipe_time.day < birthday.day:
                    age = str(12 - (birthday.month - recipe_time.month) - 1) + 'M'
                else:
                    age = str(12 - (birthday.month - recipe_time.month)) + 'M'
            else:
                age = str(y) + '岁'
        if recipe_time.month > birthday.month:
            y = recipe_time.year - birthday.year
            if y == 0:
                if recipe_time.day < birthday.day:
                    age = str(recipe_time.month - birthday.month -1) + 'M'
                else:
                    age = str(recipe_time.month - birthday.month) + 'M'
            else:
                age = str(y) + '岁'
        if recipe_time.month == birthday.month and recipe_time.day < birthday.day:
            y = recipe_time.year - birthday.year - 1
            if y == 0:
                if recipe_time.day < birthday.day:
                    age = str(12 - (birthday.month - recipe_time.month) - 1) + 'M'
                else:
                    age = str(12 - (birthday.month - recipe_time.month)) + 'M'
            else:
                age = str(y) + '岁'
        if recipe_time.month == birthday.month and recipe_time.day > birthday.day:
            y = recipe_time.year - birthday.year
            if y == 0:
                if recipe_time.day < birthday.day:
                    age = str(12 - (birthday.month - recipe_time.month) - 1) + 'M'
                else:
                    age = str(12 - (birthday.month - recipe_time.month)) + 'M'
            else:
                age = str(y) + '岁'
        return y, age

    # 体重为空时，若使用默认身高体重，则根据性别和年龄计算体重默认值
    def get_default_weight(self, sex):
        num = self.age[0:-1]
        str = self.age[-1]
        weight = 0
        if sex == '男':
            if str == '岁' and int(num) > 18:
                weight = 60
            else:
                for k in self.male:
                    if k == self.age:
                        weight = self.male[k]
        else:
            if str == '岁' and int(num) > 18:
                weight = 50
            else:
                for k in self.female:
                    if k == self.age:
                        weight = self.female[k]
        return weight

    # 不使用默认身高体重（以下只考虑传入weight不为空的情况，weight为空时直接取90（预设值））
    def ccr_calculate(self, sex, unit, age, weight, scr):
        if unit == 'mg/dl':  # 单位不区分大小写
            ccr = ((140 - age) * weight) / (72 * scr)
        elif unit == 'umol/L':  # 单位不区分大小写
            ccr = ((140 - age) * weight) / (0.818 * scr)
        else:
            ccr = 90
        if sex == '女':
            ccr = 0.85 * ccr
        return ccr

    # weight为空时使用默认体重,默认体重根据性别和年龄计算
    def ccr_default_weight(self, sex, unit, age, scr):
        if sex == '男':
            weight = self.get_default_weight('男')
            if unit == 'mg/dl':  # 单位不区分大小写
                ccr = ((140 - age) * weight) / (72 * scr)
            elif unit == 'umol/L':  # 单位不区分大小写
                ccr = ((140 - age) * weight) / (0.818 * scr)
            else:
                ccr = 90
        else:
            weight = self.get_default_weight('女')
            if unit == 'mg/dl':  # 单位不区分大小写
                ccr = ((140 - age) * weight) / (72 * scr) * 0.85
            elif unit == 'umol/L':  # 单位不区分大小写
                ccr = ((140 - age) * weight) / (0.818 * scr) * 0.85
            else:
                ccr = 90
        return ccr

if __name__ == '__main__':

    cal_ccr = Ccr('2019-07-01','2003-03-05')
    w1 = cal_ccr.get_default_weight('男')
    print(w1)
    w2 = cal_ccr.get_default_weight('女')
    print(w2)
    print(cal_ccr.age)
    print(cal_ccr.y)
    # 不使用默认体重
    # a1 = cal_ccr.ccr_calculate(sex='男', unit='mg/dl', age=cal_ccr.y, weight=60, scr=1)  # 公式一
    # b1 = cal_ccr.ccr_calculate(sex='男', unit='umol/L', age=cal_ccr.y, weight=60, scr=1)  # 公式二
    c1 = cal_ccr.ccr_calculate(sex='女', unit='mg/dl', age=25, weight=56, scr=2)
    # d1 = cal_ccr.ccr_calculate(sex='女', unit='umol/L', age=cal_ccr.y, weight=60, scr=1)
    # 使用默认体重，xml中weight应为空
    # a1 = cal_ccr.ccr_default_weight(sex='男', unit='mg/dl', age=cal_ccr.y,  scr=1)  # 公式一
    # b1 = cal_ccr.ccr_default_weight(sex='男', unit='umol/L', age=cal_ccr.y, scr=1)  # 公式二
    # c1 = cal_ccr.ccr_default_weight(sex='女', unit='mg/dl', age=cal_ccr.y,  scr=1)
    # d1 = cal_ccr.ccr_default_weight(sex='女', unit='umol/L', age=cal_ccr.y, scr=1)
    # print(a1)
    # print(b1)
    print(c1)
    # print(d1)
    a = ((140 - 19) * 60) / (0.818 * 9) # 公式一
    print(a)