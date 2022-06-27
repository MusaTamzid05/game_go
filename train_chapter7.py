from dlgo.data.processor import GoDataProcessor

def main():
    processor = GoDataProcessor(data_directory = "data_processed")
    generator = processor.load_go_data("train", 100, use_generator=True)

    for i in range(10):
        x, y = next(generator.generate(batch_size = 128, num_classes = 19 * 19))
        print(x.shape, y.shape)





if __name__ == "__main__":
    main()
