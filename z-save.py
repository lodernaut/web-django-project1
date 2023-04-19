def fix_search_value(value):
    return str(value).strip()


if __name__ == '__main__':
    # stripped_string deve conter o valor de 'A' (sem espaços)
    stripped_string = fix_search_value('     A     ')
    print(stripped_string)
