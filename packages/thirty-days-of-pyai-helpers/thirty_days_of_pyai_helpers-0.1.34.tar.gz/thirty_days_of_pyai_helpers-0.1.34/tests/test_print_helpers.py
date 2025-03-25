from thirty_days_pyai_helpers.print import slow_print, slow_print_error, slow_print_header, print_intro

def test_slow_print():
    slow_print("test")
    slow_print("test", newline=True)
    slow_print("test", delay=0.5)
    slow_print_error("test")
    slow_print_error("test", delay=0.5)
    slow_print_header("test")
    slow_print_header("test", delay=0.5)
    print_intro()
