from project import login, app, SendEmail
from flask import render_template, jsonify, request,session,redirect, url_for
import datetime, dao, stripe
from random import random
import os, random
from project.models import TaiKhoan, UserRole
from flask_login import login_user as flask_login_user, login_user
from project.admin import *
from datetime import datetime,timedelta


stripe.api_key = "sk_test_51OQW7nEDuGccAkUEVhnnJfvWztoRchurir6oDVg1AWBcag4lw6fvIYsU8FiFc4zPY2rBbmyHyuDNdHObDOl0ei96000SDdfuHI"
public_key = "pk_test_51OQW7nEDuGccAkUEwtUAoxMsf7qoYBGNWEytAWuxxRJt3FwqwP1PjDe0nuJREw9HLdNTtwj7ItvjBRxTj3oKCQJ900ivAUTxhX"


@app.route('/')
def index():
    session["flight"] = []
    return render_template('index.html')



@app.route('/login', methods = ['get','post'])
def nhanVienLogin():
    err_login = None
    if request.method.__eq__('GET'):
        if session.get('hotennv') is not None:
            if session.get('hotennv').get('role').__eq__('UserRole.laplich'):
                return render_template('LapLich.html', hoten = session.get('hotennv'))
            if session.get('hotennv').get('role').__eq__('UserRole.banve'):
                return render_template('BanVeIndex.html',hoten = session.get('hotennv'))
        else: return render_template('login.html')

    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password)
        hoten = dao.get_hoten_by_account(username=username, password=password)

        if user:
            login_user(user)
            session['hotennv'] = {
                'hovaTen': hoten.hovaTen,
                'role': str(user.user_role)
            }
            session['idnv'] = hoten.id
            if str(user.user_role).__eq__('UserRole.laplich'):
                return render_template('LapLich.html', hoten = hoten)
            if str(user.user_role).__eq__('UserRole.banve'):
                print('123')
                return render_template('BanVeIndex.html',  hoten = hoten)
        else:err_login = 'username hoặc password sai, xin vui lòng nhập lại'


        return render_template('login.html', err_login = err_login)





@app.route('/logout', methods =['get'])
def logout():
    logout_user()
    del(session['idnv'])
    del(session['hotennv'])
    return redirect('/login')

def storeSearchInformation():

    SearchInformation = {
        'start': request.form.get('StartDes'),
        'end': request.form.get('EndDes'),
        'adultNum': int(request.form.get('adultNumber')),
        'childrenNum': int(request.form.get('childrenNumber')),
        'ticketLevel': request.form.get('level'),
        'startDate': request.form.get('StartDate'),
        'timeNow' : datetime.now()
    }
    if request.form.get('one-way'):
        SearchInformation['cateFlight'] = request.form.get('one-way')
    else:
        SearchInformation['cateFlight'] = request.form.get('round-trip')
        SearchInformation['endDate'] = request.form.get('EndDate')
    session['thongtintimkiem'] = SearchInformation



URL =''
LenSS =  0
@app.route('/chuyenbay', methods = ['post','get'])
def chuyen_bay():
    global URL
    global LenSS
    time = None
    if request.method == "POST":
        if URL == '/chuyenbay':
            SSI = session.get('thongtintimkiem')
        else:
            storeSearchInformation()
            SSI = session.get('thongtintimkiem')
    if request.method == 'GET':
        time = request.args.get('time')
        SSI = session.get('thongtintimkiem')
        if LenSS > 0:
            temp = SSI.get('end')
            SSI['end'] = SSI.get('start')
            SSI['start'] = temp
        SSI['startDate'] = time
    Day = datetime.strptime(str(SSI.get('timeNow').date()), "%Y-%m-%d")
    date_range = [Day + timedelta(days=i) for i in range(30)]
    tongNguoi = SSI.get('adultNum') + SSI.get('childrenNum')
    if time is None and SSI.get('cateFlight') =='round-trip' : ## if 1
        URL = '/chuyenbay'
    if SSI.get('cateFlight') == 'one-way': ## if 2

        URL = '/ThongTinHanhKhach'

    if URL == '/chuyenbay' and LenSS > 0: # khu hoi   ## if 1
        URL = '/ThongTinHanhKhach'
        LichBay = dao.get_Valid_lichBay(SSI.get('start'), SSI.get('end'),
                                        SSI.get('timeNow')
                                        , tongNguoi, SSI.get('ticketLevel'),
                                        datetime.strptime(SSI.get('endDate'), "%Y-%m-%d"),session.get('idnv'))
        # LenSS = 0 #goback lại
        return render_template('ChuyenBay.html', SSI=SSI, soluong=tongNguoi, soluongngl=SSI.get('adultNum'),
                               soluongtre=SSI.get('childrenNum'), date_range=date_range, LichBayArr=LichBay,
                               current_day=SSI.get('timeNow'), dayStart=SSI.get('endDate'),cateFlight = SSI.get('cateFlight'),
                               noidi = SSI.get('end'),noiden = SSI.get('start'), URL = URL)
    print(SSI.get('startDate'))
    # # thang 1 chieu
    LichBay = dao.get_Valid_lichBay(SSI.get('start'), SSI.get('end'),
                                SSI.get('timeNow')
                                , tongNguoi, SSI.get('ticketLevel'),
                                datetime.strptime(SSI.get('startDate'), "%Y-%m-%d"),session.get('idnv'))
    # flag = False
    return render_template('ChuyenBay.html', SSI=SSI, soluong=tongNguoi,soluongngl = SSI.get('adultNum'),
                   soluongtre = SSI.get('childrenNum'), date_range=date_range, LichBayArr=LichBay,
                   current_day = SSI.get('timeNow'),dayStart=SSI.get('startDate'), cateFlight = SSI.get('cateFlight'),noidi = SSI.get('start'),noiden = SSI.get('end')
                    ,URL = URL)


arr=[]
@app.route("/api/flight", methods=['post'])
def add_flight(): #luu thong tin cb dc chọn
    data = request.json
    global LenSS,arr
    flight = {
        "MaLB": data.get("MaLB"),
        "MaCB": data.get("MaCB"),
        "noidi" : data.get("noidi"),
        "noiden" : data.get("noiden"),
        "idmb": dao.get_ID_MayBay(data.get('tenMB')),
        "NgayKhoiHanh":data.get("NgayKhoiHanh"),
        "Tongtien": data.get("Tongtien")
    }
    arr.append(flight)
    session['flight'] = arr
    LenSS = len(session["flight"])
    return jsonify(flight)


def GetCheckInFlight(TTChuyen):
    LichBay = []
    for lb in TTChuyen:
        noidi = dao.get_SanBay_By_ID(dao.get_TuyenBay_By_IDChuyenBay(lb.id_ChuyenBay).id_SbDi)
        noiden = dao.get_SanBay_By_ID(dao.get_TuyenBay_By_IDChuyenBay(lb.id_ChuyenBay).id_SbDen)
        LichBay.append({
            'MaLB': lb.lichbay_id,
            'MaCB': lb.id_ChuyenBay,
            'MayBay': dao.get_MayBay(lb.id_MayBay),
            'idMayBay':lb.id_MayBay,
            'Noidi': noidi,
            'Noiden': noiden,
            'NgayKhoiHanh': lb.NgayBay,
            'ThoiGianDi': lb.thoiGianBay,
        })
    return LichBay

def GetCheckInHanhKhach(TTKhachHang):
    TTHanhKhach = []
    for hk in TTKhachHang:

        tt = {
            'Hoten': hk.hoTen,
            'NgaySinh': hk.ngSinh,
            'GioiTinh': hk.gioiTinh,
            'HangGhe': hk.maHangVe
        }

        if hasattr(hk,'sdt') and hasattr(hk,'CCCD'):
            tt['SDT'] = hk.sdt
            tt['CCCD'] = hk.CCCD
        if hasattr(hk,'id_NguoiLon'):
            tt['NguoiBaoHo'] = dao.get_NguoiBaoHo_By_ID(hk.id_NguoiLon)
        TTHanhKhach.append(tt)
    return TTHanhKhach





URL_CI = ''
@app.route('/Checkin', methods=['get', 'post'])
def CheckIn():
    if request.method == 'POST':
        MaChoKH = request.form.get('madatcho')
        if MaChoKH != None:
            TTKhachHangNL = dao.get_HanhKhachNguoiLon_By_MaPhieu(maphieu=MaChoKH)
            URL_CI = '/DatCho'
            print(TTKhachHangNL)
            if TTKhachHangNL == []:
                err = 'Mã đặt chổ của bạn không đúng hoặc đã được xử lý, vui lòng kiểm tra lại'
                return render_template('Checkin.html', err = err)
            TTChuyen = dao.get_lichbay_By_MaPhieu(maphieu=MaChoKH)
            TTKhachHangTE = dao.get_HanhKhachTreEm_By_MaPhieu(maphieu=MaChoKH)
            session['CheckInFlight'] = GetCheckInFlight(TTChuyen)
            session['CheckInHKNL'] = GetCheckInHanhKhach(TTKhachHangNL)
            session['CheckInHKTE'] = GetCheckInHanhKhach(TTKhachHangTE)
            session['madatchocheckin'] = MaChoKH

            return render_template('Checkin.html', maphieu = MaChoKH,
                                   TTchuyenbay=session.get('CheckInFlight'), TTKhachHangNL=session.get('CheckInHKNL')
                                   ,TTKhachHangTE = session.get('CheckInHKTE')
                                   , URL = URL_CI)

    return render_template('Checkin.html')


@app.route('/delssCI', methods = ['get'])
def delete_ssCI():
    delete_session()
    return redirect('/Checkin')




@app.route('/datvedelss',methods = ['get'])
def delete_ssDV():
    delete_session()
    return redirect('/')





def delete_session():
    global URL_CI,URL,LenSS,arr
    URL_CI = ''
    URL = ''
    LenSS = 0
    arr = []
    if session.get('CheckInFlight') is not None:
        del(session['CheckInFlight'])
        del(session['CheckInHKNL'])
        del(session['CheckInHKTE'])
        del(session['GHE'])
        del(session['id_mb'])
        del (session['Ghe_HK'])
        del (session['hk_ghe'])

    else:
        del(session['thongtintimkiem'])
        del(session['flight'])
        del(session['soluong'])
        del(session['email'])
        del(session['sodienthoai'])
        del(session['nguoiLon'])
        del(session['treEm'])
        del(session['maHoaDon'])
        del(session['id_NguoiLon'])
        del(session['id_treEm'])
        del(session['ve_banNgl'])
        del(session['madatcho'])
        del(session['ve_banTreEm'])
        if session.get('GHE') is not None:
            del(session['GHE'])






@app.route('/api/ghe')
def load_ghe():
    if session.get('idnv'):
        print('day la lich bay co nv')
        print(session.get('flight')[0].get('MaLB'))
        id_lichbay = session.get('flight')[0].get('MaLB')

    else:
        id_lichbay = session.get('id_mb').get('malb')
    listGhe = dao.Ghe_DaDat(id_lichbay)
    soluongghe = len(listGhe)
    ghe = []
    for i in range(soluongghe):
        ghe.append(
            {
                'soghe': listGhe[i].gheDaDat
            }
        )
    return jsonify(ghe)


@app.route('/api/MayBay', methods=['POST'])
def get_id_mb(): # Load du lieu từ trang Checkin sang trang dat cho
    data = request.json
    id_mb = {
        'id': data.get('MaMB'),
        'macb': data.get('MaCB'),
        'noidi':data.get('noidi'),
        'noiden':data.get('noiden'),
        'malb':data.get('MaLB'),
        'ngaykhoihanh': data.get('NgayKhoiHanh'),
        'thoigianbay': data.get('ThoiGianBay')
    }
    session['id_mb'] = id_mb
    return jsonify('abc')



def add_Dict(TTHK, TTCB, arr):
    for hk in TTHK:
        dict = {
            'hoTen': hk.get('Hoten'),
            'MaCB': TTCB.get('macb'),
            'noidi': TTCB.get('noidi'),
            'noiden': TTCB.get('noiden'),
            'hangve': hk.get('HangGhe')
        }
        arr.append(dict)



@app.route('/DatCho', methods = ['POST', 'GET'])
def DatCho():
    global URL
    if session.get('idnv'):
        id_mb = session.get('flight')[0].get('idmb')
        dayghe = dao.get_DayGhe_In_MayBay(id_mb)
        ghe = dao.get_Ghe_In_MayBay(id_mb)
        soluongghe = dao.count_so_ghe(id_mb)
        soluongday = len(dayghe)
        lenNL = len(session.get("nguoiLon"))
        lenTE = len(session.get("treEm"))
        noidi = session.get('flight')[0].get('noidi')
        noiden = session.get('flight')[0].get('noiden')
        MaCB =session.get('flight')[0].get('MaCB')
        hk = session.get("nguoiLon")+session.get("treEm")
        return render_template('DatCho.html', ghe=ghe, dayghe=dayghe, soluongghe=soluongghe
                               , soluongday=soluongday, soluong=lenNL+lenTE,hk = hk, lenNL = lenNL,
                               hangve=dao.truyVanMaHangVe(session.get('thongtintimkiem').get('ticketLevel'))
                               ,noidi = noidi, noiden = noiden, MaCB = MaCB)
    else:
        if dao.get_tinhtrangve(session.get('id_mb').get('malb'), session.get('madatchocheckin')).__eq__('da xu ly'):
            err = 'Vé của bạn đã được xử lý, vui lòng kiểm tra lại'
            return render_template('Checkin.html', err=err, URL = '/Checkin')
        id_mb = session.get('id_mb').get('id')
        dayghe = dao.get_DayGhe_In_MayBay(id_mb)
        ghe = dao.get_Ghe_In_MayBay(id_mb)
        soluongghe = dao.count_so_ghe(id_mb)
        soluongday = len(dayghe)
        hk_ghe = []
        add_Dict(session.get('CheckInHKNL'),session.get('id_mb'),hk_ghe)
        add_Dict(session.get('CheckInHKTE'),session.get('id_mb'),hk_ghe)
        URL = ''
        session['hk_ghe'] = hk_ghe
        hangve_1hk = session.get('hk_ghe')[0].get('hangve')
        soluonghk = len(hk_ghe)
        return render_template('DatCho.html',ghe = ghe, dayghe = dayghe, soluongghe = soluongghe
                           , soluongday = soluongday, hk_ghe = session.get('hk_ghe'),
                               soluong = soluonghk, hangve = hangve_1hk)


@app.route('/api/thuonggia')
def thuonggia():

    if session.get('idnv'):
        id_mb = session.get('flight')[0].get('idmb')
        print('co nhan vien')
    else:
        id_mb = session.get('id_mb').get('id')
    print(id_mb)
    HangGhe = []
    for i in dao.get_hangGhe(id_mb):
        HangGhe.append(
            {
                'Day':i.dayGhe,
                'Ghe':i.ghe_id,
                'Hang': i.hangVe_id
            }
        )
    return jsonify(HangGhe)








#####################################TUAN

URL_banve = ''
@app.route("/ThongTinHanhKhach", methods=['POST','get'])
def send_Fligh():
    try:
        tong = tongTien()
        global URL, URL_banve
        URL = ''
        URL_banve = '/thanhtoan'
        print(session['flight'])
        print(session.get('idnv'))

    except Exception as ex:
        print(ex)
        return redirect("/ThongTinHanhKhach")
    else:
        soluong = {
            "sl_NguoiLon": session['thongtintimkiem'].get('adultNum'),
            "sl_TreEm": session['thongtintimkiem'].get('childrenNum')
            # mai mot dinh nghia nguoi lon, tre em trong day
        }
        session['soluong'] = soluong
        return render_template("ThongTinHanhKhach.html", sl=soluong, URL=URL_banve, tong=tong)


def tongTien():
    tongtien = int(session["flight"][0].get('Tongtien'))
    if session['thongtintimkiem'].get('cateFlight').__eq__('round-trip'):
        tongtien += int(session["flight"][1].get('Tongtien'))
    return tongtien

def lay_MaDatCho():
    bang_chu = "abcdefghijklmnopqrstuvwxyz"

    # Tạo ra 3 chữ ngẫu nhiên không trùng
    ma_datcho = ""
    while len(ma_datcho) < 6:
        random_bangchu = random.choice(bang_chu)
        ma_datcho += random_bangchu

    return ma_datcho


def check_MaDatCho():
    layma = lay_MaDatCho()
    ma_DatCho = dao.truyVanMaPDC(maDaCho=layma);
    print('madatcho: ' + ma_DatCho)
    if layma.__eq__(ma_DatCho):
        check_MaDatCho()
    else:
        return layma




@app.route("/thanhtoan", methods=['post', "get"])
def gui_ThongTinHK():  # hàm này xử lý gán thông tin hành khách vào session để gui qua trang nhapthogtingthantoan
    global CCCD_nguoiLon
    if request.method.__eq__("POST"):
        session['email'] = request.form.get('email')
        session['sodienthoai'] = request.form.get('sdt')
        NguoiLon = []
        TreEm = []
        print(request.form.get('nguoiLon_diCung'))
        for i in range(session['thongtintimkiem'].get('adultNum')):
            NguoiLon.append({
                'hoten': request.form.get('hoten' + str(i)),
                'gioitinh': request.form.get('gioitinh' + str(i)),
                'ngaySinh': request.form.get('ngaysinh_Nglon' + str(i)),
                'CCCD': request.form.get('CCCD' + str(i))
            })
            if request.form.get('nguoiLon_diCung') is not None:
                if NguoiLon[i]["hoten"].__eq__(str(request.form.get('nguoiLon_diCung'))):
                    CCCD_nguoiLon = NguoiLon[i]["CCCD"]

        session["nguoiLon"] = NguoiLon
        print(session['thongtintimkiem'].get('childrenNum'))
        for j in range(session['thongtintimkiem'].get('childrenNum')):
            TreEm.append({

                'CCCD_NglondiCung': CCCD_nguoiLon,
                'hotenTreEm': request.form.get('hoten_TreEm' + str(j)),
                'gioitinhTreEm': request.form.get('gioitinh_TreEm' + str(j)),
                'ngaySinhTreEm': request.form.get('ngaySinh_TreEm' + str(j))
            })
        thongtinLienHe = {
            'Email': request.form.get("email"),
            'SĐT': request.form.get("sdt")
        }
        print(thongtinLienHe)
        print(TreEm)
        session["treEm"] = TreEm
        session["lienHe"] = thongtinLienHe
        # luu_ThongTinNguoiLon()
        # luu_ThongTinTreEm()
        # luu_ThongTinChung()
        loaive =session['thongtintimkiem'].get('cateFlight')
        ma_hd = [check_MaDatCho()]
        if loaive.__eq__("round-trip"):
            ma_hd.append(check_MaDatCho())
        session["maHoaDon"] = ma_hd
        if session.get('idnv'):
            return redirect("/DatCho")
        else:
            URL_banve ='/payment'
            return render_template("nhapThongTinThanhToan.html", public_key=public_key, tongtien=tongTien(), maHD=ma_hd, URL = URL_banve)


def luu_ThongTinNguoiLon():
    NguoiLon = session.get('nguoiLon')
    lienHe = session.get("lienHe")
    print(lienHe)
    print(NguoiLon)
    ds_idNguoiLon = []
    for i in range(len(NguoiLon)):
        if i == 0:
            print(lienHe.get('SĐT'))
            print(lienHe.get('Email'))

            if NguoiLon[i]['gioitinh'] == "1":
                id_Ngl = dao.luu_ThongTinNguoiLon(name=NguoiLon[i]["hoten"], gioitinh='Nam',
                                                  ngaySinh=NguoiLon[i]["ngaySinh"],
                                                  CCCD=NguoiLon[i]["CCCD"])
                ds_idNguoiLon.append(id_Ngl)
                dao.luu_ThongTinSDT(sodienthoai=lienHe.get('SĐT'), CCCD=NguoiLon[i]['CCCD'])
                dao.luu_ThongTinEmail(ten=lienHe.get('Email'), CCCD=NguoiLon[i]["CCCD"])
            if NguoiLon[i]['gioitinh'] == "0":
                id_Ngl = dao.luu_ThongTinNguoiLon(name=NguoiLon[i]["hoten"], gioitinh='Nữ',
                                                  ngaySinh=NguoiLon[i]["ngaySinh"],
                                                  CCCD=NguoiLon[i]["CCCD"])
                ds_idNguoiLon.append(id_Ngl)
                dao.luu_ThongTinSDT(sodienthoai=lienHe.get('SĐT'), CCCD=NguoiLon[i]['CCCD'])
                dao.luu_ThongTinEmail(ten=lienHe.get('Email'), CCCD=NguoiLon[i]["CCCD"])
        else:
            print('123')
            if NguoiLon[i]['gioitinh'] == "1":
                id_Ngl = dao.luu_ThongTinNguoiLon(name=NguoiLon[i]["hoten"], gioitinh='Nam',
                                                  ngaySinh=NguoiLon[i]["ngaySinh"],
                                                  CCCD=NguoiLon[i]["CCCD"])
                ds_idNguoiLon.append([id_Ngl])
            if NguoiLon[i]['gioitinh'] == "0":
                id_Ngl = dao.luu_ThongTinNguoiLon(name=NguoiLon[i]["hoten"], gioitinh='Nữ',
                                                  ngaySinh=NguoiLon[i]["ngaySinh"],
                                                  CCCD=NguoiLon[i]["CCCD"])
                ds_idNguoiLon.append([id_Ngl])

    session["id_NguoiLon"] = ds_idNguoiLon


def luu_ThongTinTreEm():
    treEm = session.get('treEm')
    ds_idTreEm = []
    for i in range(len(treEm)):
        if treEm[i]['gioitinhTreEm'] == "1":
            id_treEm = dao.luu_ThongTinTreEm(name=treEm[i]['hotenTreEm'], gioiTinh='Nam',
                                             ngaySinh=treEm[i]['ngaySinhTreEm']
                                             , CCCD=treEm[i]['CCCD_NglondiCung'])
            ds_idTreEm.append(id_treEm)
        if treEm[i]['gioitinhTreEm'] == "0":
            id_treEm = dao.luu_ThongTinTreEm(name=treEm[i]['hotenTreEm'], gioiTinh='Nữ',
                                             ngaySinh=treEm[i]['ngaySinhTreEm']
                                             , CCCD=treEm[i]['CCCD_NglondiCung'])
            ds_idTreEm.append(id_treEm)

    session["id_treEm"] = ds_idTreEm


def luu_HoaDon():
    today = datetime.now()
    loaiVe = session['thongtintimkiem'].get('cateFlight')
    # print(today)
    mahd = session.get('maHoaDon')
    three_days_later = (today + timedelta(days=3)).strftime('%Y-%m-%d')
    dao.luu_ThanhToan(mahd = mahd[0],thanhtien=session["flight"][0].get('Tongtien'), ngayhethan=three_days_later, id_LichBay=session["flight"][0].get('MaLB'))
    if loaiVe.__eq__('round-trip'):
        dao.luu_ThanhToan(mahd = mahd[1],thanhtien=session["flight"][1].get('Tongtien'), ngayhethan=three_days_later, id_LichBay=session["flight"][1].get('MaLB'))


def luu_ThongTinMaDC(ma_dc):
    dao.luu_PhieuDatCho(maphieu=ma_dc, trangThai='đang xử lý')


def luu_ThongTinVeNguoiLon(maPhieu):
    loaiVe = session['thongtintimkiem'].get('cateFlight')
    thongtin_VeBanNgl = []
    for i in range(len(session.get("id_NguoiLon"))):
        if session.get('idnv') is not None:
            mave = check_MaDatCho()
            print('adv')
            print(session.get("flight"))
            print('ghe n è')
            print(i)
            print(session.get('GHE'))
            dao.luu_ThongTinVeBan(mave=mave, lichbay=session.get("flight")[0].get('MaLB')
                                  , id_HK=session.get("id_NguoiLon")[i], maphieu=maPhieu, mahangve=dao.truyVanMaHangVe(session['thongtintimkiem'].get('ticketLevel')),
                                  id_NVBV=session.get('idnv'), soGhe=session.get('GHE')[i])
            thongtin_VeBanNgl.append(
                mave
            )
        else:
            dao.luu_ThongTinVeDat(mave=check_MaDatCho(), lichbay=session["flight"][0].get('MaLB'), id_HK=session.get("id_NguoiLon")[i],
                                  maphieu=maPhieu, mahangve=dao.truyVanMaHangVe(session['thongtintimkiem'].get('ticketLevel')))
        if loaiVe.__eq__('round-trip'):
            if session.get('idnv'):
                mave = check_MaDatCho()
                dao.luu_ThongTinVeBan(mave=mave, lichbay=session["flight"][1].get('MaLB'), id_HK=i, maphieu=maPhieu, mahangve=dao.truyVanMaHangVe(session['thongtintimkiem'].get('ticketLevel')),
                                      id_NVBV=session.get('idnv'), soGhe="B1")
                thongtin_VeBanNgl.append({
                    "mave": mave,
                    "so_Ghe": 123  # phần này sẽ lấy từng phần tử ghế được lưu bên sơ đồ ghế bỏ cô
                })
            else:
                dao.luu_ThongTinVeDat(mave=check_MaDatCho(), lichbay=session["flight"][1].get('MaLB'), id_HK=session.get("id_NguoiLon")[i],
                                      maphieu=maPhieu, mahangve=dao.truyVanMaHangVe(session['thongtintimkiem'].get('ticketLevel')))
    if thongtin_VeBanNgl is not None:
        session["ve_banNgl"] = thongtin_VeBanNgl


def luu_ThongTinVeTreEm(maPhieu):
    loaiVe = session['thongtintimkiem'].get('cateFlight')
    thongtin_VeBanTreEm = []
    for i in range(len( session.get("id_treEm"))):
        if session.get('idnv') is not None:
            mave = check_MaDatCho()
            dao.luu_ThongTinVeBan(mave=mave, lichbay=session["flight"][0].get('MaLB'), id_HK=session.get("id_treEm")[i], maphieu=maPhieu, mahangve=dao.truyVanMaHangVe(session['thongtintimkiem'].get('ticketLevel')),
                                  id_NVBV=session.get('idnv'), soGhe=session.get('GHE')[len(session.get("id_NguoiLon")) + i])
            thongtin_VeBanTreEm.append(
                mave
            )
        else:
            dao.luu_ThongTinVeDat(mave=check_MaDatCho(), lichbay=session["flight"][0].get('MaLB'), id_HK=session.get("id_treEm")[i],
                                  maphieu=maPhieu, mahangve=dao.truyVanMaHangVe(session['thongtintimkiem'].get('ticketLevel')))
        if loaiVe.__eq__('round-trip'):
            if session.get('idnv'):
                mave = check_MaDatCho()
                dao.luu_ThongTinVeBan(mave=mave, lichbay=session["flight"][1].get('MaLB'), id_HK=i, maphieu=maPhieu

                                      , mahangve=dao.truyVanMaHangVe(session['thongtintimkiem'].get('ticketLevel')),
                                      id_NVBV=session.get('idnv'), soGhe="B1")
                thongtin_VeBanTreEm.append({
                    "mave": mave,
                    "so_Ghe": 123  # phần này sẽ lấy từng phần tử ghế được lưu bên sơ đồ ghế bỏ cô
                })
            else:
                dao.luu_ThongTinVeDat(mave=check_MaDatCho(), lichbay=session["flight"][1].get('MaLB'), id_HK=session.get("id_treEm")[i],
                                      maphieu=maPhieu, mahangve=dao.truyVanMaHangVe(session['thongtintimkiem'].get('ticketLevel')))
    if thongtin_VeBanTreEm is not None:
        session["ve_banTreEm"] = thongtin_VeBanTreEm


def luu_ThongTinChung():
    luu_ThongTinNguoiLon()
    luu_ThongTinTreEm()
    madatcho = check_MaDatCho()
    luu_ThongTinMaDC(ma_dc=madatcho)
    luu_ThongTinVeNguoiLon(maPhieu=madatcho)
    luu_ThongTinVeTreEm(maPhieu=madatcho)
    luu_HoaDon()
    print('day la ham luu_ThongTinChung')
    print(madatcho)
    return madatcho

a = 1

@app.route('/payment', methods=['POST'])
def payment():
    global a
    # CUSTOMER INFO
    # luuThongTinHanhKhach()
    if request.method.__eq__("POST"):
        if a == 2:
            a = 1
            return redirect("/")
        a += 1;
        if request.form.get("xacnhan") is None:
            customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                              source=request.form['stripeToken'])

            # PAYMENT INFO
            charge = stripe.Charge.create(
                customer=customer.id,
                amount=tongTien(),  # 19.99
                currency='VND',
                description='Trả tiền vé máy bay'
            )
            ngaydat = str(datetime.now().strftime('%d/%m/%y'))
            madatcho = luu_ThongTinChung()
            session["madatcho"] = madatcho
            print(madatcho)
            print(a)
            SendEmail.send_mail(mailto=session.get("lienHe").get("Email"), madatcho=madatcho,
                                nguoi_Lon=session.get('nguoiLon'), tre_Em=session.get('treEm'), cbs=session.get('flight'), soGhe=1,
                                venl="",vete="")
        return render_template('xacNhanThongTinThanhToan.html', nguoiLon=session.get('nguoiLon'),
                               lienHe=session.get("lienHe"),
                               treEm=session.get('treEm'),
                               soluong=session.get('soluong'), ngaydat=ngaydat, madatcho=madatcho)


def duyetSession(list, soluong, nameSS):
    for i in range(soluong):
        list.append(session.get(nameSS + str(i)))
    return list



def duyetghe (soluong):
    CacGhe = []
    soluongghe = soluong
    for i in range(soluongghe):
        session['ghe' + str(i)] = request.form.get('tenghe' + str(i))
    return duyetSession(CacGhe, soluongghe, 'ghe')



@app.route('/DatCho/xacnhanchuyendi', methods=['GET', 'POST'])
def xacnhan():
    if request.method == 'POST':

        if session.get('idnv'):
            ListGhe = duyetghe(len(session.get("nguoiLon")+session.get("treEm")))
            URL_banve  = '/xacNhanChuyenDi'
            print("trong xacnhanchuyedi")
            print(session.get('flight'))
            print('list ghe')
            print(ListGhe)
            print('ghe trong datcho/xacnhanchuyendi')
            print(session.get('GHE'))
            session['GHE'] = ListGhe
            return render_template("nhapThongTinThanhToan.html", tongtien=tongTien(), maHD=session.get("maHoaDon"),URL = URL_banve)
        else:
            ListGhe = duyetghe(len(session.get('hk_ghe')))
            session['GHE'] = ListGhe
            idlb = session.get('id_mb').get('malb')
            dao.Save_Ghe(maPhieu=session.get('madatchocheckin'), CacGhe=ListGhe, id_lb=idlb)
            return redirect('/DatCho/XacNhanChuyenDi')





@app.route('/DatCho/XacNhanChuyenDi', methods=['GET', 'POST'])
def XacNhanChuyenDi():
    if request.method == 'GET':
        # sl = session.get('SoLuongKhachHang')
        # madatcho = session.get('madatcho')
        # kh = dao.get_HanhKhach_By_MaPhieu(madatcho)
        # CB = dao.get_ChuyenBays_By_MaPhieu(madatcho)
        arr_xacnhan= []
        TTHK = session.get('CheckInHKNL')+ session.get('CheckInHKTE')
        TTCB = session.get('id_mb')
        i=0
        for hk in TTHK:
            dict = {
                'hoTen': hk.get('Hoten'),
                'MaCB': TTCB.get('macb'),
                'noidi': TTCB.get('noidi'),
                'noiden': TTCB.get('noiden'),
                'ghe': session.get('ghe' + str(i))
            }
            arr_xacnhan.append(dict)
            i +=1
        session['Ghe_HK']  = arr_xacnhan
        return render_template('XacNhanChuyenDi.html', ttxn = arr_xacnhan)



@app.route("/xacNhanChuyenDi", methods=["post"])
def xacNhan_ChuyenDi():
    if request.method.__eq__("POST"):
        print(session.get('flight'))
        nguoi_Lon = session.get("nguoiLon")
        tre_Em = session.get("treEm")
        session["madatcho"]= luu_ThongTinChung()
        lenNL = len(session.get("nguoiLon"))
        lenTE = len(session.get("treEm"))
        soluong = lenNL + lenTE
        hk = nguoi_Lon + tre_Em
        print('ghe')
        print(session.get('GHE'))
        print(session.get('GHE')[0])
        # dao.Save_Ghe(maPhieu=session.get('madatcho'), CacGhe=session.get('GHE'), id_lb=session.get('flight')[0].get('MaLB'))
        return render_template("xacNhanChuyenDi.html",hk=hk, soluong=soluong,
                           chuyen_bay=session.get('flight')[0].get('MaCB'), so_ghe= session.get('GHE')
                               ,lenNL = lenNL)


@app.route("/TheLenTauBay")
def the_LenTauBay():

    if  session.get('idnv') is not None:
        ngayDi = datetime.strptime(session.get('flight')[0].get('NgayKhoiHanh'), '%Y-%m-%d %H:%M:%S')  # phan này trường phai gửi ngày đi của cb ngta chọn đưa qua ây
        maCB =   session.get('flight')[0].get('MaCB')# truong phai dua qua ay macb hanh khach chon
        ma_datcho = session.get("madatcho")
        venl = session.get("ve_banNgl")
        vete = session.get("ve_banTreEm")
        nguoi_Lon = session.get("nguoiLon")
        tre_Em = session.get("treEm")
        lenNL = len(session.get("nguoiLon"))
        lenTE = len(session.get("treEm"))
        tongsoluong = lenNL + lenTE
        hk = nguoi_Lon + tre_Em
        return render_template("TheLenTauBay.html", ga_di=session.get('flight')[0].get('noidi')
                               , ga_den=session.get('flight')[0].get('noiden'),lenNL = lenNL,so_ghe= session.get('GHE')
                               ,hk = hk,maCB=maCB, ngayDi=ngayDi.date(), gioDi=ngayDi.time(),
                               ma_datcho=ma_datcho, soluong = tongsoluong,vete = vete, venl = venl)
    else:
        ma_datcho = session.get('madatchocheckin')
        thongtincb = session.get('id_mb')
        ngay_gio_bay =datetime.strptime(session.get('id_mb').get('ngaykhoihanh'), '%Y-%m-%d %H:%M:%S')
        print(ngay_gio_bay.time())
        hk_ve = dao.get_Mave_for_Hanhkhach(thongtincb.get('malb'),ma_datcho)
        print(len(hk_ve))
        return render_template("TheLenTauBay.html", ga_di=thongtincb.get('noidi'), ga_den=thongtincb.get('noiden')
                               , maCB=session.get('id_mb').get('macb'), ngayDi=ngay_gio_bay.date(), gioDi=ngay_gio_bay.time()
                               , ma_datcho=ma_datcho, hk_ve = hk_ve, soluong = len(hk_ve), hangve = hk_ve[0].loaiHang)


@app.route("/Email")
def gui_Email():
    venl = session.get("ve_banNgl")
    vete = session.get("ve_banTreEm")
    print('daydaow')
    print(session.get("madatcho"))
    SendEmail.send_mail(session.get("lienHe").get("Email"), madatcho=session.get("madatcho"),
                        nguoi_Lon=session.get('nguoiLon'), tre_Em=session.get('treEm'), cbs = session.get('flight'), soGhe=session.get('GHE'),
                        venl = venl,vete = vete)
    delete_session()
    return redirect('/login')




###############################API


@app.route('/api/diadiem',methods=['get'])
def load_destinations():
    destinations = []
    for des in dao.get_destination():
        destinations.append({
            'address':des.diaChi
        })
    return jsonify(destinations)


@app.route('/api/timcb',methods=['POST'])
def load_macb():
    data = request.json
    macbs = []
    for cb in dao.get_ChuyenBay_By_TuyenBayID(data.get('tuyen')):
        macbs.append({
            'macb':cb.MaCB
        })
    return jsonify(macbs)

@app.route('/api/countghe',methods=['POST'])
def load_soluongghe():
    data = request.json
    print(data)
    soluongghe = {
        'hang1': dao.count_so_ghe_all(data.get('idmb'),1).soghe,
        'hang2': dao.count_so_ghe_all(data.get('idmb'),2).soghe
    }
    return jsonify(soluongghe)


@app.route('/api/sanbay')
def load_tensb():
    tensb = []
    for sb in dao.get_destination():
        tensb.append({
            'masb':sb.tenSB
        })
    return jsonify(tensb)



@app.route('/api/maybay')
def load_maybay():
    tenmb = []
    for mb in dao.get_MayBayLL():
        tenmb.append({
            'mamb':mb.maMb,
            'tenmb':mb.tenMB
        })
        print(tenmb)
    return jsonify(tenmb)


@app.route('/api/quydinh')
def load_quydinh():
    rl = dao.get_rule()
    print(rl)
    rule = {
        'thoiGianBayToiThieu':rl.thoiGianBayToiThieu,
        'sanBayTG_ToiDa':rl.sanBayTG_ToiDa,
        'thoiGianDungToiThieu':rl.thoiGianDungToiThieu,
        'thoiGianDungToiDa':rl.thoiGianDungToiDa
    }
    print(rule)
    return jsonify(rule)



@app.route('/api/hangve',methods=['get'])
def load_ticketLevel():
    level = []
    for lev in dao.get_ticketLevel():
        level.append({
            'level': lev.loaiHang
        })
    return jsonify(level)




@app.route("/api/laplich", methods=['post'])
def add_LichBay():
    data = request.json
    print(data)
    print(len(data))
    id_cb = ''
    for i in range(len(data)):
        if data[i].get('id_chuyenbay') is not None:# cho nay viet dao luu thong tin lb
            id_cb = data[i].get('id_chuyenbay')
            print(data[i].get('sanbaybaytrunggian'))
            datetime_object = datetime.strptime(data[i].get('ngaygiodi'), '%Y-%m-%dT%H:%M')
            print(datetime_object)
            dao.luu_ThongTinLapLich(data[i].get('id_chuyenbay'), data[i].get('maybay'),session.get('idnv'),datetime_object,
                  data[i].get('thoigianbay'))
            print('anv')
            dao.luu_ThongTinSanBayTrungGian(data[i].get('sanbaybaytrunggian'),id_cb,data[i].get('thoigiandung'))
        else:#thong tin sbtg
            dao.luu_ThongTinSanBayTrungGian(data[i].get('sanbaybaytrunggian'), id_cb,
                                            data[i].get('thoigiandung'))
    return


@app.route('/laplich', methods=['post', 'get'])
def laplich():
    if request.method.__eq__("POST"):
        return redirect('/login')







################ADMIN


@login.user_loader
def load_user(user_id):
    return TaiKhoan.query.get(int(user_id))



@app.route("/sign_admin", methods=["post"])
def sign_admin():
    username = request.form.get("username")
    password = request.form.get("password")
    if request.method.__eq__("POST"):

        user = dao.check_login(username=username, password=password, role=UserRole.admin)

        if user:
            flask_login_user(user=user)
    return redirect("/admin")


if __name__ == '__main__':
    # with app.app_context():
    #   print(load_destinations())
     app.run(debug=True)