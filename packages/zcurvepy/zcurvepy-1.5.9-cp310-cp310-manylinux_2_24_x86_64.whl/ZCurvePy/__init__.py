__version__ = '1.5.9'
__upgrade__ = '2025-03-10'
f"""
    ZCurvePy -- High performance Python toolkit for the Z-curve theory!

    This is the Python package init module of ZCurvePy v{__version__} released.

    All the C/C++ apis can be called through this module. If you don't
    want to import additional third-party module (such as modules from
    scikit-learn) or APIs written in pure Python provided by ZCurvePy,
    (such as ZCurveBuilder), use 'import _ZCurvePy' instead of 'import
    ZCurvePy).

    Authors:    Zetong Zhang, Feng Gao
    Copyright:  Copyright 2025 TUBIC
    License:    MIT License
    Date:       {__upgrade__}

    Appendix Table:
            Correspondence between bases and chars in this software
    | char | base       | char | base       | char | base    | char | base    |
    |  A   | A          |  B   | C, G, T    |  C   | C       |  D   | A, G, T |
    |  E   | null       |  F   | null       |  G   | G       |  H   | A, C, T |
    |  I   | A, G, C, T |  J   | null       |  K   | G, T    |  L   | null    |
    |  M   | A, C       |  N   | A, G, C, T |  O   | null    |  P   | null    |
    |  Q   | null       |  R   | A, G       |  S   | G, C    |  T   | T       |
    |  U   | T          |  V   | A, G, C    |  W   | A, T    |  X   | null    |
    |  Y   | C, T       |  Z   | A          |

    [Remarks]:
    1.  'null' means the software will just skip the character when read strings;
    2.  Degenerate symbols will be handled using rule of frequency, for example:
        'M' will be regarded as 50% A + 50% C and vectorized as [0.5, 0, 0.5, 0]
    3.  'I' means hypoxanthine and may be paired with any type of bases; 'Z' means
        diaminopurine and can only be paired with 'A'. (Zhou Y, et al. Science, 
        2021, 372(6541): 512-516.)
"""
import sys
# Up regulate max recursion for ZCurveSegmenter
sys.setrecursionlimit(10000)
from operator import methodcaller
from copy import deepcopy
# Scikit-learn APIs
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler, MinMaxScaler
# Numpy Support
import numpy as np

# ZCurvePy C/C++ APIs (Classes)
from _ZCurvePy import ZCurveEncoder
from _ZCurvePy import ZCurvePlotter
# ZCurvePy C/C++ APIs (Multi-thread)
from _ZCurvePy import BatchZCurveEncoder
from _ZCurvePy import BatchZCurvePlotter
# ZCurvePy C/C++ APIs (Method)
from _ZCurvePy import shuffle
from _ZCurvePy import decode

class ZCurveBuilder:
    def __init__(
        self,
        encoder=None,
        model=None,
        standard=False,
        normal=False,
        neg_pos_ratio=10,
        seed=42,
        n_jobs=-1
    ):
        self.encoder = encoder
        if self.encoder is None:
            hyper_params = [
                {'n': 1, 'local': True},
                {'n': 2, 'local': True},
                {'n': 3, 'local': True}
            ]  # Final number of generated parameters: 189
            self.encoder = BatchZCurveEncoder(
                hyper_params=hyper_params,
                n_jobs=n_jobs
            )
        
        self.model = model
        if self.model is None:
            self.model = SVC(kernel='rbf')
        
        self.scaler = StandardScaler() if standard is True else None
        self.minmax = MinMaxScaler() if normal is True else None

        self.neg_pos_ratio = neg_pos_ratio
        self.seed = seed
        self.n_jobs = n_jobs
    
    @staticmethod
    def has_method(obj, method_name):
        return callable(getattr(obj, method_name, None))
    
    def fit(
        self, 
        pos_data,
    ):
        gen_seed = deepcopy(pos_data)
        gen_data = shuffle(
            records=gen_seed,
            ratio=self.neg_pos_ratio,
            seed=self.seed,
            n_jobs=self.n_jobs
        )
        pos_features = np.array(self.encoder(pos_data))
        neg_features = np.array(self.encoder(gen_data))

        pos_labels = np.ones(pos_features.shape[0])
        neg_labels = np.zeros(neg_features.shape[0])

        X = np.concatenate((pos_features, neg_features), axis=0)
        y = np.concatenate((pos_labels, neg_labels), axis=0)

        if self.scaler is not None:
            X = self.scaler.fit_transform(X)
        if self.minmax is not None:
            X = self.minmax.fit_transform(X)

        self.model.fit(X, y)
    
    def predict(
        self,
        data
    ):
        features = self.encoder(data)
        if self.scaler is not None:
            features = self.scaler.transform(features)
        if self.minmax is not None:
            features = self.minmax.transform(features)
        
        if self.has_method(self.model, "decision_function"):
            scores = self.model.decision_function(features)
            labels = np.array(scores > 0, dtype='int')
        elif self.has_method(self.model, "predict_proba"):
            scores = self.model.predict_proba(features)
            labels = np.array(scores > 0.5, dtype='int')
        else:
            raise Exception("Unsupported model types")
        
        return labels, scores


class ZCurveSegmenter:
    # Modes and their corresponding functions
    func = {
        'GN': 'genome_dS_curve',
        'RY': 'RY_dS_curve',
        'MK': 'MK_dS_curve',
        'WS': 'WS_dS_curve',
        'AT': 'AT_dS_curve',
        'GC': 'GC_dS_curve',
        'CG': 'CpG_dS_curve'
    }

    def __init__(
        self,
        mode,
        halting=100,
        min_len=3000,
        max_depth=9999
    ):
        self.mode = mode
        self.halting = halting
        self.min_len = min_len
        self.max_depth = max_depth
        self.executed = False
        self.seg_points = []
    
    def _recursion(
        self, 
        record, 
        offset: int, 
        depth: int
    ):
        plotter = ZCurvePlotter(record)
        max_point, max_value = methodcaller(self.func[self.mode], only_m=True)(plotter)
        left_len, right_len = max_point, len(record) - max_point

        if (max_value > self.halting and
            left_len >= self.min_len and right_len >= self.min_len):
            self.seg_points.append((max_point + offset, max_value))

            if depth < self.max_depth:
                # Segment left subsequence
                left_seq = record[:max_point]
                self._recursion(left_seq, offset, depth + 1)
                del left_seq
                # Segment right subsequence
                right_seq = record[max_point:]
                self._recursion(right_seq, offset + max_point, depth + 1)
                del right_seq
    
    def run(
        self, 
        record
    ):
        if not self.executed:
            self._recursion(record, 0, 0)
            self.seg_points.sort(key=lambda x : x[0])
            self.executed = True
            return self.seg_points
        else:
            raise Exception("Please reset the object first to segment another sequence!")
    
    def reset(self):
        self.seg_points = []
        self.executed = False