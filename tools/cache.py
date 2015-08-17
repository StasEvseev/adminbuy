#coding: utf-8
from tools import path_to_cache


def save_page_to_cache(page, name):
    token_stub = "TOKEN123"
    token_orig = "'{{ token }}'"
    global_stub = "GLOBALS123"
    global_orig = "{{ globals }}"
    # result = page.replace(token_orig, token_stub)
    with open(path_to_cache(name), "w") as file1:
        result = page.replace(token_stub, token_orig)
        result = result.replace(global_stub, global_orig)
        file1.write(result.encode("utf-8"))