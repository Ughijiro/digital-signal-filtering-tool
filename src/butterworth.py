# Purpose: Calculate digital Butterworth filter coefficients
# using mathematical formulas.
# Supported filters: Low Pass, High Pass, Band Pass and Band Stop.
# Supported prototype orders: 1 to 4.

import numpy as np

# Purpose: Calculate normalized analog Butterworth poles.
def calculate_poles(order):

    poles = []

    for k in range(order):
        angle = (2 * k + 1) * np.pi / (2 * order)

        real_part = -np.sin(angle)
        imaginary_part = np.cos(angle)

        pole = real_part + 1j * imaginary_part
        poles.append(pole)

    return poles

# Purpose: Convert a frequency in Hz to a prewarped
# analog angular frequency.
def prewarp(frequency_hz, sampling_hz):

    return 2 * sampling_hz * np.tan(
        np.pi * frequency_hz / sampling_hz
    )

# Purpose: Convert analog poles into digital poles
# using the bilinear transformation.
def convert_poles(analog_poles, sampling_hz):

    digital_poles = []
    K = 2 * sampling_hz

    for pole in analog_poles:
        digital_pole = (K + pole) / (K - pole)
        digital_poles.append(digital_pole)

    return digital_poles

# Purpose: Normalize the filter gain at a selected
# digital angular frequency.
def normalize_gain(b, a, omega):

    z_inverse = np.exp(-1j * omega)

    numerator = 0
    denominator = 0

    for i in range(len(b)):
        numerator += b[i] * z_inverse**i

    for i in range(len(a)):
        denominator += a[i] * z_inverse**i

    gain = np.abs(denominator) / np.abs(numerator)

    return b * gain

# Purpose: Validate common filter parameters.
def validate_order(order):

    if not 1 <= order <= 4:
        raise ValueError("Supported orders: 1 to 4.")

def validate_cutoff(cutoff_hz, sampling_hz):

    if not 0 < cutoff_hz < sampling_hz / 2:
        raise ValueError("Invalid cutoff frequency.")

# LOW PASS

def butterworth_lowpass(cutoff_hz, order, sampling_hz=48000):

    validate_order(order)
    validate_cutoff(cutoff_hz, sampling_hz)

    poles = calculate_poles(order)
    omega_c = prewarp(cutoff_hz, sampling_hz)

    # Scale the normalized analog poles.
    analog_poles = []

    for pole in poles:
        analog_poles.append(omega_c * pole)

    digital_poles = convert_poles(analog_poles, sampling_hz)

    # Calculate denominator coefficients.
    a = np.poly(digital_poles).real

    # Low Pass has N digital zeros at z = -1.
    b = np.poly([-1] * order).real

    # Normalize the gain at 0 Hz.
    b = normalize_gain(b, a, 0)

    return b, a

# HIGH PASS

def butterworth_highpass(cutoff_hz, order, sampling_hz=48000):

    validate_order(order)
    validate_cutoff(cutoff_hz, sampling_hz)

    poles = calculate_poles(order)
    omega_c = prewarp(cutoff_hz, sampling_hz)

    # Transform Low Pass poles into High Pass poles.
    analog_poles = []

    for pole in poles:
        analog_poles.append(omega_c / pole)

    digital_poles = convert_poles(analog_poles, sampling_hz)

    a = np.poly(digital_poles).real

    # High Pass has N digital zeros at z = 1.
    b = np.poly([1] * order).real

    # Normalize the gain at the Nyquist frequency.
    b = normalize_gain(b, a, np.pi)

    return b, a

# BAND PASS

def butterworth_bandpass(lower_hz, upper_hz,
                         order, sampling_hz=48000):

    validate_order(order)

    if not 0 < lower_hz < upper_hz < sampling_hz / 2:
        raise ValueError("Invalid cutoff frequencies.")

    poles = calculate_poles(order)

    # Prewarp both cutoff frequencies.
    omega_1 = prewarp(lower_hz, sampling_hz)
    omega_2 = prewarp(upper_hz, sampling_hz)

    # Calculate analog bandwidth and center frequency.
    bandwidth = omega_2 - omega_1
    omega_0 = np.sqrt(omega_1 * omega_2)

    # Transform each Low Pass pole into two Band Pass poles.
    analog_poles = []

    for pole in poles:
        term = bandwidth * pole

        discriminant = np.sqrt(
            term**2 - 4 * omega_0**2 + 0j
        )

        pole_1 = (term + discriminant) / 2
        pole_2 = (term - discriminant) / 2

        analog_poles.append(pole_1)
        analog_poles.append(pole_2)

    digital_poles = convert_poles(analog_poles, sampling_hz)

    a = np.poly(digital_poles).real

    # Band Pass has N zeros at z = 1 and N at z = -1.
    zeros = [1] * order + [-1] * order
    b = np.poly(zeros).real

    # Find the digital frequency corresponding
    # to the analog center frequency.
    K = 2 * sampling_hz
    center_omega = 2 * np.arctan(omega_0 / K)

    # Normalize the gain at the center frequency.
    b = normalize_gain(b, a, center_omega)

    return b, a

# BAND STOP

def butterworth_bandstop(lower_hz, upper_hz,
                         order, sampling_hz=48000):

    validate_order(order)

    if not 0 < lower_hz < upper_hz < sampling_hz / 2:
        raise ValueError("Invalid cutoff frequencies.")

    poles = calculate_poles(order)

    omega_1 = prewarp(lower_hz, sampling_hz)
    omega_2 = prewarp(upper_hz, sampling_hz)

    bandwidth = omega_2 - omega_1
    omega_0 = np.sqrt(omega_1 * omega_2)

    # Transform each Low Pass pole into two Band Stop poles.
    analog_poles = []

    for pole in poles:
        term = bandwidth / pole

        discriminant = np.sqrt(
            term**2 - 4 * omega_0**2 + 0j
        )

        pole_1 = (term + discriminant) / 2
        pole_2 = (term - discriminant) / 2

        analog_poles.append(pole_1)
        analog_poles.append(pole_2)

    digital_poles = convert_poles(analog_poles, sampling_hz)

    a = np.poly(digital_poles).real

    # Analog Band Stop zeros are located at +/- j*omega_0.
    # Convert them into digital zeros.
    K = 2 * sampling_hz

    zero_1 = (K + 1j * omega_0) / (K - 1j * omega_0)
    zero_2 = np.conj(zero_1)

    zeros = []

    for k in range(order):
        zeros.append(zero_1)
        zeros.append(zero_2)

    b = np.poly(zeros).real

    # Normalize the gain at 0 Hz.
    b = normalize_gain(b, a, 0)

    return b, a

# TESTING

# Purpose: Compare our coefficients with SciPy.
# These tests run only when this file is executed directly.

if __name__ == "__main__":

    from scipy.signal import butter

    sampling = 48000
    lower = 1000
    upper = 3000

    filters = {
        "Low Pass": butterworth_lowpass,
        "High Pass": butterworth_highpass,
        "Band Pass": butterworth_bandpass,
        "Band Stop": butterworth_bandstop
    }

    filter_types = {
        "Low Pass": "lowpass",
        "High Pass": "highpass",
        "Band Pass": "bandpass",
        "Band Stop": "bandstop"
    }

    for name, function in filters.items():

        print("\nTesting:", name)

        for order in range(1, 5):

            if name in ["Low Pass", "High Pass"]:
                b, a = function(lower, order, sampling)
                cutoff = lower
            else:
                b, a = function(lower, upper, order, sampling)
                cutoff = [lower, upper]

            b_scipy, a_scipy = butter(
                N=order,
                Wn=cutoff,
                btype=filter_types[name],
                fs=sampling
            )

            b_match = np.allclose(b, b_scipy)
            a_match = np.allclose(a, a_scipy)

            print(
                f"Order {order}: "
                f"b match = {b_match}, "
                f"a match = {a_match}"
            )
