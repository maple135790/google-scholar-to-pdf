from filterPdf import filterPdf
from download import download


if __name__ == "__main__":
    d = download()
    c = filterPdf()
    print("download pdf:", d)
    print("filtered pdf:", c)
