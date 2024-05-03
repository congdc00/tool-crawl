from huggingface_hub import snapshot_download
from huggingface_hub import HfApi

api = HfApi(endpoint="https://huggingface.co", # Can be a Private Hub endpoint.
    token="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")
api.snapshot_download(repo_id="congdc/thumb-youtube", local_dir="data/", repo_type="dataset")

