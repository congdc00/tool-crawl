from huggingface_hub import HfApi

api = HfApi(endpoint="https://huggingface.co", # Can be a Private Hub endpoint.
    token="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")
NAME_FILE  = "thumbsYT_12.zip"
api.upload_file(
    path_or_fileobj=f"data/output/{NAME_FILE}",
    path_in_repo=NAME_FILE,
    repo_id="congdc/imgs-collect",
    repo_type="dataset",
)