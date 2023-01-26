import ctypes


def list_browser_x_coordinates(max_threading_number):
    user32 = ctypes.windll.user32
    width_screen = user32.GetSystemMetrics(0)
    width_screen_each_browser = [i for i in range(0, width_screen, int(width_screen / max_threading_number))]
    return width_screen_each_browser


def max_size_each_browser(max_threading_number):
    user32 = ctypes.windll.user32
    width_screen, height_screen = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    # trừ 40px vào cái taskbar
    return width_screen / max_threading_number, height_screen - 40


def split_size_window(max_threading_number):
    if max_threading_number == 1 or max_threading_number == 2:
        return 2
    elif max_threading_number % 2 == 0:
        number_browser_each_row = int(max_threading_number / 2)
    else:
        number_browser_each_row = int(max_threading_number / 2) + 1
    return number_browser_each_row


def max_size_each_browser_new(max_threading_number):
    number_browser_each_row = split_size_window(max_threading_number)
    user32 = ctypes.windll.user32
    width_screen, height_screen = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    max_width_each_browser = int(width_screen / number_browser_each_row)
    max_height_each_browser = int((height_screen - 40) / 2)
    lst = [i for i in range(0, width_screen, max_width_each_browser)]
    list1 = lst.copy()
    lst = [(x, 0) for x in lst]
    list1 = [(x, 520) for x in list1]
    return lst + list1, max_width_each_browser, max_height_each_browser

# print(max_size_each_browser_new(1))
