from moku.instruments import LockInAmp
import matplotlib.pyplot as plt

i = LockInAmp(ip='[fe80::72b3:d5ff:fe87:b49a]', force_connect=True)

try:
    # Set Channel 1 and 2 to DC coupled, 1 Mohm impedance, and 400 mVpp range
    i.set_frontend(1, coupling='DC', impedance='1MOhm', attenuation='0dB')
    i.set_frontend(2, coupling='DC', impedance='1MOhm', attenuation='-20dB')

    # Configure the demod signal to local oscillator with 1 MHz and
    # 0 deg phase shift
    i.set_demodulation('Internal', frequency=1e6, phase=0)

    # Set low pass filter to 1 kHz corner frequency with 6dB/octave slope
    i.set_filter(1e3, slope='Slope6dB')

    # Config output signals
    # X component to Output 1
    # Aux oscillator signal to Output 2 at 1 MHz 500 mVpp
    i.set_outputs('X', 'Aux')
    i.set_aux_output(1e6, 0.5)

    # Set up signal monitoring
    # Config monitor points to Input 1 and main output
    i.set_monitor(1, 'Input1')
    i.set_monitor(2, 'MainOutput')

    # Config the trigger conditions
    # Trigger on Probe A, rising edge, 0V
    i.set_trigger(type='Edge', source='ProbeA', level=0)

    # View +- 1ms i.e. trigger in the centre
    i.set_timebase(-1e-3, 1e-3)

    data = i.get_data()
    plt.ion()
    plt.show()
    plt.grid(visible=True)
    plt.ylim([-1, 1])
    plt.xlim([data['time'][0], data['time'][-1]])

    line1, = plt.plot([])
    line2, = plt.plot([])

    ax = plt.gca()

    while True:
        # Get new data
        data = i.get_data()

        # Update the plot
        line1.set_ydata(data['ch1'])
        line2.set_ydata(data['ch2'])
        line1.set_xdata(data['time'])
        line2.set_xdata(data['time'])
        plt.pause(0.001)

except Exception as e:
    print(f'Exception occurred: {e}')
finally:
    # Close the connection to the Moku device
    # This ensures network resources are released correctly
    i.relinquish_ownership()
