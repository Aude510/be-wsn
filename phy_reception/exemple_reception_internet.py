#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.8.1.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
import sip
from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio.qtgui import Range, RangeWidget
from gnuradio import qtgui

class exemple_reception_internet(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
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

        self.settings = Qt.QSettings("GNU Radio", "exemple_reception_internet")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 2
        self.samp_rate = samp_rate = 1500000
        self.qpsk = qpsk = digital.constellation_qpsk().base()
        self.loop_bw = loop_bw = 0.35
        self.gain = gain = 30
        self.freq_centr = freq_centr = 863200000
        self.damping_factor = damping_factor = 0.5
        self.bpsk = bpsk = digital.constellation_bpsk().base()

        ##################################################
        # Blocks
        ##################################################
        self._loop_bw_range = Range(0, 1, 0.1, 0.35, 200)
        self._loop_bw_win = RangeWidget(self._loop_bw_range, self.set_loop_bw, 'loop_bw', "counter_slider", float)
        self.top_grid_layout.addWidget(self._loop_bw_win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_center_freq(freq_centr, 0)
        self.uhd_usrp_source_0.set_gain(gain, 0)
        self.uhd_usrp_source_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec())
        self.qtgui_const_sink_x_2_0 = qtgui.const_sink_c(
            1024, #size
            "costas output", #name
            1 #number of inputs
        )
        self.qtgui_const_sink_x_2_0.set_update_time(0.10)
        self.qtgui_const_sink_x_2_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_2_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_2_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_2_0.enable_autoscale(False)
        self.qtgui_const_sink_x_2_0.enable_grid(False)
        self.qtgui_const_sink_x_2_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_2_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_2_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_2_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_2_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_2_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_2_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_2_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_2_0_win = sip.wrapinstance(self.qtgui_const_sink_x_2_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_2_0_win)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(loop_bw, 2, True)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(bpsk)
        self.digital_cma_equalizer_cc_0 = digital.cma_equalizer_cc(1, 1, 1, 2)
        self._damping_factor_range = Range(0, 1, 0.1, 0.5, 200)
        self._damping_factor_win = RangeWidget(self._damping_factor_range, self.set_damping_factor, 'damping_factor', "counter_slider", float)
        self.top_grid_layout.addWidget(self._damping_factor_win)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/home/aude/be-wsn/debug/reception', False)
        self.blocks_file_sink_0.set_unbuffered(False)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.digital_cma_equalizer_cc_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_const_sink_x_2_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.digital_cma_equalizer_cc_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "exemple_reception_internet")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_qpsk(self):
        return self.qpsk

    def set_qpsk(self, qpsk):
        self.qpsk = qpsk

    def get_loop_bw(self):
        return self.loop_bw

    def set_loop_bw(self, loop_bw):
        self.loop_bw = loop_bw
        self.digital_costas_loop_cc_0.set_loop_bandwidth(self.loop_bw)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_source_0.set_gain(self.gain, 0)

    def get_freq_centr(self):
        return self.freq_centr

    def set_freq_centr(self, freq_centr):
        self.freq_centr = freq_centr
        self.uhd_usrp_source_0.set_center_freq(self.freq_centr, 0)

    def get_damping_factor(self):
        return self.damping_factor

    def set_damping_factor(self, damping_factor):
        self.damping_factor = damping_factor

    def get_bpsk(self):
        return self.bpsk

    def set_bpsk(self, bpsk):
        self.bpsk = bpsk



def main(top_block_cls=exemple_reception_internet, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
