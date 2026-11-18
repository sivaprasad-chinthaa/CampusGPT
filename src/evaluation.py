import pandas as pd

def hit_at_k(vectorstore, eval_csv, k=4):
    df=pd.read_csv(eval_csv)
    rows=[]
    for _,r in df.iterrows():
        docs=vectorstore.similarity_search(r['question'], k=k)
        expected=r['expected_source'].strip().lower()
        hit=any(expected in d.metadata.get('source','').lower() for d in docs)
        rows.append({"question":r['question'],"expected_source":r['expected_source'],f"hit@{k}":int(hit)})
    out=pd.DataFrame(rows)
    return out, float(out[f"hit@{k}"].mean())
