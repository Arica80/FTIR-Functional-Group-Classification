"""Three-label HOG + OneVsRest LogisticRegression baseline after label validation.
Requires confirmed image-label association and a leakage-free group-wise split.
No metrics are generated unless there are enough reviewed compounds in both folds.
"""
import argparse,json
from pathlib import Path
import numpy as np,pandas as pd
from PIL import Image
from skimage.feature import hog
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import f1_score,classification_report
from sklearn.model_selection import GroupShuffleSplit

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--images',type=Path,required=True)
    p.add_argument('--labels',type=Path,default=Path('data/labels_to_review.csv'))
    p.add_argument('--out',type=Path,default=Path('reports/baseline_results.json'))
    a=p.parse_args()
    df=pd.read_csv(a.labels,dtype=str).fillna('')
    cols=['label_alcohol','label_amine','label_ketone']
    good=df[cols].isin(['0','1']).all(axis=1) & df.verified_compound_id.str.strip().ne('')
    df=df[good].copy()
    if len(df)<30 or df.verified_compound_id.nunique()<10:raise SystemExit('Insufficient reviewed compound-level labels. No model trained.')
    by_name={}
    for f in a.images.rglob('*.png'):by_name.setdefault(f.name,[]).append(f)
    x=[];y=[];groups=[]
    for _,r in df.iterrows():
        matches=by_name.get(r.arquivo,[])
        if len(matches)!=1:raise SystemExit(f'Image missing or ambiguous: {r.arquivo}')
        arr=np.asarray(Image.open(matches[0]).convert('L').resize((256,128)),dtype=np.uint8)
        x.append(hog(arr,pixels_per_cell=(16,16),cells_per_block=(2,2),feature_vector=True))
        y.append([int(r[c]) for c in cols]);groups.append(r.verified_compound_id)
    x=np.array(x);y=np.array(y);groups=np.array(groups)
    train,test=next(GroupShuffleSplit(n_splits=1,test_size=.2,random_state=42).split(x,y,groups))
    if any(len(np.unique(y[train,j]))<2 for j in range(3)):
        raise SystemExit('Training subset lacks both classes for one or more labels. No metrics generated.')
    model=OneVsRestClassifier(LogisticRegression(max_iter=3000,class_weight='balanced',random_state=42))
    model.fit(x[train],y[train]);pred=model.predict(x[test])
    out={'note':'Exploratory baseline; do not infer external generalization','sample_count':len(x),'unique_compounds':len(set(groups)),'train_count':len(train),'test_count':len(test),'split':'GroupShuffleSplit by verified_compound_id (seed 42)','macro_f1':float(f1_score(y[test],pred,average='macro',zero_division=0)),'micro_f1':float(f1_score(y[test],pred,average='micro',zero_division=0)),'per_label':classification_report(y[test],pred,target_names=cols,output_dict=True,zero_division=0)}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps({'macro_f1':out['macro_f1'],'micro_f1':out['micro_f1'],'test_count':len(test)},indent=2))

if __name__=='__main__': main()
