# Lab 03 – Email Login · Selenium + pytest

- Dùng *Email + Password* (không có username)
- Bắt buộc tick *Captcha (demo)*
- Có *Remember me* (lưu email vào localStorage)
- Có nút *Show/Hide password*
- Link: *Need help?*, *Create account*
- Social: *GitHub + Google*
- Điều hướng sau khi login: #/home

Trang demo: `auth_email_login.html` (đặt ở root repo).  
Thư mục test: `tests/test_auth_email_login.py`


---

## 1) Cách chạy nhanh (tuỳ chọn, để chụp ảnh pass/fail)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -U pip
pip install pytest selenium webdriver-manager
pytest -q

Sau khi chạy, ảnh sẽ nằm trong thư mục screenshots/ (đưa vào phần nộp).

---

## 2) Use Case (Ảnh PNG/SVG)

![Use Case](./usecase.svg)

## 3) Test cases (≥ 6 case theo yêu cầu)
| ID | Tên test | Tiền điều kiện | Bước thực hiện | Kết quả mong đợi |
|---|---|---|---|---|
| F-TC01 | Đăng nhập thành công | Mở auth_email_login.html | Nhập friend@example.com + Passw0rd! → tick *I'm not a robot* → *SIGN IN* | Thông báo “Welcome! Signed in successfully.”; URL có #/home |
| F-TC02 | Sai mật khẩu | Mở trang | Email đúng, mật khẩu sai, tick Captcha → *SIGN IN* | “Incorrect email or password.”; *không* vào #/home |
| F-TC03 | Bỏ trống trường | Mở trang | (a) Trống email; (b) Trống password; đã tick Captcha | Lỗi tại ô tương ứng + message “Fix the highlighted errors.” |
| F-TC04 | Email sai định dạng | Mở trang | Nhập abc@ + đúng password + tick Captcha → *SIGN IN* | Lỗi “Invalid email format.” |
| F-TC05 | Chưa tick Captcha | Mở trang | Email & password đúng nhưng *không* tick Captcha | Lỗi “Please verify captcha.” |
| F-TC06 | Nút Show/Hide password | Mở trang | Nhập password → bấm 👁️ 2 lần | type đổi password`→text`→`password`; có message “Password visible/hidden” |


- F-TC07: “Remember me” lưu email vào localStorage → refresh vẫn thấy email + checkbox tick.
- F-TC08: Link *Need help?* chuyển hash #/help và hiển thị message.
- F-TC09: Link *Create account* chuyển hash #/register.
- F-TC10: 2 nút social hiển thị & click được (GitHub/Google).

---

## 4) Locators dùng trong test (ngắn gọn, chính xác)
- Email: By.ID, "email"
- Password: By.ID, "pwd"
- Toggle eye: By.ID, "toggle"
- Checkbox Captcha: By.ID, "captcha"
- Checkbox Remember: By.ID, "remember"
- Nút SIGN IN: By.ID, "login"
- Message tổng: By.ID, "message"
- Lỗi trường: By.ID, "emailError", By.ID, "pwdError", By.ID, "captchaError"
- Link: By.ID, "help-link", By.ID, "register-link"
- Social: By.ID, "social-github", By.ID, "social-google"

---

## 5) Bằng chứng nộp bài
- *Ảnh pass/fail* trong thư mục screenshots/ (từ pytest)
- *README.md* (file này) hiển thị rõ *Use Case* + *Bảng test case*
- *Mã nguồn*:
  - auth_email_login.html
  - tests/test_auth_email_login.py
## 5.1 Screenshots (kết quả chạy pytest)
- screenshots/F-TC01_success.png
- screenshots/F-TC02_wrong_pwd.png
- screenshots/F-TC03_empty_emailError.png
- screenshots/F-TC04_invalid_email.png
- screenshots/F-TC05_captcha_required.png
- screenshots/F-TC06_toggle_eye.png
## 5.1 Screenshots (pytest)
- screenshots/F-TC01_success.png
- screenshots/F-TC02_wrong_pwd.png
- screenshots/F-TC03_empty_emailError.png
- screenshots/F-TC04_invalid_email.png
- screenshots/F-TC05_captcha_required.png
- screenshots/F-TC06_toggle_eye.png
Repo: https://github.com/<n23dcpt107-blip>/<auth_email_login.html>
Demo form: (Github Pages):
https://<n23dcpt107-blip>.github.io/<auth_email_login.html>/auth_email_login.html
Hướng dẫn chạy test cục bộ:
pip install -U pytest selenium webdriver-manager
pytest -q

