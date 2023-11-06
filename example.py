from addoutline import addtoc
import re

# 用法1
# 为离散数学增加目录
# 直接编写完整的目录字串
tocstring='''第1部分 数理逻辑 1
 第1章 命题逻辑的基本概念 3
  1.1 命题与联结词 3
  1.2 命题公式及其赋值 9
  习题1 14
 第2章 命题逻辑等值演算 19
 第3章 命题逻辑的推理理论 46
 第4章 一阶逻辑基本概念 60
 第5章 一阶逻辑等值演算与推理 73
第2部分 集合论 89
 第6章 集合代数 91
 第7章 二元关系 110
 第8章 函数 145
第3部分 代数结构 175
 第9章 代数系统 177
 第10章 群与环 194
 第11章 格与布尔代数 220
第4部分 组合数学 235
 第12章 基本的组合计数公式 237
 第13章 递推方程与生成函数 253
第5部分 图论 291
 第14章 图的基本概念 293
 第15章 欧拉图与哈密顿图 316
 第16章 树 329
 第17章 平面图 344
 第18章 支配集、覆盖集、独立集、匹配与着色 356
第6部分 初等数论 369
 第19章 初等数论 371'''


addtoc(tocstring,"离散数学.pdf",offset=9,outputname="离散数学（有目录）.pdf")

# 用法2
# 为「发现社会 西方社会学思想评述.pdf」增加目录
# outline.txt文件中包含目录
# number.txt文件中包含页码

tocfile=open("outline.txt",encoding="utf-8")
number=open("number.txt")
#去掉所有的换行和多余一个的空格
n=number.read()
n=re.sub("\s+"," ",n)
n=n.strip("")
n=n.split(" ")
lines=tocfile.read().split("\n")
#构造目录字符串
tocstring=""
numberlen=len(n)
toclen=len(lines)
if(numberlen!=toclen):
    print("目录和页码的数量不匹配！")
    numberlen=min([numberlen,toclen])
for i in range(numberlen):
    tocstring=tocstring+lines[i]+' '+n[i]+"\n"
    print(f"{lines[i]} {n[i]}")
# table_of_contents=tocfile.read()
#删除最后一个换行符
tocstring=tocstring[:-1]
addtoc(tocstring,"发现社会 西方社会学思想述评.pdf",offset=11,outputname="发现社会 西方社会学思想述评(有目录).pdf")


