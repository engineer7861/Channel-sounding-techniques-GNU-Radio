#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not doch Doch titled yet
# Author: usama
# GNU Radio version: 3.10.7.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
from gnuradio import digital
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import sip



class time_freq_correlation(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not doch Doch titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not doch Doch titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "time_freq_correlation")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 62.5e6
        self.tx_gain = tx_gain = 60
        self.taps = taps = 1
        self.symbol = symbol = samp_rate/1
        self.rx_gain = rx_gain = 40
        self.freq = freq = 3.740e9
        self.fft_1 = fft_1 = 1024*4
        self.deg = deg = 7
        self.alpha = alpha = 0.350
        self.BW = BW = 0

        ##################################################
        # Blocks
        ##################################################

        self._tx_gain_range = Range(0, 120, 1, 60, 200)
        self._tx_gain_win = RangeWidget(self._tx_gain_range, self.set_tx_gain, "'tx_gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._tx_gain_win)
        self._samp_rate_range = Range(5e6, 130e6, 1e6, 62.5e6, 200)
        self._samp_rate_win = RangeWidget(self._samp_rate_range, self.set_samp_rate, "'samp_rate'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._samp_rate_win)
        self._rx_gain_range = Range(0, 150, 1, 40, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, "'rx_gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rx_gain_win)
        self._freq_range = Range(1.700e9, 3.900e9, 500e3, 3.740e9, 200)
        self._freq_win = RangeWidget(self._freq_range, self.set_freq, "'freq'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._freq_win)
        self._alpha_range = Range(0, 1, 0.250, 0.350, 200)
        self._alpha_win = RangeWidget(self._alpha_range, self.set_alpha, "'alpha'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._alpha_win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(('addr=192.168.30.212', '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_gain(rx_gain, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(('addr=192.168.30.212', '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_sink_0.set_center_freq(freq, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_gain(tx_gain, 0)
        self.root_raised_cosine_filter_1 = filter.fir_filter_ccf(
            2,
            firdes.root_raised_cosine(
                1,
                samp_rate,
                symbol,
                alpha,
                taps))
        self.root_raised_cosine_filter_0 = filter.interp_fir_filter_fff(
            2,
            firdes.root_raised_cosine(
                1,
                samp_rate,
                symbol,
                alpha,
                taps))
        self.qtgui_vector_sink_f_0_1_0_1 = qtgui.vector_sink_f(
            fft_1,
            0,
            1,
            'Frequency(bin)',
            "dB",
            'CFR (Freq. domain Correlation)',
            3, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_1_0_1.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_1_0_1.set_y_axis((-140), 20)
        self.qtgui_vector_sink_f_0_1_0_1.enable_autoscale(True)
        self.qtgui_vector_sink_f_0_1_0_1.enable_grid(True)
        self.qtgui_vector_sink_f_0_1_0_1.set_x_axis_units("sample Index")
        self.qtgui_vector_sink_f_0_1_0_1.set_y_axis_units("dB")
        self.qtgui_vector_sink_f_0_1_0_1.set_ref_level(0)


        labels = ['Real', 'Imag', '20log', 'log20', 'mag2',
            '', '', '', '', '']
        widths = [1, 1, 4, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "green", "red", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(3):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_1_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_1_0_1.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_1_0_1.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_1_0_1.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_1_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_1_0_1_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_1_0_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_1_0_1_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_vector_sink_f_0_1_0 = qtgui.vector_sink_f(
            fft_1,
            0,
            1.0,
            '"FFT bin Length" in Time domain> sample/sampling rate',
            "Amplitude",
            'CIR using IFFT',
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_1_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_1_0.set_y_axis((-140), 10)
        self.qtgui_vector_sink_f_0_1_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0_1_0.enable_grid(True)
        self.qtgui_vector_sink_f_0_1_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_1_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_1_0.set_ref_level(0)


        labels = ['Magnitude', 'Mag^2', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_1_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_1_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_1_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_1_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_1_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_1_0_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_1_0_0 = qtgui.time_sink_f(
            128, #size
            samp_rate, #samp_rate
            "CIR (PN)", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_1_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_1_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_1_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_1_0_0.enable_tags(False)
        self.qtgui_time_sink_x_0_1_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_1_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_1_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_1_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_1_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_1_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_1_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_1_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_1_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_1_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_1_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_1_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_1_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_1_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_1_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_1_0_0_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0_1 = qtgui.freq_sink_c(
            4096, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            samp_rate, #bw
            'TX / RX', #name
            2,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0_1.set_y_axis((-120), 10)
        self.qtgui_freq_sink_x_0_0_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_1.enable_autoscale(True)
        self.qtgui_freq_sink_x_0_0_1.enable_grid(True)
        self.qtgui_freq_sink_x_0_0_1.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0_0_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0_1.set_fft_window_normalized(False)



        labels = ['Transmitter', 'Receiver', '', '', '',
            '', '', '', '', '']
        widths = [1, 4, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_0_1_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.fft_vxx_2 = fft.fft_vcc(fft_1, True, window.blackmanharris(fft_1), True, 1)
        self.fft_vxx_0_0 = fft.fft_vcc(fft_1, True, window.blackmanharris(fft_1), True, 1)
        self.fft_vxx_0 = fft.fft_vcc(fft_1, True, window.blackmanharris(fft_1), True, 1)
        self.digital_pn_correlator_cc_0 = digital.pn_correlator_cc(deg, 0, 1)
        self.digital_glfsr_source_x_0 = digital.glfsr_source_f(deg, True, 0, 1)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_1)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_1)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_float*1)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, fft_1, 0)
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(fft_1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(fft_1)
        self.blocks_complex_to_mag_0_1_0 = blocks.complex_to_mag(fft_1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(fft_1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_float_0, 1), (self.qtgui_vector_sink_f_0_1_0_1, 1))
        self.connect((self.blocks_complex_to_float_0, 0), (self.qtgui_vector_sink_f_0_1_0_1, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.qtgui_time_sink_x_0_1_0_0, 0))
        self.connect((self.blocks_complex_to_mag_0_1_0, 0), (self.qtgui_vector_sink_f_0_1_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.qtgui_freq_sink_x_0_0_1, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.fft_vxx_2, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.qtgui_vector_sink_f_0_1_0_1, 2))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0_0, 0))
        self.connect((self.digital_glfsr_source_x_0, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.digital_pn_correlator_cc_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.fft_vxx_2, 0), (self.blocks_complex_to_mag_0_1_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.root_raised_cosine_filter_1, 0), (self.digital_pn_correlator_cc_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_freq_sink_x_0_0_1, 1))
        self.connect((self.uhd_usrp_source_0, 0), (self.root_raised_cosine_filter_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "time_freq_correlation")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_symbol(self.samp_rate/1)
        self.qtgui_freq_sink_x_0_0_1.set_frequency_range(self.freq, self.samp_rate)
        self.qtgui_time_sink_x_0_1_0_0.set_samp_rate(self.samp_rate)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symbol, self.alpha, self.taps))
        self.root_raised_cosine_filter_1.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symbol, self.alpha, self.taps))
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symbol, self.alpha, self.taps))
        self.root_raised_cosine_filter_1.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symbol, self.alpha, self.taps))

    def get_symbol(self):
        return self.symbol

    def set_symbol(self, symbol):
        self.symbol = symbol
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symbol, self.alpha, self.taps))
        self.root_raised_cosine_filter_1.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symbol, self.alpha, self.taps))

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_freq_sink_x_0_0_1.set_frequency_range(self.freq, self.samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(self.freq, 0)
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)

    def get_fft_1(self):
        return self.fft_1

    def set_fft_1(self, fft_1):
        self.fft_1 = fft_1

    def get_deg(self):
        return self.deg

    def set_deg(self, deg):
        self.deg = deg

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symbol, self.alpha, self.taps))
        self.root_raised_cosine_filter_1.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.symbol, self.alpha, self.taps))

    def get_BW(self):
        return self.BW

    def set_BW(self, BW):
        self.BW = BW
        self.uhd_usrp_sink_0.set_bandwidth(self.BW, 0)
        self.uhd_usrp_source_0.set_bandwidth(self.BW, 0)




def main(top_block_cls=time_freq_correlation, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
