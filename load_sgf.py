from dlgo.data.processor import CustomDataProcessor

if __name__ == "__main__":
    path = "/home/musa/python_pro/working_go_data/sgf_data/KGS-2002-19-3646/KGS2002/2002-02-15-8.sgf"
    data_processor = CustomDataProcessor()
    data_processor.load_sgf(path = path)


