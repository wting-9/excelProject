import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender='1183298554@qq.com'  #邮件发送账号
reciever='332582281@qq.com'  #接收邮件账号
password='gqraeiwuiommbahc'  #授权码（这个要填自己获取到的）
smtp_server='smtp.qq.com'#固定写死
smtp_port=465#固定端口
 
 
#配置服务器
stmp=smtplib.SMTP_SSL(smtp_server,smtp_port)
stmp.login(sender,password)

filename = input("请输入Excel文件名：")

try:
    df = pd.read_excel(filename, skiprows=[0])
except FileNotFoundError:
    print("文件不存在或路径错误")
    exit()
except Exception as e:
    print("发生了错误:", str(e))
    exit()

# 按照姓名分组
grouped = df.groupby("姓名")

# 创建一个空数组用于存储每个分组的内容
contents = []

# 遍历每个分组
for name, group in grouped:
    # 创建一个新的字符串用于存储当前分组的内容
    content = "亲爱的" + name +"同学：" + "\n"
    content +=("祝贺您顺利完成本学期的学习！教务处在此向您发送最新的成绩单。\n\n")
    
    # 遍历该组的每一行数据
    for index, row in group.iterrows():
        # 输出课程名称、学分、百分成绩、五分成绩
        content += ("[" + str(row["课程名称"]) + "]" + ":"
                    "[" + str(row["百分成绩"]) + "]" + "\n")
    content += ("希望您能够对自己的成绩感到满意，并继续保持努力和积极的学习态度。如果您在某些科目上没有达到预期的成绩，不要灰心，这也是学习过程中的一部分。我们鼓励您与您的任课教师或辅导员进行交流，他们将很乐意为您解答任何疑问并提供帮助。请记住，学习是一个持续不断的过程，我们相信您有能力克服困难并取得更大的进步。\n\n")
    
    content += ("再次恭喜您，祝您学习进步、事业成功！\n\n")

    content +=("教务处\n")

    # 将当前分组的内容添加到数组中
    contents.append(content)

# 将数组中的内容进行处理
result = "\n".join(contents)

# 打印结果
print(result)

message = MIMEText(result, 'plain', 'utf-8')  #发送的内容
message['From'] = sender
message['To'] = reciever
subject = '成绩单发送'
message['Subject'] = Header(subject, 'utf-8') #邮件标题

try:
  stmp.sendmail(sender, reciever, message.as_string())
except Exception as e:
  print ('邮件发送失败--' + str(e))
print ('邮件发送成功')
