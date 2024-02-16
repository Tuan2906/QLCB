import enum
import hashlib

from flask_login import UserMixin
from sqlalchemy import (Integer, Column, String, Boolean, DateTime,
                        Float, ForeignKey, Enum, Date)
from sqlalchemy.orm import relationship, backref
from datetime import datetime, date
from project import db, app


# doi vs 1 N thi ben phia ben co 1 se thiet lap relationship con phia ben N se thiet lap khoa ngoai
# doi VS N N thi thu nhat phai khai bao trung gian ten_dat= db.Table('ten_bang', Colunm('ten_id',interger,ForeginKey('ten.id'),primary_key=true),
# Colum(tuong tu))
# thu 2 la phai relationship 2 bang vd thuoctinh=reklationship('tenbangthu2', secondary='ten_bang', lazy=subquery,backref=
# bacref('tenbangthu1',lazy=true)-> cai nay khai bao trong  bang 1  voi 1 thuoc tinh o 2 bang  relationship vs nhau
# trong backref dung de relatipnship cho bang 2

# lazy= true la no khong lay thang co quan he tru khi tac dong len thi se lay, false lay, subquwey lay nhung ma roi rac
# inset du lieu VD p=tenclass(tenthuoctinh='',...)
# db.session.add(p)
# db.session.commit()
# b1: thuc hien truy van trong cmd from BanVeMay.models import *
# b2: p= Tenclass.query.get(tencantim)
# de xem kq truy van thi p.__dict__
# t1=tentt.query.get(dulieucantim)
# doi voi do du lieu vao bang trung gian thi p.thuoctinh.append(t1)
# Sau do from Banvemaybay import db, db.session.add(p), db.session.commit()
# class Emloyee(db.Model):
#     __tablenam__= 'SinhVien'
#     stt = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(20), nullable=False)

class UserRole(enum.Enum):
    admin = 1
    laplich = 2
    banve = 3

class TaiKhoan(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1688179242/hclq65mc6so7vdrbp7hz.jpg')
    user_role = Column(Enum(UserRole), default=UserRole.admin)
    nhanvien = relationship("NhanVien", backref="TaiKhoan", uselist=False)

    def __str__(self):
        return self.username


class NhanVien(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    hovaTen = Column(String(20), nullable=False)
    ngaySinh = Column(Date)
    gioiTinh = Column(String(5), nullable=False)
    luong = Column(Integer, nullable=False)
    id_TK = Column(Integer, ForeignKey(TaiKhoan.id), nullable=False,unique=True)
    lichBays = relationship("LichBay", backref="NhanVien", lazy=True)
    vebans = relationship("VeBan", backref="NhanVien", lazy=True)


class MayBay(db.Model):
    maMb = Column(Integer, primary_key=True, autoincrement=True)
    tenMB = Column(String(20), nullable=False)
    lichBays = relationship("LichBay", backref="MayBay", lazy=False)


class SanBay(db.Model):
    maSB = Column(Integer, primary_key=True, autoincrement=True)
    tenSB = Column(String(30), nullable=False)
    diaChi = Column(String(20), nullable=False)
    # tuyen_BayDi = relationship('TuyenBay', backref='SanBay', lazy=True)
    # # tuyen_BayDen = relationship('TuyenBay', backref='SanBayDen', lazy=True)
    SBTGs = relationship("SanBayTrungGian", backref="SanBay")


class TuyenBay(db.Model):
    maTuyenBay = Column(Integer, primary_key=True, autoincrement=True)
    id_SbDi = Column(Integer, ForeignKey(SanBay.maSB))
    id_SbDen = Column(Integer, ForeignKey(SanBay.maSB))
    # Column('ChuyenBay_MaCB', String(20), ForeignKey(SanBay.maSB))

    chuyenBays = relationship("ChuyenBay", backref="TuyenBay", lazy=False)
    chitiet_DoanhThu = relationship("ChiTietDoanhThu", backref="TuyenBay", lazy=True)


class ChuyenBay(db.Model):
    MaCB = Column(String(10), primary_key=True)
    id_TuyenBay = Column(Integer, ForeignKey(TuyenBay.maTuyenBay), nullable=False)
    SBTGs = relationship("SanBayTrungGian", backref="ChuyenBay")
    lichbays = relationship("LichBay", backref="ChuyenBay", lazy=True)


class LichBay(db.Model):
    MaLB = Column(Integer, primary_key=True, autoincrement=True)
    NgayBay = Column(DateTime, nullable=False,unique=True)
    thoiGianBay = Column(Integer, nullable=False)
    trangThai = Column(String(20))
    id_MayBay = Column(Integer, ForeignKey(MayBay.maMb), nullable=False)
    id_ChuyenBay = Column(String(10), ForeignKey(ChuyenBay.MaCB), nullable=False)
    id_NVLL = Column(Integer, ForeignKey(NhanVien.id), nullable=False)
    lichbay_GiaVe = relationship("LichBay_GiaVe", backref="LichBay", lazy=False)
    vemaybay = relationship("VeDat", backref="LichBay", lazy=True)
    hoadons = relationship("HoaDon", backref="LichBay", lazy=True)


class SanBayTrungGian(db.Model):
    maSBTG = Column(Integer,primary_key=True,autoincrement=True)
    thoiGianDung = Column(Integer, nullable=False)
    GhiChu = Column(String(20), nullable=False, default="Dang")
    maSb = Column(Integer, ForeignKey(SanBay.maSB), nullable=False)
    maCb = Column(String(10), ForeignKey(ChuyenBay.MaCB), nullable=False)


class HangVe(db.Model):
    id = Column(Integer, primary_key=True)
    loaiHang = Column(String(10), nullable=False)
    lichBay_GiaVe = relationship("LichBay_GiaVe", backref="HangVe", lazy=True)
    veDat = relationship("VeDat", backref="HangVe", lazy=True)


class GiaVe(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    Gia = Column(Float, nullable=False)
    lichBay_GiaVe = relationship("LichBay_GiaVe", backref="GiaVe", lazy=True)


class LichBay_GiaVe(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngayApDung = Column(Date, nullable=False)
    ngayKetThuc = Column(Date, nullable=False)
    SoLuongGhe = Column(Integer, nullable=False)
    id_HangVe = Column(Integer, ForeignKey(HangVe.id), nullable=False)
    id_LichBay = Column(Integer, ForeignKey(LichBay.MaLB), nullable=False)
    id_GiaVe = Column(Integer, ForeignKey(GiaVe.id), nullable=False)


# chuyenBay_SBtrungGian=db.Table('chuyenBaySBTG',
#         Column('ChuyenBay_MaCB',String(20),ForeignKey(ChuyenBay.MaCB)),
#         Column('ma_SBTG',Integer,ForeignKey(SanBayTrungGian.maSBTG)))

class HanhKhach(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    gioiTinh = Column(String(3), nullable=False)
    hoTen = Column(String(30), nullable=False)
    ngSinh = Column(Date, nullable=True)


class NguoiLon(db.Model):
    id_NguoiLon= Column(Integer,ForeignKey(HanhKhach.id),primary_key=True)
    CCCD = Column(String(13), unique=True, nullable=False)
    emails = relationship("Email", backref='NguoiLon', lazy=True)
    sdts = relationship("SoDienThoai", backref='NguoiLon', lazy=True)
    childrends = relationship("TreEm", backref='NguoiLon', lazy=True)


class TreEm(db.Model):
    id_TreEm= Column(Integer,ForeignKey(HanhKhach.id),primary_key=True)
    nguoiLon_id = Column(Integer, ForeignKey(NguoiLon.id_NguoiLon))


class PhieuDatCho(db.Model):
    MaPhieu = Column(String(15), primary_key=True)
    NgMua = Column(DateTime, nullable=False, default=datetime.now())
    TrangThai = Column(String(20), nullable=False)  # dung de kiem tra la phieu nay da xu li chua
    veDats = relationship("VeDat", backref="PhieuDatCho", lazy=True)


class VeDat(db.Model):
    MaVe = Column(String(20), primary_key=True)
    NgDat = Column(DateTime, nullable=False, default=datetime.now())
    gheDaDat= Column(String(4))
    TinhTrangVe = Column(String(20))
    lichbay_id = Column(Integer, ForeignKey(LichBay.MaLB), nullable=False)
    hanhKhach_id = Column(Integer, ForeignKey(HanhKhach.id))
    maHangVe = Column(Integer, ForeignKey(HangVe.id), nullable=False)
    maphieu = Column(String(15), ForeignKey(PhieuDatCho.MaPhieu), nullable=False)
    veban = relationship("VeBan", backref="VeDat", uselist=False)


class VeBan(db.Model):
    MaVe = Column(String(20), ForeignKey(VeDat.MaVe), primary_key=True)
    id_NVBV = Column(Integer, ForeignKey(NhanVien.id), nullable=False)


class Ghe(db.Model):
    id = Column(Integer, primary_key=True)

class MayBay_Ghe(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ghe_id = Column(Integer, ForeignKey(Ghe.id), primary_key=True, nullable=False)
    dayGhe= Column(String(3),nullable=False)
    hangVe_id= Column(Integer,ForeignKey(HangVe.id),nullable=False)
    mayBay_id = Column(Integer, ForeignKey(MayBay.maMb), primary_key=True, nullable=False)

class HoaDon(db.Model):
    id = Column(String(10), primary_key=True)
    ngayLap = Column(Date, default=date.today())
    tongTien = Column(Float, default=0)
    NgHetHanThanhToan = Column(Date, nullable=False)
    lichBay = Column(Integer, ForeignKey(LichBay.MaLB), nullable=False)


class BaoCaoDoanhThu(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngayXuat = Column(Date, default=date.today())
    thangDoanhThu = Column(Date, nullable=False)
    tongDoanhThu = Column(Float, default=0)
    chitiet_DoanhThu = relationship("ChiTietDoanhThu", backref="BaoCaoDoanhThu", lazy=True)


class ChiTietDoanhThu(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tuyenBay_id = Column(Integer, ForeignKey(TuyenBay.maTuyenBay), primary_key=True, nullable=False)
    BaoCao_id = Column(Integer, ForeignKey(BaoCaoDoanhThu.id), primary_key=True, nullable=False)
    soLuotBay = Column(Integer, default=0)  ##số lượt bay
    tyLe = Column(Float, default=0)  ##tỷ lệ
    doanhThu = Column(Float, default=0)


class Email(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(50), nullable=False)
    id_kh = Column(Integer, ForeignKey(NguoiLon.id_NguoiLon), nullable=False)


class SoDienThoai(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    sdt = Column(String(14))
    id_kh = Column(Integer, ForeignKey(NguoiLon.id_NguoiLon), nullable=False)


# Quy định này chỉ tạo 1 lần và lan sau chi duoc update
class QuyDinh(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    thoiGianChamNhatDatVe = Column(Integer, nullable=False, unique=True)
    thoiGianChamNhatBanVe = Column(Integer, nullable=False, unique=True)
    thoiGianBayToiThieu = Column(Integer, nullable=False, unique=True)
    sanBayTG_ToiDa = Column(Integer, nullable=False, unique=True)
    thoiGianDungToiThieu = Column(Integer, nullable=False, unique=True)
    thoiGianDungToiDa = Column(Integer, nullable=False, unique=True)


if __name__ == '__main__':
    with app.app_context():
         db.create_all()
        # u = TaiKhoan(username='admin', password=hashlib.md5("abc".strip().encode("utf-8")).hexdigest(),
        #              user_role=UserRole.admin)
        #
        # # nv = NhanVien(hovaTen='Hoang Nhi', ngaySinh='2003-04-04', gioiTinh='nam', luong=100000, id_TK=1)
        # db.session.add(u)
        # db.session.commit()
