from dlgo.data.processor import GoDataProcessor

def main():
    processor = GoDataProcessor()
    generator = processor.load_go_data('train', 100, use_generator=True)


if __name__ == "__main__":
    main()
