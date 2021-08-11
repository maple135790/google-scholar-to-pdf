import fitz
import shutil
import glob


def filterPdf() -> int:
    origPdfPath = ".\\pdf"
    filteredPdfPath = ".\\pdf_filtered"
    filteredCount = 0
    with open("filter.log", "w") as LogF:
        for file in glob.glob(origPdfPath + "\\*.pdf"):
            filename = file.split('\\')[-1]
            with fitz.open(file) as doc:
                text = ""
                for page in doc:
                    text += page.getText(text)
            if ('Table' or 'chart') in text:
                shutil.copyfile(origPdfPath + "\\" + filename,
                                filteredPdfPath + "\\" + filename)
                print("[I]interesting {}".format(filename))
                LogF.write("[I]interesting {}\n".format(filename))
                filteredCount += 1
            else:
                print("[I]not interesting {}".format(filename))
                LogF.write("[I]not interesting {}\n".format(filename))
    return filteredCount
