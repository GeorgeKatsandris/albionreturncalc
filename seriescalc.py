import numpy as np
import sqlitequeries

return_rate = 0.367
item_number = 141

total_crafted = 0
remaining = item_number

while remaining != 0:
    total_crafted += remaining
    remaining = np.floor(return_rate * remaining)
    print(str(total_crafted) + " " + str(remaining))
