import numpy as np

class MyMatrix(np.ndarray):
    def _new_(cls, shape):
        obj = np.zeros(shape, dtype=np.dtype([('index', ('i4', 2)), ('value', 'f8')]), align=True).view(cls)
        return obj

    def _getitem_(self, key):
        if isinstance(key, tuple) and len(key) == 2 and isinstance(key[0], tuple) and isinstance(key[1], tuple) and len(key[0]) == 2 and len(key[1]) == 2 and key[0] == key[1]:
            return 0
        else:
            return super(MyMatrix, self)._getitem_(key)

Q1=MyMatrix((16,16))
Q1[(0,0)][(0,0)]