import joblib
import numpy as np
import matplotlib.pyplot as plt

crashed = joblib.load('crashed.pkl')
car_passed = joblib.load('car_passed.pkl')

episodes = list(range(len(car_passed)))

plt.subplot(2, 1, 1)
plt.plot(episodes, car_passed, label='Car passed')
plt.plot(episodes, crashed, label='Crashes')
plt.legend()
plt.grid()
plt.xlabel('Number of episodes')
plt.ylabel('Car passed and Crashed')
plt.subplot(2, 1, 2)
plt.plot(episodes, np.array(crashed) /
         np.array(car_passed), label='Car crashed rate')
plt.legend()
plt.grid()
plt.xlabel('Number of episodes')
plt.ylabel('Crashe rate')
plt.tight_layout()
plt.show()
