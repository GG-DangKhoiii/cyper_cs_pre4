class KhoaHoc:
    def __init__(self, maKhoaHoc, tenKhoaHoc, hinhThuc, hocPhi):
        self.maKhoaHoc = maKhoaHoc
        self.tenKhoaHoc = tenKhoaHoc
        self.hinhThuc = hinhThuc
        self.hocPhi = hocPhi
        

    def thongTinKhoaHoc(self):
        print(f"Mã khóa học: {self.maKhoaHoc}")
        print(f"Tên khóa học: {self.tenKhoaHoc}")
        print(f"Hình thức học: {self.hinhThuc}")
        print(f"Học phí: {self.hocPhi} VND")
        print("-" * 30)


class HocVien:
    def __init__(self, maHV, tenHV, ngaySinh, khoaHoc):
        self.maHV = maHV
        self.tenHV = tenHV
        self.ngaySinh = ngaySinh
        self.khoaHoc = khoaHoc

    def dangKyKhoaHoc(self, khoaHoc):
        self.khoaHoc.append(khoaHoc)  # Thêm khóa học vào danh sách
        print(f"Học viên {self.tenHV} đã đăng ký thành công khóa học: {khoaHoc.tenKhoaHoc}")

    def hienThiKhoaHoc(self):
        print(f"Học viên: {self.tenHV} (Mã: {self.maHV}) đã đăng ký các khóa học sau:")
        for khoaHoc in self.khoaHoc:
            print(f"- {khoaHoc.tenKhoaHoc} (Mã: {khoaHoc.maKhoaHoc})")
        print("-" * 30)
        
    def tinhTongHocPhi(self):
        tongHocPhi = sum(khoaHoc.hocPhi for khoaHoc in self.khoaHoc)
        print(f"Tổng học phí của học viên {self.tenHV}: {tongHocPhi} VND")
        return tongHocPhi        
        

class HocVienVIP(HocVien):
    def __init__(self, maHV, tenHV, ngaySinh, khoaHoc, uuDai):
        super().__init__(maHV, tenHV, ngaySinh, khoaHoc)
        self.uuDai = uuDai

    def tinhTongHocPhi(self):
        tongHocPhi = sum(khoaHoc.hocPhi for khoaHoc in self.khoaHoc)
        hocPhiUuDai = tongHocPhi * (1 - self.uuDai / 100)  # Áp dụng ưu đãi
        print(f"Tổng học phí sau ưu đãi {self.uuDai}% của học viên VIP {self.tenHV}: {hocPhiUuDai:.2f} VND")
        return hocPhiUuDai
   
# Hàm tính tổng học phí của tất cả học viên
def tinhTongHocPhiTatCa(hocVienList):
    tongHocPhiTatCa = 0
    for hocVien in hocVienList:
        tongHocPhiTatCa += hocVien.tinhTongHocPhi()
    print(f"Tổng học phí của tất cả học viên: {tongHocPhiTatCa:.2f} VND")
    return tongHocPhiTatCa

# Tạo các đối tượng khóa học
khoaHoc1 = KhoaHoc("KH001", "Lập trình Python", "Online", 6500000)
khoaHoc2 = KhoaHoc("KH002", "Phân tích Dữ liệu", "Offline", 2000000)

# Tạo các đối tượng học viên
hocVien1 = HocVien("HV001", "Tran Doan Dang Khoi", "25/12/1999", [])
hocVien2 = HocVien("HV002", "Tran Ngoc An Thinh ", "04/08/2003", [])

# Tạo các đối tượng học viên
hocVienVIPP = HocVienVIP("HVVIP01", "Doan Thi Kim Ngan", "22/09/1998", [], 20 )

# Đăng ký khóa học cho học viên
hocVien1.dangKyKhoaHoc(khoaHoc1)
hocVien1.dangKyKhoaHoc(khoaHoc2)

hocVien2.dangKyKhoaHoc(khoaHoc2)

hocVienVIPP.dangKyKhoaHoc(khoaHoc1)
hocVienVIPP.dangKyKhoaHoc(khoaHoc2)

# Hiển thị thông tin khóa học
print("Thông tin khóa học đã tạo:")
khoaHoc1.thongTinKhoaHoc()
khoaHoc2.thongTinKhoaHoc()

# Hiển thị danh sách khóa học đã đăng ký của từng học viên
print("\nDanh sách khóa học của từng học viên:")
hocVien1.hienThiKhoaHoc()
hocVien2.hienThiKhoaHoc()
hocVienVIPP.hienThiKhoaHoc()

# Tính tổng học phí
danhSachHocVien = [hocVien1, hocVien2, hocVienVIPP]
tinhTongHocPhiTatCa(danhSachHocVien)