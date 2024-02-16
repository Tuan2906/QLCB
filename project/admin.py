from project.models import *
from project import admin, db,dao
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose, Admin, BaseView
from flask_login import logout_user, current_user
from flask import redirect,request


# sửa RelationShip bên lớp models lại

class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.admin)


class TaiKhoanView(AuthenticatedView):
    column_display_pk = True
    # column_labels = {
    #     'username': 'Mã chuyến bay',
    #     'password': 'Máy Bay',
    #     'avatar': 'Ga đi',
    # }
    # can_view_details = True
    # form_columns = ['username','password','avatar']


class NhanVienView(AuthenticatedView):
    column_display_pk = True


class NhanVienLapLichView(AuthenticatedView):
    column_display_pk = True


class NhanVienView(AuthenticatedView):
    column_display_pk = True


class NhanVienBanVeView(AuthenticatedView):
    column_display_pk = True


class MayBayView(AuthenticatedView):
    column_display_pk = True


class SanBayView(AuthenticatedView):
    column_display_pk = True
    # column_list = ['SBTGs']



class SanBayTrungGianView(AuthenticatedView):
    column_display_pk = True

class TuyenBayView(AuthenticatedView):
    column_display_pk = True
    column_searchable_list = ['maTuyenBay']
    column_filters = ['maTuyenBay']
    column_editable_list = ['maTuyenBay']




class ChuyenBayView(AuthenticatedView):
    column_display_pk = True
    column_searchable_list = ['MaCB']
    column_filters = ['MaCB']
    column_editable_list = ['MaCB']

class HangVeView(AuthenticatedView):
    column_display_pk = True


class GiaVeView(AuthenticatedView):
    column_display_pk = True


class ChuyenBay_GiaVeView(AuthenticatedView):
    column_display_pk = True


class ChuyenBay_SBTrungGianView(AuthenticatedView):
    column_display_pk = True


class NguoiLonView(AuthenticatedView):
    column_display_pk = True


class TreEmView(AuthenticatedView):
    column_display_pk = True


class PhieuDatChoView(AuthenticatedView):
    column_display_pk = True


class VeBanView(AuthenticatedView):
    column_display_pk = True


class GheView(AuthenticatedView):
    column_display_pk = True


class MayBay_GheView(AuthenticatedView):
    column_display_pk = True


class VeDatView(AuthenticatedView):
    column_display_pk = True

class LichBayView(AuthenticatedView):
    column_display_pk = True
    form_columns = ['NgayBay', 'thoiGianBay', 'trangThai','id_MayBay','id_ChuyenBay','id_NVLL']
    column_searchable_list = ['NgayBay', 'trangThai','id_ChuyenBay']
    column_filters = ['NgayBay', 'trangThai','id_ChuyenBay']
    column_editable_list = ['NgayBay', 'trangThai','id_ChuyenBay']

class QuyDinhView(AuthenticatedView):
    column_display_pk = True


class LichBay_GiaVeView(AuthenticatedView):
    column_display_pk = True

#
# class MyAdminIndexView(AdminIndexView):
#     @expose("/")
#     def index(self):
#         return self.render('admin/index.html')

class statistical(BaseView):
    @expose("/")
    def index(self):
        if request.args.get("month"):
            month = request.args.get("month", datetime.now())
        else:
            month = datetime.now().month
        return self.render('admin/thongke.html' ,general_states=dao.thongkebaocao(m=month),sum =dao.tong_doanh_thu(month))
    def is_accessible(self):
        return current_user.is_authenticated

class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated



admin.add_view(TaiKhoanView(TaiKhoan, db.session, name='Tài khoản'))
admin.add_view(TuyenBayView(TuyenBay, db.session, name='Tuyến bay'))
admin.add_view(ChuyenBayView(ChuyenBay, db.session, name='Chuyến bay'))
admin.add_view(MayBayView(MayBay, db.session, name='Máy bay'))
admin.add_view(LichBayView(LichBay, db.session, name='Lịch bay'))
admin.add_view(QuyDinhView(QuyDinh, db.session, name='Quy định'))
admin.add_view(GiaVeView(GiaVe, db.session, name='Giá Vé'))
admin.add_view(LichBay_GiaVeView(LichBay_GiaVe, db.session, name='Giá vé của lịch'))
admin.add_view(HangVeView(HangVe, db.session, name='Hạng vé'))

admin.add_view(LogoutView(name="Đăng xuất"))
admin.add_view(statistical(name="Thống kê doanh thu"))
