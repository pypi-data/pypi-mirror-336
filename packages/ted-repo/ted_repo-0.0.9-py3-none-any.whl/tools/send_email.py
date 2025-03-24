from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
import sys


def send_email(msg="test msg", mail_title="info"):
    #qq邮箱smtp服务器
    host_server = 'smtp.163.com'
    #sender_qq为发件人的qq号码
    sender_qq = '17628292357@163.com'
    #pwd为qq邮箱的授权码
    pwd = 'ILHYSKNCFWCVRPJG' ## xh**********bdc
    #发件人的邮箱
    sender_qq_mail = '17628292357@163.com'
    #收件人邮箱
    receiver = '565428604@qq.com'

    #邮件的正文内容
#     mail_content = '你好，这是使用python登录qq邮箱发邮件的测试'
    mail_content = msg
    #邮件标题

    #ssl登录
    smtp = SMTP_SSL(host_server)
    #set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.set_debuglevel(1)
    smtp.ehlo(host_server)
    smtp.login(sender_qq, pwd)

    msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq_mail
    msg["To"] = receiver
    smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
    smtp.quit()
    
if __name__ == "__main__":
    if len(sys.argv)==3:
        msg = sys.argv[1]
        title = sys.argv[2]
        send_email(msg, title)
    elif len(sys.argv)==2:
        msg = sys.argv[1]
        send_email(msg)
    else:
        send_email()        
