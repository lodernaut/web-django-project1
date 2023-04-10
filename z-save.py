if __name__ == "__main__":
    fields = [
        ("title", 65),
        ("description", 165),
        ("preparation_time_unit", 65),
        ("servings_unit", 65),
    ]
    for field, max_length in fields:
        x = "x"*(max_length+1)
        print(field, x, len(x))
