import numpy as np
import matplotlib.pyplot as plt



tx_data=np.genfromtxt('Ethernet _Electrical_Tx.csv',delimiter=',')
led_driver_data=np.genfromtxt('Ethernet _Electrical_LED_Drive.csv',delimiter=',')
rx_tia_data=np.genfromtxt('Ethernet _Electrical_Rx_TIA.csv',delimiter=',')


rx_tia_data[::,1] = -rx_tia_data[::,1]


plt.plot(tx_data)
plt.plot(rx_tia_data)
plt.show()
