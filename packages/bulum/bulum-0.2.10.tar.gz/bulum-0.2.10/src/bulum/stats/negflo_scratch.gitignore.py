import pandas as pd

df = pd.DataFrame({
    "a": [1, 2, 3, 4, 5],
    "b": [6, 4, 6, 7, 4]
})

print(df[df.index <= 3])
