from pythumb import Thumbnail



def download_thumb(link, save_folder_path):
    t = Thumbnail(link)
    t.fetch()
    try:
        t.save(f'{save_folder_path}')
        return True
    except:
        return False