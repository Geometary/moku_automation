'''
This program plots both the 1f and 2f R signals in real time alternatively
for MOKE alignment/calibration.
'''
from moku.instruments import LockInAmp
import matplotlib.pyplot as plt

i = LockInAmp(ip='[fe80::72b3:d5ff:fe87:b49a]', force_connect=True)

try:
    # Set both input channels to DC coupling with 50Ohm impedance, and 0dB attenuation.
    i.set_frontend(1, coupling='DC', impedance='50Ohm', attenuation='0dB')
    i.set_frontend(2, coupling='DC', impedance='50Ohm', attenuation='0dB')

    # Set demodulation to be external and automatically reads frequency
    i.set_demodulation('ExternalPLL', phase=0)
    i.set_pll(auto_acquire=True)

    # Set the lowpass filter
    i.set_filter(corner_frequency=2, slope='Slope6dB')

    # Go to the R-theta mode to read 1f/2f magnitudes
    i.set_outputs(main='R', aux='Theta')

    # Configure the monitor points
    i.set_monitor(1, 'MainOutput')
    i.set_monitor(2, 'AuxOutput')

    # Configure the trigger on ProbeA at zero level, at the centre of a +-0.1s timebase
    i.set_trigger(type="Edge", source="ProbeA", level=0)
    i.set_timebase(-3, 0)

    data = i.get_data()
    plt.ion()
    plt.show()
    plt.grid(visible=True)
    plt.ylim([0, 0.25])
    plt.xlim([data['time'][0], data['time'][-1]])

    line1, = plt.plot([], linestyle=None, label="1f")
    line2, = plt.plot([], linestyle=None, label='2f')
    plt.ylabel('Amplitude (V)')
    plt.xlabel('Time (s)')
    plt.legend()
    ax = plt.gca()

    while True:
        # Go to 1f mode first
        i.set_pll(frequency_multiplier=1)
        i.set_gain(main=70, aux=0)     # 70dB of gain
        i.set_polar_mode(range='7.5mVpp')       # 7.5mVpp of range

        # Update the plot
        data = i.get_data()
        line1.set_ydata(data['ch1'])
        line1.set_xdata(data['time'])
        plt.xlim([data['time'][0], data['time'][-1]])
        plt.pause(3)

        # Then go to 2f mode
        i.set_pll(frequency_multiplier=2)
        i.set_gain(main=0, aux=0)      # zero gain
        i.set_polar_mode(range='2Vpp')      # 2Vpp of range
    
        # update the plot
        data = i.get_data()
        line2.set_ydata(data['ch1'])
        line2.set_xdata(data['time'])
        plt.xlim([data['time'][0], data['time'][-1]])
        plt.pause(3)

except Exception as e:
    print(f'Exception occurred: {e}')
finally:
    # Close the connection to the Moku device
    # This ensures network resources are released correctly
    i.relinquish_ownership()