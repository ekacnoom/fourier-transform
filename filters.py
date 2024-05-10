from scipy import signal

def apply_lowpass_filter(input_data, order):
    # Визначення коефіцієнтів фільтра
    b, a = signal.butter(order, 0.05, 'low')  # Налаштовувані параметри фільтрації

    # Застосування фільтру до вхідних даних
    filtered_data = signal.lfilter(b, a, input_data)

    return filtered_data

def apply_highpass_filter(input_data, order):
    # Визначення коефіцієнтів фільтра
    b, a = signal.butter(order, 0.05, 'high')  # Налаштовувані параметри фільтрації

    # Застосування фільтру до вхідних даних
    filtered_data = signal.lfilter(b, a, input_data)

    return filtered_data
