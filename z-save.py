middle_range = 2
current_page = 1

start_range = current_page - middle_range  # range antes da atual
stop_range = current_page + middle_range  # range atrás da atual

if start_range < 0:
    start_range = 0

print(start_range)
print(stop_range)
