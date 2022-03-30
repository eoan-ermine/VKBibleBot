def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def page(lst, idx, rows_per_page):
    return lst[idx * rows_per_page:(idx + 1) * rows_per_page]
