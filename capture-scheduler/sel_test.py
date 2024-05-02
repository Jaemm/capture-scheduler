import os
import time
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox  # messagebox 추가
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading

custom_path = None  # 초기 저장 경로
reservation_times = []  # 예약 시간 리스트
capture_records = []  # 캡처를 완료한 기록 저장할 리스트 생성
capture_thread = None  # 캡처 스레드
stop_thread = False  # 스레드 중지 플래그


def update_current_time():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_time_label.config(text=current_time)
    root.after(1000, update_current_time)  # 1초마다 업데이트


def take_screenshot_now():
    global custom_path, capture_records
    if custom_path is None:
        messagebox.showwarning("경고", "저장 경로를 설정해주세요.")
        return

    capture_result = take_screenshot()
    if capture_result:  # 캡처가 성공했을 경우에만 기록에 추가
        capture_records.append(capture_result)
        update_capture_record_list()


def take_screenshot_at_time():
    global custom_path, capture_records, capture_thread
    if custom_path is None:
        messagebox.showwarning("경고", "저장 경로를 설정해주세요.")
        return

    # 현재 설정된 시간 가져오기
    selected_hour = int(hour_var.get())
    selected_minute = int(minute_var.get())

    # 현재 시간 및 설정된 시간 가져오기
    now = datetime.now()
    target_time = now.replace(hour=selected_hour, minute=selected_minute, second=0, microsecond=0)

    # 현재 시간보다 과거인지 확인
    if target_time <= now:
        messagebox.showwarning("경고", "과거의 시간은 선택할 수 없습니다.")
        return
    
    # 중복 예약인지 확인
    new_reservation_time = f"{selected_hour:02d}:{selected_minute:02d}"
    if new_reservation_time in reservation_times:
        messagebox.showwarning("경고", "이미 해당 시간에 예약이 되어 있습니다.")
        return

    # 예약 시간에 추가
    reservation_time = f"{selected_hour:02d}:{selected_minute:02d}"
    reservation_times.append(reservation_time)
    update_reservation_list()

    messagebox.showinfo("성공", f"{reservation_time}에 캡처가 예약되었습니다.")

    # 예약 캡처 스레드 시작
    capture_thread = threading.Thread(target=capture_at_time_thread)
    capture_thread.start()


def capture_at_time_thread():
    global stop_thread
    stop_thread = False  # 스레드 중지 플래그 초기화

    # 현재 설정된 시간 가져오기
    selected_hour = int(hour_var.get())
    selected_minute = int(minute_var.get())

    # 예약 시간 설정
    reservation_time = datetime.now().replace(hour=selected_hour, minute=selected_minute, second=0, microsecond=0)

    # 예약 시간이 여전히 리스트에 있는지 확인(유효성 검사)
    if f"{selected_hour:02d}:{selected_minute:02d}" not in reservation_times:
        return  # 삭제된 예약 시간이므로 실행 중단

    # 대기
    while datetime.now() < reservation_time:
        if stop_thread:  # 스레드 중지 플래그 확인
            return  # 스레드 종료
        update_current_time()
        time.sleep(1)

    # 캡처 실행
    capture_result = take_screenshot()
    if capture_result:  # 캡처가 성공했을 경우에만 기록에 추가
        capture_records.append(capture_result)
        update_capture_record_list()

    reservation_times.remove(f"{selected_hour:02d}:{selected_minute:02d}")
    update_reservation_list()


def update_reservation_list():
    global reservation_times
    # 예약 시간 리스트를 시간 순으로 정렬
    sorted_times = sorted(reservation_times, key=lambda x: datetime.strptime(x, "%H:%M"))
    reservation_listbox.delete(0, tk.END)  # 리스트 초기화
    for time in sorted_times:
        reservation_listbox.insert(tk.END, time)  # 리스트에 추가
    print_reservation_times()  # 예약 시간 목록 출력 추가

def delete_selected_reservation():
    global reservation_times, stop_thread
    selected_index = reservation_listbox.curselection()  # 선택된 항목의 인덱스 가져오기
    if selected_index:  # 선택된 항목이 있으면
        selected_time = reservation_listbox.get(selected_index[0])  # 선택된 항목 가져오기
        reservation_times.remove(selected_time)  # 리스트에서 삭제
        stop_thread = True  # 스레드 중지 플래그 설정
        update_reservation_list()  # 업데이트된 리스트 표시


def take_screenshot():
    # 크롬 드라이버 실행
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        # 로그인 페이지로 이동
        driver.get('https://bms.firstcorea.com/login')

        # 사용자 이름과 비밀번호 입력
        username = 'first'
        password = 'first'
        username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'user-id')))
        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'user-password')))
        username_field.send_keys(username)
        password_field.send_keys(password)

        # 비밀번호 입력 후 Enter 키 누르기
        password_field.send_keys(Keys.RETURN)

        # 로그인 완료될 때까지 기다림
        WebDriverWait(driver, 10).until(EC.url_contains('firstcorea.com'))

        # 로그인 후 10초간 대기
        time.sleep(3)

        # 현재 날짜와 시간을 문자열로 변환하여 파일명에 추가
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_filename = f"screenshot_{current_datetime}.png"
        screenshot_path = os.path.join(custom_path, screenshot_filename)

        # 페이지 스크린샷 캡처 및 저장
        driver.save_screenshot(screenshot_path)

        # 성공 메시지 출력
        messagebox.showinfo("Success", f"스크린샷이 성공적으로 저장되었습니다. 파일 경로:\n{screenshot_path}")
        return {
            'datetime': current_datetime,
            'path': screenshot_path
        }
    except Exception as e:
        # 에러 메시지 출력
        messagebox.showerror("Error", f"오류 발생: {str(e)}")
        return None  # 캡처 실패 시 None 반환
    finally:
        # 작업 완료 후 드라이버 종료
        driver.quit()


def update_capture_record_list():
    capture_listbox.delete(0, tk.END)  # 기존 항목 모두 삭제
    for record in capture_records:
        capture_listbox.insert(tk.END, f"{record['datetime']} - {record['path']}")


def browse_path():
    global custom_path
    custom_path = filedialog.askdirectory()
    path_label.config(text=custom_path)

def print_reservation_times():
    global reservation_times
    print("예약 시간 목록:", reservation_times)

def show_about_info():
    messagebox.showinfo("About", "B&FCS 캡처 스케줄러\n버전: Beta_v0.1\n개발자: JAEMIN CHOI\n배포일: 24-05-02")


# Tkinter GUI 생성
root = tk.Tk()
root.title("B&FCS 캡처 스케줄러 Beta_v0.1")
root.geometry("900x300")  # 윈도우 크기 설정

# 현재 시간 표시
current_time_label = tk.Label(root, text="", font=("Helvetica", 14))
current_time_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5)
update_current_time()  # 현재 시간 업데이트 시작

# 시간 설정 레이블 및 드롭다운 메뉴
hour_label = tk.Label(root, text="시간:")
hour_label.grid(row=1, column=0, padx=10, pady=5)
hour_var = tk.StringVar(root)
hour_dropdown = tk.OptionMenu(root, hour_var, *range(24))
hour_var.set("0")
hour_dropdown.grid(row=1, column=1, padx=10, pady=5)

minute_label = tk.Label(root, text="분:")
minute_label.grid(row=2, column=0, padx=10, pady=5)
minute_var = tk.StringVar(root)
minute_dropdown = tk.OptionMenu(root, minute_var, *range(60))
minute_var.set("0")
minute_dropdown.grid(row=2, column=1, padx=10, pady=5)

# 경로 설정 버튼
path_button = tk.Button(root, text="저장 경로 설정", command=browse_path)
path_button.grid(row=3, columnspan=2, padx=10, pady=5)

# 경로 레이블
path_label = tk.Label(root, text="저장 경로:")
path_label.grid(row=4, columnspan=2, padx=10, pady=5)

# 즉시 캡처 버튼
capture_now_button = tk.Button(root, text="즉시 캡처", command=take_screenshot_now)
capture_now_button.grid(row=5, columnspan=2, padx=10, pady=5)

# 설정된 시간에 캡처 버튼
capture_at_time_button = tk.Button(root, text="예약 캡처", command=take_screenshot_at_time)
capture_at_time_button.grid(row=6, columnspan=2, padx=10, pady=5)

# 예약 시간 리스트
reservation_frame = tk.Frame(root)
reservation_frame.grid(row=1, column=2, rowspan=6, padx=10, pady=5, sticky="nsew")

reservation_label = tk.Label(reservation_frame, text="예약 시간 리스트")
reservation_label.pack()

reservation_listbox = tk.Listbox(reservation_frame)
reservation_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

reservation_scrollbar = tk.Scrollbar(reservation_frame, orient=tk.VERTICAL)
reservation_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

reservation_listbox.config(yscrollcommand=reservation_scrollbar.set)
reservation_scrollbar.config(command=reservation_listbox.yview)

# 삭제 버튼 추가
delete_button = tk.Button(reservation_frame, text="예약 삭제", command=delete_selected_reservation)
delete_button.pack(side=tk.BOTTOM, padx=10, pady=5)

# 캡처 기록 레이블 및 리스트 박스
capture_frame = tk.Frame(root)
capture_frame.grid(row=1, column=3, rowspan=6, padx=10, pady=5, sticky="nsew")

capture_label = tk.Label(capture_frame, text="캡처 기록")
capture_label.pack()

capture_listbox = tk.Listbox(capture_frame, width=50)
capture_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

capture_scrollbar = tk.Scrollbar(capture_frame, orient=tk.VERTICAL)
capture_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

capture_listbox.config(yscrollcommand=capture_scrollbar.set)
capture_scrollbar.config(command=capture_listbox.yview)

# 메뉴에 About 메뉴 추가
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

about_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Menu", menu=about_menu)
about_menu.add_command(label="About", command=show_about_info)

# 캡처 기록 업데이트
update_capture_record_list()
root.mainloop()
