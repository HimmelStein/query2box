import pickle as pkl
import os, glob
import pandas as pd


dataNames = ['FB15k'] #, 'FB15k-237', 'NELL']
infoNames = ['ent2ind.pkl', 'rel2ind.pkl']


def decode_datasets(lst):
    def decode_tupe(tp):
        newKey = []
        for ele in tp:
            if isinstance(ele, tuple):
                newKey.append((infoDict['ent2ind'][ele[0]], [infoDict['rel2ind'][e] for e in ele[1]]))
            elif isinstance(ele, int) and ele > 0:
                newKey.append(infoDict['ent2ind'][ele])
            else:
                newKey.append(ele)
        return newKey
    for dt in lst:
        srcDir = "/Users/tdong/git/query2box/data/" + dt
        infoDir = "/Users/tdong/git/query2box/data/info/" + dt
        infoDict = {'ent2ind' : dict(), 'rel2ind': dict()}
        fb15kDic = dict()

        with open("/Users/tdong/git/query2box/data/info/FB15k/FB15k_mid2name.txt") as fh:
            for ln in fh:
                k, v = ln.split()
                fb15kDic[k] = v

        with open(os.path.join(infoDir, 'ent2ind.pkl'), 'rb') as fh:
            pklDict = pkl.load(fh)
            for k, v in pklDict.items():
                infoDict['ent2ind'][v] = fb15kDic.get(k, '')

        with open(os.path.join(infoDir, 'rel2ind.pkl'), 'rb') as fh:
            pklDict = pkl.load(fh)
            for k, v in pklDict.items():
                infoDict['rel2ind'][v] = k

        os.chdir(srcDir)
        for pklfile in glob.glob('*.pkl'):
            tfile = os.path.splitext(pklfile)[0]+ '.csv'
            tfile0 = os.path.splitext(pklfile)[0] + '.txt'
            print(tfile)
            lines = []
            lines0 = []
            with open(pklfile, 'rb') as pklHD:
                pklDict = pkl.load(pklHD)
                if type(pklDict) == list:
                    for tp in pklDict:
                        lines.append(decode_tupe(tp))
                        lines0.append(str(tp))
                else:
                    for key, value in pklDict.items():
                        lines.append(decode_tupe(key)+ [[" ".join([infoDict['ent2ind'][ele] for ele in value])]])
                        lines0.append("("+str(key) + " " + str(value)+")")
            pd.DataFrame(lines).to_csv(tfile, index=False)
            with open(tfile0, 'w') as ofh:
                ofh.writelines(lines0)
            print(pklfile)


if __name__ == "__main__":
    decode_datasets(dataNames)