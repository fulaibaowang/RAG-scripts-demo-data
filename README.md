# RAG-scripts-demo-data

Small corpus, queries, **Terrier BM25** + **dense HNSW** indexes, and env files used by [RAG-scripts](https://github.com/fulaibaowang/RAG-scripts) CI (`run_retrieval_rerank_pipeline.sh`).

## Corpus layouts

Two parallel layouts exercise different **`docno`** conventions (see RAG-scripts docs). Everything else (queries, models, rerank settings) can stay the same; gold PMIDs in `data/queries.jsonl` still evaluate correctly because chunk ids map to PMIDs for metrics.

| Layout | Corpus file | Indexes | `docno` |
|--------|-------------|---------|---------|
| Baseline (PMID-only) | `data/docs.jsonl` | `indexes/bm25`, `indexes/dense` | bare PMID string |
| Chunked abstract | `data/docs_chunked.jsonl` | `indexes/bm25_chunked`, `indexes/dense_chunked` | `{pmid}#abstract` |

## Regenerating `docs_chunked.jsonl`

From the repo root:

```bash
python3 scripts/make_docs_chunked.py
```

Reads `data/docs.jsonl` and writes `data/docs_chunked.jsonl` with `docno = "{pmid}#abstract"`.

## Rebuilding indexes (chunked corpus)

Paths below assume this repo is mounted at `/demo` and RAG-scripts at `/work` (as in CI Docker).

```bash
python /work/index/build_bm25_index_from_jsonl_shards.py \
  --jsonl_glob "/demo/data/docs_chunked.jsonl" \
  --index_path "/demo/indexes/bm25_chunked" \
  --threads 2 --overwrite

python /work/index/build_dense_hnsw_index_from_jsonl_shards.py \
  --jsonl_glob "/demo/data/docs_chunked.jsonl" \
  --out_dir "/demo/indexes/dense_chunked" \
  --device cpu \
  --batch_size 32 \
  --model_name abhinand/MedEmbed-small-v0.1
```

Dense output must include `hnsw_index.bin`, `meta.json`, and `rowid_to_docno.tsv`.

## Config / CI

- Baseline pipeline: `config.env` → writes under `output/` (path `WORKFLOW_OUTPUT_DIR`).
- Chunked pipeline: `config.chunked.env` → writes under `output_chunked/`.

Upstream CI runs both in parallel (matrix); see RAG-scripts `.github/workflows/ci.yml`.
