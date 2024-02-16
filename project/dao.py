import hashlib

from project.models import *
from project import app,db
from sqlalchemy import func,and_, distinct,tuple_
from flask import jsonify
from datetime import datetime, timedelta


def get_rule():
    return QuyDinh.query.first()


############# Truong
def get_destination ():
    return  SanBay.query.all()

def get_MayBayLL():
    return MayBay.query.all()

def get_ticketLevel():
    return HangVe.query.all()

def get_LichBay():
    return LichBay.query.all()

def filter_LichBay_With_Valid_Time(Startdate,dateNow, id_nv):
    ListLichBay = []
    if id_nv is not None:
        rule = get_rule().thoiGianChamNhatBanVe
    else:
        rule = get_rule().thoiGianChamNhatDatVe
    for lb in get_LichBay():
        dateNow = dateNow.replace(tzinfo=None)
        dateDelta = (lb.NgayBay - dateNow)
        if lb.NgayBay.day == Startdate.day and lb.NgayBay.month  == Startdate.month and lb.NgayBay.year == Startdate.year:
            further = abs((dateDelta.total_seconds()) / 3600)
            if(further > rule):
                ListLichBay.append(lb)
    return ListLichBay


def count_So_Ghe_Da_Dat(HangVe, year, month, day):
    return db.session.query(VeDat.lichbay_id,
                     VeDat.maHangVe,
                     LichBay.id_ChuyenBay,
                     LichBay_GiaVe.SoLuongGhe,
                     func.count(VeDat.MaVe).label('SoLuongVeDaDat')
                            ).join(LichBay, LichBay.MaLB == VeDat.lichbay_id).join(
                        LichBay_GiaVe,and_(LichBay_GiaVe.id_LichBay == LichBay.MaLB, LichBay_GiaVe.id_HangVe == VeDat.maHangVe)
                    ).filter(VeDat.maHangVe == HangVe,
                            func.year(LichBay.NgayBay) == year,
                            func.month(LichBay.NgayBay) == month,
                            func.day(LichBay.NgayBay) == day
                    ).group_by(VeDat.lichbay_id,
                      VeDat.maHangVe,
                     LichBay.id_ChuyenBay,
                     LichBay_GiaVe.SoLuongGhe
               ).all()


def get_LichBay_with_ChuyenBays(listChuyenBay, listLichBay_filter_by_time):
    listLB = []
    for soHieu in listChuyenBay:
        for lb in listLichBay_filter_by_time:
            if soHieu.MaCB == lb.id_ChuyenBay:
                listLB.append(lb)
    return listLB

def get_GiaVe (HangVe):
    return db.session.query(LichBay.MaLB, LichBay_GiaVe.id_HangVe, GiaVe.Gia) \
                        .join(LichBay_GiaVe, LichBay.MaLB == LichBay_GiaVe.id_LichBay) \
                        .join(GiaVe, LichBay_GiaVe.id_GiaVe == GiaVe.id) \
                        .filter(LichBay_GiaVe.id_HangVe == HangVe) \
                        .all()


def get_Id_HangVe (hangve):
    for hang in get_ticketLevel():
        if hang.loaiHang == hangve:
            return hang.id


def get_SanBayTrungGian(id_chuyenBay):
    return db.session.query(SanBay.tenSB, SanBay.diaChi, SanBayTrungGian.thoiGianDung
                            , SanBayTrungGian.GhiChu, SanBayTrungGian.maCb) \
                        .join(SanBayTrungGian, SanBay.maSB == SanBayTrungGian.maSb) \
                        .filter(SanBayTrungGian.maCb == id_chuyenBay) \
                        .all()


def get_MayBay (id_mb):
    return MayBay.query.filter(MayBay.maMb.__eq__(id_mb)).first().tenMB

def get_Valid_lichBay(start,end,timeNow,tongnguoi,tiklevel, startDate,idnv):
    # tim lich bay theo
    # thoi gian dung quy dinh
    # lich bay còn cho : tong ở lichbay-giave  - soluong (ve) r so sanh voi tong nguoi
    startDate = datetime.strptime(str(startDate), '%Y-%m-%d %H:%M:%S')
    print(startDate.day)
    tiklevel = get_Id_HangVe(tiklevel)
    print(tiklevel)
    soHieuChuyenBay = get_ChuyenBay_By_TuyenBay(start,end) # chuyem dung tuyen
    print(soHieuChuyenBay)
    ListLB_validTime  = filter_LichBay_With_Valid_Time(startDate,timeNow,idnv) # lich dung time
    print(ListLB_validTime)

    ListSoLuongVeDaDat = count_So_Ghe_Da_Dat(tiklevel,startDate.year,startDate.month,startDate.day) #TrongMotLich
    print(ListSoLuongVeDaDat)

    # So luong lich bay theo soHieu cua tuyen dc chon
    listLB = get_LichBay_with_ChuyenBays(soHieuChuyenBay,ListLB_validTime)
    print(listLB)

    # So lich bay còn ghe
    LichBay_Valid_ConGhe = [dict1 for dict2 in  ListSoLuongVeDaDat for dict1 in listLB
                            if dict1.MaLB == dict2.lichbay_id and dict2.SoLuongGhe - dict2.SoLuongVeDaDat >= tongnguoi]
    #
    print(LichBay_Valid_ConGhe)

    # So lich bay chua co ve
    listLichBayDaDat = []
    for obj in ListSoLuongVeDaDat:
        listLichBayDaDat.append(obj.lichbay_id)

    print(listLichBayDaDat)

    LichBay_Valid_GheTrong= [lb for lb in  listLB if lb.MaLB not in listLichBayDaDat]

    print(LichBay_Valid_GheTrong)

    result = LichBay_Valid_ConGhe + LichBay_Valid_GheTrong



    finalRes = []

    for lb in result:
        for gv in get_GiaVe(tiklevel):
            if lb.MaLB == gv.MaLB:
                finalRes.append({
                    'MaLB' : lb.MaLB,
                    'MaCB': lb.id_ChuyenBay,
                    'MayBay': get_MayBay(lb.id_MayBay),
                    'NgayKhoiHanh': lb.NgayBay,
                    'ThoiGianDi' : lb.thoiGianBay,
                    'HangVe:' :tiklevel,
                    'SanBayTrungGian': get_SanBayTrungGian(lb.id_ChuyenBay),
                    'GiaVe' : gv.Gia
                })
    return finalRes


def get_ChuyenBay_By_TuyenBayID(ID):
    return ChuyenBay.query.filter(ChuyenBay.id_TuyenBay.__eq__(ID)).all()

def get_ChuyenBay_By_TuyenBay(start,end):
    return ChuyenBay.query.filter(ChuyenBay.id_TuyenBay.__eq__(get_TuyenBay_By_SanBay(start,end))).all()


def get_TuyenBay_By_SanBay(start, end):
    sbdi = get_Id_By_Diadiem(start)
    sbden = get_Id_By_Diadiem(end)
    return TuyenBay.query.filter(TuyenBay.id_SbDi.__eq__(sbdi),TuyenBay.id_SbDen.__eq__(sbden)).first().maTuyenBay

def get_Id_By_Diadiem (des):
    return SanBay.query.filter(SanBay.diaChi.__eq__(des)).first().maSB


def get_HanhKhachNguoiLon_By_MaPhieu (maphieu):
    return db.session.query(VeDat.maphieu,VeDat.maHangVe,HanhKhach.id, HanhKhach.hoTen
                                   , HanhKhach.ngSinh, HanhKhach.gioiTinh, NguoiLon.CCCD
                                     , SoDienThoai.sdt).distinct() \
                        .join(HanhKhach, VeDat.hanhKhach_id.__eq__(HanhKhach.id))\
                        .join(NguoiLon,HanhKhach.id.__eq__(NguoiLon.id_NguoiLon))\
                        .join(SoDienThoai, SoDienThoai.id_kh.__eq__(HanhKhach.id)) \
                        .filter(VeDat.maphieu.__eq__(maphieu))\
                        .all()


def get_HanhKhachTreEm_By_MaPhieu(maphieu):
    return db.session.query(VeDat.maphieu,VeDat.maHangVe, HanhKhach.id, HanhKhach.hoTen
                            , HanhKhach.ngSinh, HanhKhach.gioiTinh, NguoiLon.id_NguoiLon
                            ).distinct() \
        .join(HanhKhach, VeDat.hanhKhach_id.__eq__(HanhKhach.id)) \
        .join(TreEm, HanhKhach.id.__eq__(TreEm.id_TreEm)) \
        .join(NguoiLon, TreEm.nguoiLon_id.__eq__(NguoiLon.id_NguoiLon)) \
        .filter(VeDat.maphieu.__eq__(maphieu)) \
        .all()


def get_NguoiBaoHo_By_ID (ID):
    return HanhKhach.query.filter(HanhKhach.id.__eq__(ID)).first().hoTen

def get_lichbay_By_MaPhieu(maphieu):
    return db.session.query(VeDat.lichbay_id,
                            LichBay.NgayBay
                            , LichBay.thoiGianBay, LichBay.id_ChuyenBay, LichBay.id_MayBay
                            ).distinct() \
        .join(LichBay, VeDat.lichbay_id.__eq__(LichBay.MaLB)) \
        .join(LichBay_GiaVe, LichBay.MaLB.__eq__(LichBay_GiaVe.id_LichBay))\
        .filter(VeDat.maphieu.__eq__(maphieu)) \
        .all()

def get_TuyenBay_By_IDChuyenBay(ID):
    return (ChuyenBay.query.join(TuyenBay, ChuyenBay.id_TuyenBay.__eq__(TuyenBay.maTuyenBay))
            .filter(ChuyenBay.MaCB.__eq__(ID))
             .add_columns(ChuyenBay.MaCB, TuyenBay.id_SbDi, TuyenBay.id_SbDen).first())

def get_SanBay_By_ID(ID):
    return SanBay.query.filter(SanBay.maSB.__eq__(ID)).first().diaChi


def count_so_ghe (id_mb):
    sub_query = db.session.query(db.func.count(MayBay_Ghe.ghe_id).label('maxghe'), MayBay_Ghe.dayGhe) \
        .filter(MayBay_Ghe.mayBay_id.__eq__(id_mb)) \
        .group_by(MayBay_Ghe.dayGhe) \
        .subquery()

    return db.session.query(db.func.MAX(sub_query.c.maxghe)).scalar()

def count_so_ghe_all(id_mb, hang):
    return  (db.session.query(MayBay_Ghe.hangVe_id,(db.func.count(MayBay_Ghe.ghe_id).label('soghe'))).filter(
        MayBay_Ghe.hangVe_id == hang,
        MayBay_Ghe.mayBay_id == id_mb
    ).group_by(
        MayBay_Ghe.hangVe_id
    )
    .first())


def get_DayGhe_In_MayBay(id_mb):
    return (db.session.query(MayBay_Ghe.dayGhe).distinct()
            .filter(MayBay_Ghe.mayBay_id.__eq__(id_mb))
            .order_by( MayBay_Ghe.dayGhe)
            .all())


def get_ghe_mot_day(id_mb,day):
    return (db.session.query(MayBay_Ghe.dayGhe, MayBay_Ghe.ghe_id, MayBay_Ghe.hangVe_id)
            .filter(MayBay_Ghe.mayBay_id.__eq__(id_mb) and MayBay_Ghe.dayGhe.__eq__(day)).all())


def get_Ghe_In_MayBay(id_mb):
    return (db.session.query(MayBay_Ghe.dayGhe, MayBay_Ghe.ghe_id, MayBay_Ghe.hangVe_id) \
                    .filter(MayBay_Ghe.mayBay_id.__eq__(id_mb)) \
                    .order_by(MayBay_Ghe.ghe_id, MayBay_Ghe.dayGhe) \
                    .all())


def get_hangGhe(id_mb):
    return (db.session.query(MayBay_Ghe.dayGhe, MayBay_Ghe.hangVe_id, MayBay_Ghe.ghe_id) \
                    .distinct()
                    .filter(MayBay_Ghe.mayBay_id.__eq__(id_mb), MayBay_Ghe.hangVe_id == 1) \
                    .all())


def get_hoten_by_account(username,password):
    return db.session.query(NhanVien.hovaTen, NhanVien.id) \
        .join(TaiKhoan, NhanVien.id_TK == TaiKhoan.id) \
        .filter(TaiKhoan.username.__eq__(username),
                TaiKhoan.password.__eq__(password)).first()


def get_ID_MayBay(tenmb):
    return MayBay.query.filter(MayBay.tenMB.__eq__(tenmb)).first().maMb



def get_vedat(Lichbay_id, maPhieu):
    return VeDat.query.filter(VeDat.maphieu.__eq__(maPhieu), VeDat.lichbay_id.__eq__(Lichbay_id))


def get_tinhtrangve (Lichbay_id, maPhieu):
    return get_vedat(Lichbay_id,maPhieu).first().TinhTrangVe


def get_LichBay_ByID(ID):
    return LichBay.query.filter(LichBay.MaLB == ID).first()



def Ghe_DaDat (LichBay_id): # theo lich
    return db.session.query(VeDat.gheDaDat, VeDat.TinhTrangVe)\
                            .filter(VeDat.lichbay_id.__eq__(LichBay_id),VeDat.TinhTrangVe.__eq__('da xu ly'))\
                            .all()


def Save_Ghe(maPhieu, CacGhe, id_lb):
    print('Trong save ghe')
    print(maPhieu)
    print(CacGhe)
    print(id_lb)
    listVeMB = get_vedat(id_lb,maPhieu).all()
    print(listVeMB)
    for i in range(len(CacGhe)):
        listVeMB[i].gheDaDat = CacGhe[i]
        listVeMB[i].TinhTrangVe = 'da xu ly'
    db.session.commit()



def get_Mave_for_Hanhkhach (Lichbay_id, maphieu):
    return db.session.query(VeDat.MaVe,HanhKhach.hoTen, VeDat.gheDaDat, HangVe.loaiHang)\
        .join(HanhKhach, VeDat.hanhKhach_id.__eq__(HanhKhach.id))\
        .join(HangVe, VeDat.maHangVe.__eq__(HangVe.id))\
        .filter(VeDat.lichbay_id.__eq__(Lichbay_id), VeDat.maphieu.__eq__(maphieu))\
        .all()



def thongkebaocao(m):
    total_revenue = db.session.query(func.sum(HoaDon.tongTien)).scalar()
    k = 100 / total_revenue
    subquery1 = db.session.query(
        func.sum(HoaDon.tongTien).label('tongtientheolich'),
        HoaDon.lichBay
    ).filter(
        func.MONTH(HoaDon.ngayLap) == m
    ).group_by(
        HoaDon.lichBay
    ).subquery()

    subquery2 = db.session.query(
        func.count(LichBay.MaLB).label('solichmotchuyen'),
        func.sum(subquery1.c.tongtientheolich).label('tongtientheochuyen'),
        LichBay.id_ChuyenBay
    ).join(
        subquery1, subquery1.c.lichBay == LichBay.MaLB
    ).group_by(
        LichBay.id_ChuyenBay
    ).subquery()

    return db.session.query(
        ChuyenBay.id_TuyenBay,
        func.sum(subquery2.c.tongtientheochuyen).label('doanhthu'),
        func.sum(subquery2.c.solichmotchuyen).label('sochuyenmottuyen'),
        (func.sum(subquery2.c.tongtientheochuyen) * k).label('tongtientheotuyen')
    ).join(
        subquery2, subquery2.c.id_ChuyenBay == ChuyenBay.MaCB
    ).group_by(
        ChuyenBay.id_TuyenBay
    ).all()


def tong_doanh_thu(m):
    tong = 0
    for i in thongkebaocao(m):
        tong+=i.doanhthu
    return tong






###################################
def luu_ThongTinNguoiLon(name, gioitinh, ngaySinh, CCCD):
    can_Cuoc = NguoiLon.query.filter(NguoiLon.CCCD.__eq__(CCCD)).first()
    if can_Cuoc is None:
        khachangs = HanhKhach(hoTen=name, gioiTinh=gioitinh, ngSinh=ngaySinh)
        db.session.add(khachangs)
        db.session.commit()
        # print(khachangs.id)
        nguoilon = NguoiLon(id_NguoiLon=khachangs.id, CCCD=CCCD)
        db.session.add(nguoilon)
        db.session.commit()
        return khachangs.id
    else:
        return can_Cuoc.id_NguoiLon


def luu_ThongTinTreEm(name, gioiTinh, ngaySinh, CCCD):
    global khachangs
    if CCCD is not None and name is not None and gioiTinh is not ngaySinh is not None:
        Nglon = NguoiLon.query.filter(NguoiLon.CCCD.__eq__(CCCD)).first()
        khachangs = HanhKhach(hoTen=name, gioiTinh=gioiTinh, ngSinh=ngaySinh)
        db.session.add(khachangs)
        db.session.commit()
        treEm = TreEm(id_TreEm=khachangs.id, nguoiLon_id=Nglon.id_NguoiLon)
        db.session.add(treEm)
        db.session.commit()
    return khachangs.id


def luu_ThongTinEmail(ten, CCCD):
    cancuoc = NguoiLon.query.filter(NguoiLon.CCCD.__eq__(CCCD)).first()
    eml = Email.query.filter(Email.ten.__eq__(ten)).first()
    if eml is None:
        email = Email(ten=ten, id_kh=cancuoc.id_NguoiLon)
        db.session.add(email)
        db.session.commit()
    else:
        return


def luu_ThongTinSDT(sodienthoai, CCCD):
    cancuoc = NguoiLon.query.filter(NguoiLon.CCCD.__eq__(CCCD)).first()
    Sdt = SoDienThoai.query.filter(SoDienThoai.sdt.__eq__(sodienthoai)).first()
    if Sdt is None:
        SDT = SoDienThoai(sdt=sodienthoai, id_kh=cancuoc.id_NguoiLon)
        db.session.add(SDT)
        db.session.commit()
    else:
        return


def luu_ThanhToan(mahd,thanhtien, ngayhethan, id_LichBay):
    thanhtoan = HoaDon(id=mahd, tongTien=thanhtien,
                       NgHetHanThanhToan=ngayhethan, lichBay=id_LichBay)
    db.session.add(thanhtoan)
    db.session.commit()
    return thanhtoan.id


def truyvan_HanhKhach(CCCD):
    can_Cuoc = NguoiLon.query.filter(NguoiLon.CCCD.__eq__(CCCD)).first()
    if can_Cuoc is None:
        return False
    else:
        return can_Cuoc


def truyVanMaPDC(maDaCho):
    ma_datcho = PhieuDatCho.query.filter(PhieuDatCho.MaPhieu.__eq__(maDaCho)).first()
    if ma_datcho is None:
        return '1'
    else:
        return ma_datcho.MaPhieu

def truyVanMaHangVe(loai_Hang):
    if loai_Hang is not None:
        id_HangVe = HangVe.query.filter(HangVe.loaiHang.__eq__(loai_Hang)).first()
        return id_HangVe.id


def luu_PhieuDatCho(maphieu, trangThai):
    phieuDatCho = PhieuDatCho(MaPhieu=maphieu, TrangThai=trangThai)

    db.session.add(phieuDatCho)
    db.session.commit()


def luu_ThongTinVeDat(mave, lichbay, id_HK, maphieu, mahangve):
    Ve = VeDat(MaVe=mave, lichbay_id=lichbay,
               hanhKhach_id=id_HK,
               maphieu=maphieu, maHangVe=mahangve,TinhTrangVe='xu ly')
    db.session.add(Ve)
    db.session.commit()


def luu_ThongTinVeBan(mave, lichbay, id_HK, maphieu, mahangve, id_NVBV, soGhe):
    ve_dat = VeDat(MaVe=mave, lichbay_id=lichbay, hanhKhach_id=id_HK,
                   maphieu=maphieu, maHangVe=mahangve, TinhTrangVe="da xu ly", gheDaDat=soGhe)
    db.session.add(ve_dat)
    db.session.commit()
    veBan = VeBan(MaVe=ve_dat.MaVe, id_NVBV=id_NVBV)
    db.session.add(veBan)
    db.session.commit()




def truyvan_NgayGioBay(ngaygio):
    ngaygio = LichBay.query.filter(LichBay.NgayBay.__eq__(ngaygio)).first()
    if ngaygio:
        return False
    return True


def Lay_idMayBay(tenMB):
    return MayBay.query.filter(MayBay.tenMB.__eq__(tenMB)).first()


def luu_ThongTinLapLich(id_CB, tenMB, id_NVLL, ngaygio, thoigianbay):
    if truyvan_NgayGioBay(ngaygio=ngaygio):
        print(id_CB)
        print(tenMB)
        print(id_NVLL)
        print(thoigianbay)
        print(Lay_idMayBay(tenMB=tenMB).maMb)
        print(ngaygio)
        lap_lich = LichBay(id_ChuyenBay=id_CB, id_MayBay=Lay_idMayBay(tenMB=tenMB).maMb, NgayBay=ngaygio,
                           thoiGianBay=thoigianbay, id_NVLL=id_NVLL)
        db.session.add(lap_lich)
        db.session.commit()


def Lay_idSanBay(tenSanBay):
    print(SanBay.query.filter(SanBay.tenSB.__eq__(tenSanBay.strip())).first())
    return SanBay.query.filter(SanBay.tenSB.__eq__(tenSanBay.strip())).first()


def luu_ThongTinSanBayTrungGian(tenSanBay, id_CB, thoigiandung):
    print('day la dao')
    print(tenSanBay.strip())
    print(id_CB)
    print(thoigiandung)
    print(Lay_idSanBay(tenSanBay=tenSanBay).maSB)
    sb_tg = SanBayTrungGian(maCb=id_CB, maSb=Lay_idSanBay(tenSanBay=tenSanBay).maSB,thoiGianDung=thoigiandung)
    db.session.add(sb_tg)
    db.session.commit()




#########ADMIN
def get_user_by_id(user_id):
    return TaiKhoan.query.get(user_id)


def check_login(username, password, role=UserRole.admin):
    # password = hashlib.md5(password.strip().encode("utf-8")).hexdigest()

    result = db.session.query(TaiKhoan).select_from(TaiKhoan).\
        join(NhanVien, NhanVien.id_TK == TaiKhoan.id).\
        filter(TaiKhoan.username.__eq__(username.strip()),
             TaiKhoan.password.__eq__(password), TaiKhoan.user_role == role).first()
    return result

def auth_user(username, password):
    # password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    return TaiKhoan.query.filter(TaiKhoan.username.__eq__(username),
                             TaiKhoan.password.__eq__(password)).first()

if __name__ == '__main__':
    with app.app_context():
        a = get_Valid_lichBay('Hồ Chí Minh','Hà Nội',datetime.now(),1,'Thương gia','2024-01-10 10:00:00' )
        # print(get_lichbay_By_MaPhieu('kbquwq'))
        # print(get_lichbay_By_MaPhieu('mysokg')[0].id_ChuyenBay)
        # print(get_TuyenBay_By_IDChuyenBay(get_lichbay_By_MaPhieu('mysokg')[0].id_ChuyenBay))
        # print(get_SanBay_By_ID(get_TuyenBay_By_IDChuyenBay(get_lichbay_By_MaPhieu('mysokg')[0].id_ChuyenBay).id_SbDi))
        # print(get_SanBay_By_ID(get_TuyenBay_By_IDChuyenBay(get_lichbay_By_MaPhieu('mysokg')[0].id_ChuyenBay).id_SbDen))
        # print(get_HanhKhachNguoiLon_By_MaPhieu('bxcois'))
        # print(get_NguoiBaoHo_By_ID(get_HanhKhachTreEm_By_MaPhieu('kbquwq')[0].id_NguoiLon))
        # print(get_Ghe_In_MayBay(2))
        # print(get_hangGhe(2))
        # print(get_hoten_by_account('NVBV',123).hovaTen)
        # Save_Ghe('dmrqhp', [],3)
        # print(  Ghe_DaDat(26))
        # print(get_Mave_for_Hanhkhach(27,'dmrqhp'))
        # print(        thongkebaocao(1))
        # print(count_so_ghe_all(2,1).soghe)
        print(get_destination()[0].tenSB)