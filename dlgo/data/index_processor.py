import os
import six
import sys
import multiprocessing
from urllib.request import urlopen
from urllib.request import urlretrieve

def worker(url_and_target):
    try:
        (url, target_path) = url_and_target
        print(f">>> Downloading {target_path}")
        urlretrieve(url, target_path)

    except (KeyboardInterrupt, SystemExit):
        print(f">>> Exiting child process")


class KGSIndex:
    def __init__(
            self,
            kgl_url = "http://u-go.net/gamerecords/",
            index_page = "kgs_index.html",
            data_directory = "data"
            ):
        self.kgl_url = kgl_url
        self.index_page = index_page
        self.data_directory = data_directory
        self.file_info = []
        self.urls = []
        self.load_index()


    def create_index_page(self):
        index_contents = None

        if os.path.isfile(self.index_page):
            print(">>> Reading cahed index page")

            with open(self.index_page, "r") as f:
                index_contents = f.read()
        else:
            print(">>> Downloading index page")
            fp = urlopen(self.kgl_url)
            data = six.text_type(fp.read())
            fp.close()
            index_contents = data


            with open(self.index_page, "w") as index_file:
                index_file.write(index_contents)

        return index_contents



    def load_index(self):
        index_contents = self.create_index_page()
        split_page = [item for item in index_contents.split('<a href="') if item.startswith("https://")]

        for item in split_page:
            download_url = item.split('">Download')[0]

            if download_url.endswith(".tar.gz"):
                self.urls.append(download_url)

        for url in self.urls:
            filename = os.path.basename(url)
            split_file_name = filename.split("-")
            num_games = int(split_file_name[len(split_file_name) - 2])
            self.file_info.append({"url" : url, "filename" : filename, "num_games" : num_games})


    def download_files(self):
        if not os.path.isdir(self.data_directory):
            os.makedirs(self.data_directory)
        else:
            if len(os.listdir(self.data_directory)) > 0:
                print(f"[*] There are data already downloaded in {self.data_directory}")
                return


        urls_to_download = []

        for file_info in self.file_info:
            url = file_info["url"]
            file_name = file_info["filename"]

            file_path = os.path.join(self.data_directory, file_name)

            if not os.path.isfile(file_path):
                urls_to_download.append((url, file_path))


        cores = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes = cores)


        try:
            it = pool.imap(worker, urls_to_download)

            for _ in it:
                pass

            pool.close()
            pool.join()

        except KeyboardInterrupt:
            print(">>> Caught KeyboardInterrupt, terminate workers")
            pool.terminate()
            pool.join()
            sys.exit(-1)






if __name__ == "__main__":
    index = KGSIndex()
    index.download_files()

