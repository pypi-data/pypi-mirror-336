from telemetrix_rpi_pico_w import telemetrix_rpi_pico_w

board = telemetrix_rpi_pico_w.TelemetrixRpiPicoW(ip_address='192.168.2.102')

board.digital_write(pin=5, value=1)

