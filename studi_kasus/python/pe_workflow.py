"""Pipeline pelatihan. Bukan model klinis."""
from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

NUM=['USIA','PARITAS']
CAT=['JARAK KELAHIRAN','RIW HIPERTENSI','OBESITAS','RIW DM',
     'RIW HIPERTENSI/PE DALAM KELUARGA','SOSEK RENDAH']
FEATURES=NUM+CAT
TARGET_MAP={'Non PE':0,'PE':1,'PEB':1,'Eklamsia':1,'PE gemelli':1,'PEB impending eklampsi':1}

def load_data(path):
    """Baca berkas penuh, bersihkan format, lalu pisahkan X dan y."""
    path=Path(path)
    data=pd.read_excel(path,sheet_name='2022') if path.suffix=='.xlsx' else pd.read_csv(path)
    data.columns=data.columns.str.strip()
    for col in data.select_dtypes(include='object'):
        data[col]=data[col].astype('string').str.strip().replace('',pd.NA)
    data['USIA']=pd.to_numeric(data['USIA'].astype('string').str.extract(r'(\d+)',expand=False),errors='coerce').astype(float)
    data['PARITAS']=pd.to_numeric(data['PARITAS'],errors='coerce').astype(float)
    unknown=set(data['PE/Non PE'].dropna())-set(TARGET_MAP)
    if unknown or data['PE/Non PE'].isna().any():
        raise ValueError(f'Label perlu ditelaah: {unknown}')
    X=data[FEATURES].copy()
    for col in CAT:
        X[col]=X[col].astype(object).where(X[col].notna(),np.nan)
    return X,data['PE/Non PE'].map(TARGET_MAP).astype(int)

def build_pipeline():
    numeric=Pipeline([('impute',SimpleImputer(strategy='median'))])
    category=Pipeline([('impute',SimpleImputer(strategy='most_frequent')),
                       ('encode',OneHotEncoder(handle_unknown='ignore',sparse_output=False))])
    prep=ColumnTransformer([('num',numeric,NUM),('cat',category,CAT)])
    tree=DecisionTreeClassifier(max_depth=3,min_samples_leaf=10,class_weight='balanced',random_state=42)
    return Pipeline([('preprocess',prep),('model',tree)])

def metrics(y,p):
    tn,fp,fn,tp=confusion_matrix(y,p,labels=[0,1]).ravel()
    return {'accuracy':float(accuracy_score(y,p)),
            'precision_PE':float(precision_score(y,p,zero_division=0)),
            'recall_PE':float(recall_score(y,p,zero_division=0)),
            'f1_PE':float(f1_score(y,p,zero_division=0)),
            'specificity':float(tn/(tn+fp)) if tn+fp else None,
            'TN':int(tn),'FP':int(fp),'FN':int(fn),'TP':int(tp)}

def train_export(root):
    """Reproduksi notebook 06 dan 07 dari data asli, lalu simpan semua hasil."""
    from sklearn.tree import export_text
    from sklearn.metrics import classification_report
    root=Path(root)
    case=root/'studi_kasus'
    X,y=load_data(case/'data/asli/dataKasus-1.xlsx')
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,stratify=y,random_state=42)
    pipe=build_pipeline().fit(Xtr,ytr)
    dummy=DummyClassifier(strategy='most_frequent').fit(Xtr,ytr)
    pred=pipe.predict(Xte)
    report={'rows':len(X),'class_counts':{str(k):int(v) for k,v in y.value_counts().items()},
            'train_rows':len(Xtr),'test_rows':len(Xte),'seed':42,
            'test_class_counts':{str(k):int(v) for k,v in yte.value_counts().items()},
            'sklearn_version':sklearn.__version__,'features':FEATURES,
            'excluded_from_model':['NO','NAMA','Unnamed: 12','RIW PE'],
            'decision_tree':metrics(yte,pred),
            'majority_baseline':metrics(yte,dummy.predict(Xte)),
            'limitations':'Split baris untuk pendidikan; independensi pasien, waktu pencatatan dan validitas label belum terverifikasi. Tidak untuk keputusan klinis.'}
    for folder in ['data/hasil','hasil','model']:(case/folder).mkdir(parents=True,exist_ok=True)
    clean=X.copy();clean['target_PE']=y
    clean.to_csv(case/'data/hasil/data_bersih.csv',index=False)
    cols=pipe.named_steps['preprocess'].get_feature_names_out()
    for label,xx,yy in [('train',Xtr,ytr),('test',Xte,yte)]:
        out=xx.copy();out.insert(0,'baris_sumber',xx.index+2);out['target_PE']=yy
        out.to_csv(case/f'data/hasil/{label}.csv',index=False)
        encoded=pd.DataFrame(pipe.named_steps['preprocess'].transform(xx),columns=cols,index=xx.index)
        encoded.insert(0,'baris_sumber',xx.index+2);encoded['target_PE']=yy
        encoded.to_csv(case/f'data/hasil/{label}_encoded.csv',index=False)
    predictions=pd.DataFrame({'baris_sumber':Xte.index+2,'aktual':yte,'prediksi':pred,
      'skor_PE':pipe.predict_proba(Xte)[:,list(pipe.classes_).index(1)]})
    predictions.to_csv(case/'hasil/prediksi_test.csv',index=False)
    pd.DataFrame({'baseline':report['majority_baseline'],'decision_tree':report['decision_tree']}).to_csv(case/'hasil/metrik.csv')
    (case/'hasil/classification_report.txt').write_text(classification_report(yte,pred,labels=[0,1],target_names=['Non PE','PE'],zero_division=0))
    (case/'hasil/aturan_pohon.txt').write_text(export_text(pipe.named_steps['model'],feature_names=list(cols)))
    destinations=[case/'model',root/'deployment/versi_2_hasil_studi_kasus/models']
    for out in destinations:
        out.mkdir(parents=True,exist_ok=True)
        joblib.dump(pipe,out/'pe_workshop_pipeline.joblib')
        (out/'model_card.json').write_text(json.dumps(report,indent=2))
    examples=X.iloc[[0,1,2]].copy()
    examples.to_csv(root/'deployment/versi_2_hasil_studi_kasus/data/contoh_input.csv',index=False)
    return pipe,report

if __name__=='__main__':
    print(json.dumps(train_export(Path(__file__).resolve().parents[2])[1],indent=2))
