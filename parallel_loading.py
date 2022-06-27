from dlgo.data.parallel_processor import GoDataProcessor
processor = GoDataProcessor()
generator = processor.load_go_data('train', 100, use_generator=True)
