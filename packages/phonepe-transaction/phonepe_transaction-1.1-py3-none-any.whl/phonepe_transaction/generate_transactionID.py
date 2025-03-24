import random
from datetime import datetime
import string

class gen_ids:

    def generate_id(self):
        random_id = "".join(random.choice(string.digits) for _ in range(12))
        get_time = datetime.now().strftime('%Y%m%d%H%M%S')

        return f"TXN{random_id}T{get_time}"
    

if __name__ == "__main__":
    transaction_id = gen_ids()
    get_ids = transaction_id.generate_id()
    print(f"id : {get_ids}")
