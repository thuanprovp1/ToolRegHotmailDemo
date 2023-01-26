import threading
import tkinter
from tkinter import *
import re
import sys
from itertools import cycle
from tkinter import ttk
import concurrent.futures
import tkinter.messagebox
from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service

from src.create_hotmail import reg_outlook
from src.get_resolution_computer import max_size_each_browser_new
from src.privateChromeOptions import setting_chrome_privated
from src.readExcelData import read_info_in_excel, write_status

MAX_WIDTH_EACH_WINDOW = 100
MAX_HEIGHT_EACH_WINDOW = 100
WINDOW_LIST_COORDINATES = list()


def start_browser(account):
    global status_lbl_text, use_proxy_var
    has_proxy = bool(use_proxy_var.get())
    x_coordinates, y_coordinates = next(WINDOW_LIST_COORDINATES)
    if has_proxy:
        if account['proxy'] is not None and account['proxy'] != '':
            chrome_options_setting = setting_chrome_privated(account['proxy'])
        else:
            return 'Bạn chưa điền proxy'
    else:
        chrome_options_setting = setting_chrome_privated(False)
    driver = wd.Chrome(service=Service('chromedriver.exe'), options=chrome_options_setting)
    driver.set_window_position(x_coordinates, y_coordinates)
    driver.set_window_size(MAX_WIDTH_EACH_WINDOW, MAX_HEIGHT_EACH_WINDOW)
    info_account = reg_outlook(driver, account)
    return info_account


def start_reg_account():
    global max_threading_number, status_lbl_text, WINDOW_LIST_COORDINATES, MAX_WIDTH_EACH_WINDOW, MAX_HEIGHT_EACH_WINDOW
    try:
        if max_threading_number.get() <= 0 or max_threading_number.get() > 30:
            print('Số luồng phải trong khoảng 1-30')
            sys.exit()
        data_full = read_info_in_excel()
        WINDOW_LIST_COORDINATES, MAX_WIDTH_EACH_WINDOW, MAX_HEIGHT_EACH_WINDOW = max_size_each_browser_new(
            max_threading_number.get())
        WINDOW_LIST_COORDINATES = cycle(WINDOW_LIST_COORDINATES)
        status_lbl_text.set('Đang chạy..')

        if data_full:
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_threading_number.get()) as executor:
                for acc, result in zip(data_full, executor.map(start_browser, data_full)):
                    print(result, '-Excel col-', acc['current_row'])
                    write_status(result, acc['current_row'], 8)
            status_lbl_text.set('Đã chạy xong')
        else:
            tkinter.messagebox.showerror(title='Lỗi dữ liệu đầu vào', message='Không có dữ liệu excel')

    except Exception as e:
        e = re.sub(r'Stacktrace.+', '', str(e), flags=re.S)
        print(e)


if __name__ == '__main__':
    top = Tk()
    top.title('Auto Reg Hotmail - Thuan Luu')
    top.geometry("340x190+790+300")
    top.resizable(True, True)

    # value
    max_threading_number = tkinter.IntVar(value=1)
    use_proxy_var = tkinter.IntVar(value=0)
    status_lbl_text = tkinter.StringVar(value='Vui lòng điền dữ liệu vào data.xlxs trước khi chạy tool')
    # end value

    # MAIN FEATURES
    main_zone = LabelFrame(top, text="Chức năng", bd=2)
    main_zone.grid(row=0, column=0, columnspan=3, ipadx=12, ipady=8, padx=15, pady=5)

    # thread number
    Label(main_zone, text="Số luồng", wraplength=260).grid(row=1, column=0, sticky='ns', padx=12)
    max_thearding_number_entry = Entry(main_zone, width=30, text=max_threading_number)
    max_thearding_number_entry.grid(row=1, column=1, sticky='nw', padx=(10, 0))

    # user proxy
    Label(main_zone, text="Dùng proxy").grid(row=2, column=0, sticky='ns')
    use_proxy_radio = Radiobutton(main_zone, text="Có", variable=use_proxy_var, value=1)
    use_proxy_radio.grid(row=2, column=1, sticky='nw', padx=5)
    not_use_proxy_radio = Radiobutton(main_zone, text="Không", variable=use_proxy_var, value=0)
    not_use_proxy_radio.grid(row=2, column=1, sticky='ne', padx=(0, 20))

    # status
    Label(main_zone, text="Trạng thái: ", font=("Helvetica", 10)).grid(row=3, column=0, sticky='ns')
    status_lbl = Label(main_zone, textvariable=status_lbl_text, fg='#04AA6D',
                       wraplength=190,
                       font=("Helvetica", 10))
    status_lbl.grid(row=3, column=1, padx=7, sticky='w', columnspan=2)

    # run button
    run_btn = Button(main_zone, text='Run', width=8,
                     command=lambda: threading.Thread(target=start_reg_account).start())
    # command=start_profile)
    run_btn.grid(row=5, column=1, padx=(4, 5), pady=(5, 0), sticky='e')
    # END MAIN FEATURES
    top.mainloop()
