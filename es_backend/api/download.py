import os
import urllib.request

url_01 = "https://dumps.wikimedia.org/other/cirrussearch/current/jawikinews-20231106-cirrussearch-content.json.gz"
save_name_01 = "./wiki/jawikinews-20231106-cirrussearch-content.json.gz"

url_02 = "https://github.com/singletongue/WikiEntVec/releases/download/20190520/jawiki.all_vectors.200d.txt.bz2"
save_name_02 = "./wiki/jawiki.all_vectors.200d.txt.bz2"

def main():
    if os.path.exists("./wiki"):
        print("すでにWikiのファイルはダウンロード済み")
        return
    else:
        os.mkdir("./wiki")
        print("Downloading wiki files...")
        urllib.request.urlretrieve(url_01, save_name_01)
        urllib.request.urlretrieve(url_02, save_name_02)
        print("...Complete.")


if __name__=="__main__":
    main()