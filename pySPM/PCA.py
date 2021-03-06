# -- coding: utf-8 --

# Copyright 2018 Olivier Scholder <o.scholder@gmail.com>

"""
This module performs the PCS with the help of the scikit library and gives the user various function for quick plotting.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA as PCA1
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from scipy import stats
import matplotlib.pyplot as plt
from pySPM.SPM import SPM_image
import matplotlib as mpl
from matplotlib import cm
from pySPM import collection
import re

class PCA:

    def __init__(self, data):
        self.data = data
        self.pca = None
        self.standX = None

    def scatter(self, **kargs):
        pd.tools.plotting.scatter_matrix(self.data, diagonal="kde", **kargs)
        plt.tight_layout()

    def corr(self):
        corrmat = self.data.corr()
        return corrmat

    def corrShow(self):
        import seaborn as sns
        corrmat = self.corr()
        sns.heatmap(corrmat).xaxis.tick_top()

    def hinton(self, max_weight=None, ax=None, matrix = None, xlabel=None, ylabel=None):
        """Draw Hinton diagram for visualizing a weight matrix."""
        if matrix is None:
            matrix = self.corr()
        ax = ax if ax is not None else plt.gca()

        if not max_weight:
            max_weight = 2**np.ceil(np.log(np.abs(matrix).max())/np.log(2))

        ax.patch.set_facecolor('lightgray')
        ax.set_aspect('equal', 'box')
        ax.xaxis.set_major_locator(plt.NullLocator())
        ax.yaxis.set_major_locator(plt.NullLocator())

        for (x, y), w in np.ndenumerate(matrix):
            color = 'red' if w > 0 else 'blue'
            size = np.sqrt(np.abs(w))
            rect = plt.Rectangle([y - size / 2, x - size / 2], size, size,
                                 facecolor=color, edgecolor=color)
            ax.add_patch(rect)

        nxticks = matrix.shape[1]
        nyticks = matrix.shape[0]
        if xlabel is None:
            xlabel = []
            for x in list(matrix.columns):
                x = re.sub(r'\^([0-9]+)',r'^{\1}', x)
                x = re.sub(r'_([0-9]+)',r'_{\1}', x)
                if x[-1] in ['+','-']:
                    x = x[:-1]+'^'+x[-1]
                xlabel.append('$'+x+'$')
        if ylabel is None:
            ylabel = list(matrix.index)
        ax.xaxis.tick_top()
        ax.set_xticks(range(nxticks))
        ax.set_xticklabels(xlabel, rotation=90)
        ax.set_yticks(range(nyticks))
        ax.set_yticklabels(ylabel)
        ax.grid(False)

        ax.autoscale_view()
        ax.invert_yaxis()

    def standardized(self, meanCentering=True):
        self.standX = pd.DataFrame(
            scale(self.data, with_mean=meanCentering), index=self.data.index, columns=self.data.columns)
        return self.standX

    def runPCA(self, meanCentering=True):
        if self.standX is None:
            self.standardized(meanCentering=meanCentering)
        self.pca = PCA1().fit(self.standX)

    def pca_summary(self):
        if self.pca is None:
            self.runPCA()
        names = ["PC"+str(i)
                 for i in range(1, len(self.pca.explained_variance_ratio_)+1)]
        a = list(np.std(self.pca.transform(self.standX), axis=0))
        b = list(self.pca.explained_variance_ratio_)
        c = [np.sum(self.pca.explained_variance_ratio_[:i])
             for i in range(1, len(self.pca.explained_variance_ratio_)+1)]
        columns = pd.MultiIndex.from_tuples([("sdev", "Standard deviation"), (
            "varprop", "Proportion of Variance"), ("cumprop", "Cumulative Proportion")])
        Z = zip(a, b, c)
        summary = pd.DataFrame(list(Z), index=names, columns=columns)
        return summary

    def screeplot(self, ax=None, num=None):
        if self.pca is None:
            self.runPCA()
        ax = ax if ax is not None else plt.gca()
        
        y = np.std(self.pca.transform(self.standX), axis=0)**2
        if num is None:
            num = len(y)
        x = np.arange(len(y)) + 1
        ax.grid(True)
        ax.plot(x[:num], y[:num], "o-")
        ax.set_xticks(x[:num])
        ax.set_xticklabels(["PC"+str(i) for i in x[:num]], rotation=60)
        ax.set_ylabel("Variance")

    def pc(self, id=0):
        # find the number of samples in the data set and the number of
        # variables
        if self.pca is None:
            self.runPCA()
        pc = np.matmul(self.standX.as_matrix(), self.pca.components_[id].T)
        return pc

    def loadings(self, id=None):
        if self.pca is None:
            self.runPCA()
        if id is not None:
            return pd.DataFrame(self.pca.components_[id, None], columns=self.data.columns)
        return pd.DataFrame(self.pca.components_, columns=self.data.columns, index=["PC{0}".format(i+1) for i in range(len(self.pca.components_))])

    def getPCAtransf(self):
        if self.pca is None:
            self.runPCA()
        return self.pca.transform(self.standX)

    def showStand(self):
        return pd.DataFrame([self.standX.apply(np.mean), self.standX.apply(np.std)], index=['Mean', 'Std'])

    def pca_scatter(self, classifs=None, light=False):
        import seaborn as sns
        foo = self.getPCAtransf()
        if classifs is None:
            if light:
                plt.scatter(foo[:, 0], foo[:, 1])
            else:
                bar = pd.DataFrame(
                    list(zip(foo[:, 0], foo[:, 1])), columns=["PC1", "PC2"])
                sns.lmplot("PC1", "PC2", bar, fit_reg=False)
        else:
            if light:
                plt.scatter(foo[:, 0], foo[:, 1], color=cm.Scalar)
            else:
                bar = pd.DataFrame(list(zip(foo[:, 0], foo[:, 1], classifs)), columns=[
                                   "PC1", "PC2", "Class"])
                sns.lmplot("PC1", "PC2", bar, hue="Class", fit_reg=False)


class ITA_PCA(PCA):

    def __init__(self, c, channels=None):
        """Init a PCA class from a collection"""
        self.col = c
        if channels is None:
            channels = c.channels.keys()
        mul = self.col.get_multivariate(channels)
        PCA.__init__(self, mul)

    def showPCA(self, num=None, ax=None, **kargs):
        c = self.getPCAcol(num)
        c.show(ax=ax, cmap='hot', **kargs)

    def getPCAcol(self, num=None):
        if num is None:
            num = self.data.shape[1]
        assert num <= self.data.shape[1]
        PCA_col = collection.Collection(
            cls=self.col, name=self.col.name+"[PCA]")
        for i in range(num):
            PC = self.getPCA(i)
            PCA_col.add(PC, 'PC{0}'.format(i+1))
        return PCA_col

    def getPCA(self, id=0):
        s = list(self.col.channels.values())[0].pixels.shape
        PC = self.pc(id).reshape(s)
        return PC
