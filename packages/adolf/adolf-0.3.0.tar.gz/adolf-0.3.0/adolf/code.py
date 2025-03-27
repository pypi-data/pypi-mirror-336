from IPython.display import Javascript, display

#from .tokenizer import tokenize
# from .wordcount import wordcount
# from .corpus import corpus
# from .grams import grams
# from .smoothing import smoothing
# from .pos import pos
# from .stopwords import stopwords
# from .stemming import stemming

from .slr import slr
from .mlr import mlr
from .blgr import blgr
from .mlgr import mlgr
from .dt import dt
from .gd import gd
from .km import km
from .knn import knn
from .ar import ar
from .nb import nb




def print_codes(codes):
    codes = codes[::-1]

    for code in codes:
        js_code = f'''
        var cell = Jupyter.notebook.insert_cell_below('code');
        cell.set_text(`{code}`);
        '''
        display(Javascript(js_code))



def code(program):
    codes = []
    if program == "19-12-18":
        codes = slr()
    elif program == "13-12-18":
        codes = mlr()
    elif program == "2-12-7-18":
        codes = blgr()
    elif program == "13-12-7-18":
        codes = mlgr()
    elif program == "4-20":
        codes = dt()
    elif program == "7-4":
        codes = gd()
    elif program == "11-13":
        codes = km()
    elif program == "11-14-14":
        codes = knn()
    elif program == "1-18":
        codes = ar()
    elif program == "14-2":
        codes = nb()
    elif program == "diddy":
        codes = [
            """
            SLR = 19-12-18

            MLR = 13-12-18

            BLGR = 2-12-7-18

            MLGR = 13-12-7-18

            DT = 4-20

            GD = 7-4

            KM = 11-13

            KNN = 11-14-14

            AR = 1-18

            NB = 14-2
            """
        ]
    else:
        codes = ["Nice Try Diddy"]
    print(codes)
    print_codes(codes)

code("19-12-18")

# def code(program):
#     if (1 == 1):
#         codes = []
#     elif program == "tokenize":
#         codes = tokenize()
#     elif program == "wordcount":
#         codes = wordcount()
#     elif program == "corpus":
#         codes = corpus()
#     elif program == "grams":
#         codes = grams()
#     elif program == "smoothing":
#         codes = smoothing()
#     elif program == "pos":
#         codes = pos()
#     elif program == "stopwords":
#         codes = stopwords()
#     elif program == "stemming":
#         codes = stemming()
#     else:
#         codes = []

#     print_codes(codes)