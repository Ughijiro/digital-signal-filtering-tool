
# Purpose: Design a digital Butterworth Low Pass filter
# using mathematical formulas and pole calculations.
# SciPy is used only to verify the results.

import numpy as np


def butterworth_lowpass(cutoff_hz, order, sampling_hz=48000):

    # Check the input parameters.
    if not 0 < cutoff_hz < sampling_hz / 2:
        raise ValueError("Invalid cutoff frequency.")

    if not 1 <= order <= 4:
        raise ValueError("Supported orders: 1 to 4.")

    # Step 1: Calculate the normalized analog Butterworth poles.
    poles = []

    for k in range(order):
        angle = (2 * k + 1) * np.pi / (2 * order)

        real_part = -np.sin(angle)
        imaginary_part = np.cos(angle)

        pole = real_part + 1j * imaginary_part
        poles.append(pole)

    # Step 2: Adjust the cutoff frequency (prewarping).
    omega_c = 2 * sampling_hz * np.tan(
        np.pi * cutoff_hz / sampling_hz
    )

    # Step 3: Convert analog poles to digital poles.
    digital_poles = []

    for pole in poles:
        analog_pole = omega_c * pole
        digital_pole = (
            (2 * sampling_hz + analog_pole) /
            (2 * sampling_hz - analog_pole)
        )
        digital_poles.append(digital_pole)

    # Step 4: Calculate denominator coefficients.
    a = np.poly(digital_poles).real

    # Step 5: Calculate numerator coefficients.
    # A digital Butterworth Low Pass has N zeros at z = -1.
    b = np.poly([-1] * order).real

    # Step 6: Normalize the gain at zero frequency.
    gain = np.sum(a) / np.sum(b)
    b = b * gain

    return b, a


# Purpose: Test the filter and compare it with SciPy.
# This part runs only when executing butterworth.py directly.

if __name__ == "__main__":

    from scipy.signal import butter

    cutoff = 1000
    order = 4
    sampling = 48000

    # Calculate coefficients using our implementation.
    b, a = butterworth_lowpass(cutoff, order, sampling)

    print("Our b:", b)
    print("Our a:", a)

    # Calculate coefficients using SciPy.
    b_scipy, a_scipy = butter(
        N=order,
        Wn=cutoff,
        btype="lowpass",
        fs=sampling
    )

    print("SciPy b:", b_scipy)
    print("SciPy a:", a_scipy)

    # Compare the calculated coefficients.
    print("Numerator match:", np.allclose(b, b_scipy))
    print("Denominator match:", np.allclose(a, a_scipy))
