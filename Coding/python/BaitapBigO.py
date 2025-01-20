# Bài tập 1 
print("Bai Tap 1")
def BaiTap1():
    Vidu1 = [
        "i = 0",                      #Dòng 1                         
        "while (i < n):",             #Dòng 2      
        "    i = i + 100"             #Dòng 3     
    ]

    # Lời giải thích tương ứng với từng dòng
    GiaiThich1 = [
        "1. Biến 'i' được khởi tạo với giá trị ban đầu là 0 (O(1)).",
        "2. Vòng lặp 'while' tiếp tục chạy miễn là điều kiện 'i < n' thỏa mãn.",
        "3. Sau mỗi lần lặp, giá trị của 'i' tăng thêm 100 (O(1) cho mỗi lần lặp).",
        "=> Số lần lặp được tính bằng n / 100 (tỷ lệ tuyến tính với n).",      
    ]

    print("Giải thích từng dòng của đoạn mã:")
    for i, line in enumerate(Vidu1):
        print(f"{line:<20} <-- {GiaiThich1[i]}")

    print(f"\n{GiaiThich1[-1]}")  
    print("Kết luận: tổng số lần lặp tỷ lệ với n, dẫn đến độ phức tạp thời gian là O(n).")  

BaiTap1()


# Bai Tap 2 
print("\nBai Tap 2")
def Baitap2():
    Vidu2 = [
        "while (i < n):",                      # Dòng 1
        "    while (a < n):",                  # Dòng 2
        "        while (b < n):",              # Dòng 3
        "            b = b + 1",               # Dòng 4
        "        a = a + 1",                   # Dòng 5
        "    while (c < n):",                  # Dòng 6
        "        c = c + 1",                   # Dòng 7
        "    i = i + 100"                      # Dòng 8
    ]

    GiaiThich2 = [
        "1. Vòng lặp ngoài cùng, chạy cho đến khi i >= n. Số lần lặp là n / 100.",
        "2. Bên trong vòng lặp i, vòng lặp a chạy từ 0 đến n (O(n)).",
        "3. Vòng lặp b nằm trong vòng lặp a, chạy từ 0 đến n với mỗi lần lặp của a (O(n^2)).",
        "4. Tăng giá trị b lên 1 trong mỗi lần lặp (O(1) mỗi lần).",
        "5. Sau khi b hoàn thành, tăng giá trị a lên 1 để tiếp tục vòng lặp.",
        "6. Vòng lặp c chạy độc lập trong mỗi lần lặp của i (O(n)).",
        "7. Tăng giá trị c lên 1 trong mỗi lần lặp (O(1) mỗi lần).",
        "8. Sau khi hoàn thành các vòng lặp, tăng giá trị i lên 100."
    ]

    print("Giải thích từng dòng của đoạn mã:")
    for i, (line, GiaiThich2) in enumerate(zip(Vidu2, GiaiThich2), start=1):
        print(f"{i}. {line:<25} <-- {GiaiThich2}")

    # Kết luận
    print("\nKết luận:")
    print("Vòng lặp i: lặp lại n/100 => O(n)")
    print("Vòng lặp a: Mỗi lần vòng lặp i, vòng lặp a thực hiện O(n) lần => tổng cộng giữa i và a : O(n^2)")
    print("Vòng lặp b: Mỗi lần vòng lặp a, vòng lặp b thực hiện O(n) lần => tổng cộng giữa b và a:  O(n^2)")
    print("Vì vòng lặp i,a,b liên tục => tổng cộng độ phức tạp của 3 vòng i,a,b: O(n^3)")
    print("Vòng lặp c: Vòng lặp c và i có ảnh hưởng tuyến tính(khong lien quan den vong lap a va b). Do đó, tổng độ phức tạp là O(n*(n/100) => tổng cộng O(n^2).")
    print("\n")
    print("Vòng lặp a và b nằm trong i tạo thành độ phức tạp lớn nhất: O(n^3).")

# Gọi hàm để in giải thích
Baitap2()


# Bài tập 3
print("Bai Tap 3")
def BaiTap3():
    Vidu3 = [
        "i = 0",                      #Dòng 1                         
        "while (i < n):",             #Dòng 2      
        "    i = i + 1"               #Dòng 3     
    ]

    GiaiThich3 = [
        "1. Biến 'i' được khởi tạo với giá trị ban đầu là 0 (O(1)).",
        "2. Vòng lặp 'while' tiếp tục chạy miễn là điều kiện 'i < n' thỏa mãn.",
        "3. Sau mỗi lần lặp, giá trị của 'i' tăng thêm 1 (O(1) cho mỗi lần lặp).",     
    ]

    print("Giải thích từng dòng của đoạn mã:")
    for i, line in enumerate(Vidu3):
        print(f"{line:<20} <-- {GiaiThich3[i]}")
 
    print("Kết luận: tổng số lần lặp tỷ lệ với n, dẫn đến độ phức tạp thời gian là O(n).")  

BaiTap3()
