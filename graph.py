import string
from data import last_name_letters
import matplotlib.pyplot as plt
import numpy as np
from ascii_base import float_to_letters


letters = last_name_letters()
print(letters.count('X'))
print(f'Total Last Names: {len(letters)}')
letters = [ord(letter) for letter in letters]

mean_letter_value = np.mean(letters)
print(f'Mean Letter Code: {mean_letter_value}')
mean_letter = chr(int(np.around(mean_letter_value)))
print(f'Mean Letter: {mean_letter}')

# 1 extra bin + 1 bin because range is exclusive on the upper bound
plt.hist(letters, bins=range(ord('A'), ord('Z') + 2))
plt.axvline(mean_letter_value, color='red')
plt.xticks(range(ord('A'), ord('Z') + 1), labels=list(string.ascii_uppercase))
plt.xlabel('First letter of last name')
plt.ylabel('Number of students')

vertical_bar_text = f'Mean {np.around(mean_letter_value, decimals=3)} ({float_to_letters(mean_letter_value - 65, precision=2)})'
plt.text(mean_letter_value + 0.35, 84, vertical_bar_text)

plt.show()

