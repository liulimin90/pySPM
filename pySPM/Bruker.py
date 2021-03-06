# -- coding: utf-8 --

# Copyright 2018 Olivier Scholder <o.scholder@gmail.com>

"""
Module to handle SPM images recorded by a Bruker AFM
"""

import struct
import re
import numpy as np
import pySPM
import warnings


class Bruker:
    """
    Class to handle SPM images recorded by a Bruker AFM
    """

    def __init__(self, path):
        self.path = path
        self.file = open(self.path, 'rb')
        self.layers = []
        self.scanners = []
        mode = ''
        while True:
            line = self.file.readline().rstrip().replace(b'\\', b"")
            if line == b'*Ciao image list':
                self.layers.append({})
                mode = 'Image'
            elif line == b'*Scanner list':
                self.scanners.append({})
                mode = 'Scanner'
            else:
                args = line.split(b": ")
                if len(args) > 1:
                    if mode == 'Image':
                        self.layers[-1][args[0]] = args[1:]
                    elif mode == 'Scanner':
                        self.scanners[-1][args[0]] = args[1:]
                if line == b"*File list end":
                    break

    def _get_raw_layer(self, i):
        """
        Internal function to retrieve raw data of a layer
        """
        off = int(self.layers[i][b'Data offset'][0])
        cols = int(self.layers[i][b'Number of lines'][0])
        rows = int(self.layers[i][b'Samps/line'][0])
        self.file.seek(off)
        length = cols*rows
        return np.array(
            struct.unpack("<"+str(length)+"h", self.file.read(length*2)),
            dtype='float64').reshape((cols, rows))

    def load_image(self, channel="Height Sensor", backward=False, corr=None):
        warnings.warn(
            "Deprecated. Please use get_image() instead.", DeprecationWarning)
        return self.get_channel(channel, backward, corr=corr)

    def list_channels(self):
        print("Channels")
        print("========")
        for x in [z[b'@2:Image Data'][0] for z in self.layers]:
            print("\t"+x.decode('utf8'))

    def get_channel(self, channel="Height Sensor", backward=False, corr=None, debug=False):
        """
        Load the SPM image contained in a channel
        """
        for i in range(len(self.layers)):
            layer_name = self.layers[i][b'@2:Image Data'][0].decode('utf8')
            result = re.match(
                r'([^ ]+) \[([^\]]*)\] "([^"]*)"', layer_name).groups()
            if result[2] == channel:
                if debug:
                    print("channel "+channel+" Found!")
                bck = False
                if self.layers[i][b'Line Direction'][0] == b'Retrace':
                    bck = True
                if bck == backward:
                    if debug:
                        print("Direction found")
                    var = self.layers[i][b'@2:Z scale'][0].decode('utf8')
                    if '[' in var:
                        result = re.match(r'[A-Z]+\s+\[([^\]]+)\]\s+\([0-9\.]+ .*?\)\s+([0-9\.]+)\s+.*?$', var).groups()
                        scale = float(result[1])/65536.0
                        result = self.scanners[0][b'@'+result[0].encode('utf8')][0].split()
                        scale2 = float(result[1])
                        zscale = result[2].split(b'/')[0]
                        var = self.layers[i][b'@2:Z offset'][0].decode('utf8')
                        result = re.match(r'[A-Z]+\s+\[[^\]]+\]\s+\([0-9\.]+ .*?\)\s+([0-9\.]+)\s+.*?$', var).groups()
                        offset = float(result[0])
                    else:
                        result = re.match(r'[A-Z]+ \([0-9\.]+ [^\)]+\) ([0-9\.]+) [\w]+', var).groups()
                        scale = float(result[0])/65536.0
                        scale2 = 1
                        zscale = b'V'
                        result = re.match(r'[A-Z]+ \([0-9\.]+ .*?\) ([0-9\.]+) .*?', self.layers[i][b'@2:Z offset'][0].decode('utf8')).groups()
                        offset = float(result[0])
                    data = self._get_raw_layer(i)*scale*scale2

                    scan_size = self.layers[i][b'Scan Size'][0].split()
                    if scan_size[2][0] == 126:
                        scan_size[2] = b'u'+scan_size[2][1:]
                    size = {
                        'x': float(scan_size[0]),
                        'y': float(scan_size[1]),
                        'unit': scan_size[2].decode('utf8')}
                    image = pySPM.SPM_image(
                        channel=channel,
                        BIN=data,
                        real=size,
                        _type='Bruker AFM',
                        zscale=zscale.decode('utf8'),
                        corr=corr)
                    return image
        raise Exception("Channel {} not found".format(channel))