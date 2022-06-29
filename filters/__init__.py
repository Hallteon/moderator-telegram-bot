from filters.bad_words_filter import Bad_Words_Filter
from loader import dp

if __name__ == "filters":
    dp.filters_factory.bind(Bad_Words_Filter)