import pandas as pd
import numpy as np
import random
import string

from ofwhich import OfWhich

num_rows = 100

def random_string(length=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

df = pd.DataFrame({
    'Category1': np.random.choice(['X', 'Y', 'Z'], size=num_rows),
    'Category2': np.random.choice(['Red', 'Green', 'Blue'], size=num_rows),
    'Bool1': np.random.choice([True, False], size=num_rows),
    'Bool2': np.random.choice([True, False], size=num_rows),
    'String1': [random_string() for _ in range(num_rows)],
    'Float1': np.random.uniform(0, 100, num_rows),
    'Float2': np.random.uniform(50, 200, num_rows),
})

_ = OfWhich(df, 'Category1', 'Bool1')

