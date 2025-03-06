# ======================================================
# TA-Lib
import talib

# ======================================================
# basic library
import argparse
import warnings

import openpyxl
import pandas as pd
import numpy as np

import time
import math
import os
import os.path
import random
import shutil
import glob
import pickle

from tqdm import tqdm
from datetime import timedelta, datetime

# ======================================================
# Data preprocessing
from sklearn.preprocessing import MinMaxScaler

# ======================================================
# multiprocessing
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import multiprocessing

# ======================================================
# visualize
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter, MonthLocator

import seaborn as sns

import plotly.graph_objects as go
import plotly.subplots as ms
import plotly.express as px

import mplfinance as fplt
from mplfinance.original_flavor import candlestick2_ohlc, volume_overlay

from PIL import Image

import cv2
import csv

plt.rcParams['figure.dpi'] = 150
plt.rcParams['figure.max_open_warning'] = 0
from IPython.display import clear_output

# ======================================================
# torch
import torch
from transformers import ViTFeatureExtractor, ViTModel

# ======================================================
# similarity
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import euclidean, cityblock, chebyshev, minkowski, canberra, braycurtis
from scipy.stats import wasserstein_distance

from dtw import dtw
from fastdtw import fastdtw

# ======================================================
# similarity
import multiprocessing as mp

from itertools import groupby
from pathlib import Path

# ======================================================
limitations = [500, 400, 300, 200, 100, 75, 50, 25, 10, 5, 1] 