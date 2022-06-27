from dlgo.data.parallel_processor import GoDataProcessor
processor = GoDataProcessor()
generator = processor.load_go_data('train', 1, use_generator=True)
