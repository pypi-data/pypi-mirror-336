def say_hello(s = None):
    if s:
        print(f"Hello {s}!")
        return
    print("Hello World!")
