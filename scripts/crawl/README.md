# Hướng dẫn crawl 

## Youtube

### 1. Setup
Bước 1: Lấy API_KEY tại [Google cloud](https://console.cloud.google.com/apis/credentials?project=tool-crawl&supportedpurview=project)  
Bước 2: Đặt API_KEY vào api_key thư mục `env/config.yaml`

### 2. Crawl thumb youtube  
Run 
```
python -m scripts.crawl.thumb_youtube
```