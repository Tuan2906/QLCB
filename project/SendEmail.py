import smtplib
from email.message import EmailMessage


def send_mail(mailto, madatcho, nguoi_Lon, tre_Em, cbs,soGhe,venl, vete):
    email_from = 'tuannguyen2022002@gmail.com'  # email người gửi
    email_to = mailto  # email người nhận
    password = 'gmty cxng ckud uglr'  # password phải sinh ra trong bảo vệ 2 lớp bảo mật của google
    subject = 'Thu xac nhan thong tin chuyen bay'

    for cb in cbs:
        body = 'Ten chuyen bay: ' + str(cb.get('MaCB')) + '.\n'
        body = body + 'Ga di: ' + str(cb.get('noidi')) + '.\n'
        body = body + 'Ga den: ' + str(cb.get('noiden')) + '.\n'
        body = body + 'Ma dat cho:' + str(madatcho) + '.\n '

    for i in range(len(nguoi_Lon)):
        body = body + 'Ten hanh khach thứ'+str(i+1) + ":" + str(nguoi_Lon[i]["hoten"]) + '.\n'
        if venl !="":
            body = body + 'Mã vé :' + venl[i] + '.\n'
            body = body + 'Số ghế :' + soGhe[i]+ '.\n'

    for i in range(len(tre_Em)):
        body = body + 'Ten hanh khach(trẻ em)'+ str(i+1) + ":" + str(tre_Em[i]["hotenTreEm"]) + '.\n'
        if vete != "":
            body = body + 'Mã vé :' + vete[i]+ '.\n'
            body = body + 'Số ghế :' + soGhe[len(nguoi_Lon) + i]+ '.\n'

    em = EmailMessage()
    em['From'] = email_from
    em['To'] = email_to
    em['Subject'] = subject
    em.set_content(body)
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()  # Định danh trong stmp server
        smtp.starttls()  # Thiết lập kết nối smtp trong chế độ TLS
        smtp.login(email_from, password)  # Đăng nhập vào tài khoản email sender
        smtp.send_message(em)  # Gửi mail
        print('Check your email ;)')
