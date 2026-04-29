from huggingface_hub import snapshot_download
model_dir = './models/all-MiniLM-L6-v2'
snapshot_download(
    repo_id='sentence-transformers/all-MiniLM-L6-v2',
    local_dir=model_dir,
    endpoint='https://hf-mirror.com'
)