# 🛸 UFO HACK NÃO — phòng chung

Bản nâng cấp có phòng dùng chung, giới hạn 2–100 người, bảng xếp hạng, UFO gọi học sinh và giáo viên tự tạo câu hỏi.

## 1. Tạo Supabase (cơ sở dữ liệu dùng chung)
1. Vào https://supabase.com/ và tạo tài khoản/dự án.
2. Trong dự án, mở **SQL Editor** → **New query**.
3. Sao chép toàn bộ nội dung `supabase_setup.sql`, dán vào SQL Editor và nhấn **Run**.
4. Vào **Project Settings → API** (hoặc **Data API**) lấy Project URL và `anon`/publishable key. Không dùng `service_role` key trong ứng dụng công khai.

## 2. Thêm secrets vào Streamlit Cloud
Trong Streamlit Community Cloud, mở app → **Settings → Secrets**, dán:
```toml
[supabase]
url = "https://YOUR_PROJECT.supabase.co"
key = "YOUR_SUPABASE_ANON_KEY"
```
Thay hai giá trị bằng URL và anon key thật. Lưu để app khởi động lại.

## 3. Tải lên GitHub
Tải các tệp `app.py`, `requirements.txt`, `supabase_setup.sql`, `README.md` lên repository. Đặt Main file path là `app.py`.

## 4. Chơi
- Mọi người mở cùng link Streamlit và nhập cùng mã phòng.
- Giáo viên đăng ký với vai trò Giáo viên, tạo câu hỏi và phát câu hỏi.
- Giáo viên chọn học sinh và bấm gọi UFO.
- Học sinh gửi đáp án; đáp án đúng được cộng 10 điểm.
- Xem tab Bảng xếp hạng.

## Lưu ý quan trọng
- Bản demo cho phép mọi người có quyền anon đọc/ghi bảng để dễ thiết lập; không phù hợp cho dữ liệu nhạy cảm hoặc môi trường công khai lớn. Với lớp học thực tế, hãy thêm đăng nhập/xác thực giáo viên và chính sách bảo mật chặt hơn.
- Cập nhật màn hình bằng nút “Làm mới dữ liệu”; chưa cấu hình cập nhật realtime tự động.
- Bản này minh họa phòng chung; nên kiểm thử với một nhóm nhỏ trước khi cho 100 người vào.
