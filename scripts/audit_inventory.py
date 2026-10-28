from pathlib import Path
import pandas as pd
import json

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "inventory_498.csv", dtype=str).fillna("")
summary = {
    "total": len(df),
    "families": df["familia_original"].value_counts().to_dict(),
    "partitions": df["particao_historica"].value_counts().to_dict(),
    "structure_status": df["status_estrutura"].value_counts().to_dict(),
    "train_decision": df["decisao_para_treino"].value_counts().to_dict(),
    "repeated_compound_ids": int(df.duplicated("composto_id").sum()),
    "duplicate_sha256": int(df.duplicated("sha256").sum()),
}
# Identify compounds appearing across training/validation/test partitions.
active = df[df["particao_historica"].isin(["treino", "validacao", "teste"])]
splits_per_compound = active.groupby("composto_id")["particao_historica"].nunique()
summary["compounds_crossing_splits"] = int((splits_per_compound > 1).sum())
print(json.dumps(summary, ensure_ascii=False, indent=2))
