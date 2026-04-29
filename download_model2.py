from huggingface_hub import hf_hub_download, snapshot_download
import os

# 设置HF国内镜像
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# 下载模型
snapshot_download(
    repo_id='sentence-transformers/all-MiniLM-L6-v2',
    local_dir='./models/all-MiniLM-L6-v2',
    local_dir_use_symlinks=False
)

print("模型下载完成！")
