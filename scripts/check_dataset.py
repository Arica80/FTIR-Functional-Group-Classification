"""Check curated labels, image presence and compound-wise split leakage.
Run: python scripts/check_dataset.py --images /path/to/FTIR_pngs
"""
import argparse
from pathlib import Path
import pandas as pd

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--images',required=True,type=Path)
    p.add_argument('--labels',type=Path,default=Path('data/labels_to_review.csv'))
    p.add_argument('--out',type=Path,default=Path('reports/dataset_check.json'))
    a=p.parse_args()
    df=pd.read_csv(a.labels,dtype=str).fillna('')
    label_cols=['label_alcohol','label_amine','label_ketone']
    complete=df[label_cols].isin(['0','1']).all(axis=1) & df['verified_compound_id'].str.strip().ne('')
    # Files can be nested by original family; exact basename may be ambiguous.
    all_png=list(a.images.rglob('*.png'))
    by_name={}
    for f in all_png: by_name.setdefault(f.name,[]).append(f)
    missing=[];ambiguous=[];present=0
    for name in df['arquivo']:
        matches=by_name.get(name,[])
        if not matches:missing.append(name)
        elif len(matches)>1:ambiguous.append(name)
        else:present+=1
    sub=df[complete & df['particao_historica'].isin(['treino','validacao','teste'])]
    leakage=[]
    for compound, group in sub.groupby('verified_compound_id'):
        splits=sorted(set(group['particao_historica']))
        if len(splits)>1: leakage.append({'compound':compound,'splits':splits})
    report={'inventory_records':len(df),'fully_reviewed_labels':int(complete.sum()),'unreviewed_labels':int((~complete).sum()),'uniquely_matched_images':present,'missing_filenames_count':len(missing),'ambiguous_filenames_count':len(ambiguous),'missing_filenames_sample':missing[:20],'ambiguous_filenames_sample':ambiguous[:20],'cross_split_compound_leakage':leakage,'training_ready':bool(complete.all() and not missing and not ambiguous and not leakage)}
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(__import__('json').dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    print(__import__('json').dumps(report,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
