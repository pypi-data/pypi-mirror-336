#!/usr/bin/python3

import os
from binascii import b2a_hex
import pandas as pd
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage, LTChar, LTPage
from pathlib import Path
from io import StringIO


def with_pdf(pdf_doc, fn, pdf_pwd, *args):
    """Open the pdf document, and apply the function, returning the results"""
    result = None
    try:
        # open the pdf file
        fp = open(pdf_doc, "rb")
        # create a parser object associated with the file object
        parser = PDFParser(fp)
        # create a PDFDocument object that stores the document structure
        doc = PDFDocument(parser, pdf_pwd)
        # connect the parser and document objects
        parser.set_document(doc)

        if doc.is_extractable:
            # apply the function and return the result
            result = fn(doc, *args)

        # close the pdf file
        fp.close()
    except IOError:
        # the file doesn't exist or similar problem
        pass
    return result


# Table of Contents
def _parse_toc(doc):
    """With an open PDFDocument object, get the table of contents (toc) data
    [this is a higher-order function to be passed to with_pdf()]"""
    toc = []
    try:
        outlines = doc.get_outlines()
        for level, title, dest, a, se in outlines:
            toc.append((level, title))
    except PDFNoOutlines:
        pass
    return toc


def get_toc(pdf_doc, pdf_pwd=""):
    """Return the table of contents (toc), if any, for this pdf file"""
    return with_pdf(pdf_doc, _parse_toc, pdf_pwd)


# Extracting Images
def write_file(folder, filename, filedata, flags="w"):
    """Write the file data to the folder and filename combination
    (flags: 'w' for write text, 'wb' for write binary, use 'a' instead of 'w' for append)"""
    if os.path.isdir(folder):
        file_obj = open(os.path.join(folder, filename), flags)
        file_obj.write(filedata)
        file_obj.close()


# Extracting Text
def to_bytestring(s, enc="utf-8"):
    """Convert the given unicode string to a bytestring, using the standard encoding,
    unless it's already a bytestring"""
    if s:
        if isinstance(s, str):
            return s
        else:
            return s.encode(enc)


def update_page_text(df, lt_obj, pct=0.2):
    """
    Use the bbox x0,x1 values within pct% to produce lists of associated text within the hash

    df:
        cols = [x0, y0, x1, y1, class, objs, str]
    """
    if df is None:
        df = pd.DataFrame(columns=["x0", "y0", "x1", "y1", "class", "objs", "str"])

    if isinstance(lt_obj, (LTTextLine, LTTextBox)):
        store_new_line(df, lt_obj, pct)
    else:
        raise NotImplementedError(lt_obj)
    return df


def store_new_line(df, lt_obj, pct):
    """
    store a new line to df
    """
    x0, y0, x1, y1 = lt_obj.bbox
    candidates = df[
        (df["class"] == lt_obj.__class__)
        & (df["x0"] >= x0 * (1 - pct))
        & (df["x0"] <= x0 * (1 + pct))
        & (df["x1"] >= x1 * (1 - pct))
        & (df["x1"] <= x1 * (1 + pct))
        & (df["y1"] <= y0)
    ]

    if candidates.shape[0] > 0:
        target = candidates.iloc[0]
        df.at[target.name, "y0"] = y0
        df.at[target.name, "y1"] = y1
        df.at[target.name, "x0"] = x0
        df.at[target.name, "x1"] = x1
        df.at[target.name, "objs"].append(lt_obj)
        df.at[target.name, "str"].append(to_bytestring(lt_obj.get_text()))
    else:
        df.loc[0 if pd.isnull(df.index.max()) else df.index.max() + 1] = [
            *lt_obj.bbox,
            lt_obj.__class__,
            [lt_obj],
            [to_bytestring(lt_obj.get_text())],
        ]
    return df


def parse_lt_objs(lt_objs, page_number, images_folder, text_content=None, return_df=False):
    """Iterate through the list of LT* objects and capture the text or image data contained in each"""
    if text_content is None:
        text_content = []

    generator = lt_objs
    if page_number == 4:
        print(f"{page_number=}")

    page_text = None
    # k=(x0, x1) of the bbox, v=list of text strings within that bbox width (physical column)
    for lt_obj in generator:

        if isinstance(lt_obj, (LTTextBox, LTTextLine, LTChar)):
            print(f"lt_obj {lt_obj.bbox} -> {lt_obj.get_text()}")
            # text, so arrange is logically based on its column width
            page_text = update_page_text(page_text, lt_obj)
        elif isinstance(lt_obj, LTFigure):
            # LTFigure objects are containers for other LT* objects, so recurse through the children
            text_content.append(parse_lt_objs(lt_obj, page_number, images_folder, text_content, return_df=return_df))
        else:
            print(f"NOT PROCESSED: lt_obj {lt_obj.bbox} -> {type(lt_obj)}")

    if page_text is None:
        if return_df:
            return pd.DataFrame()
        else:
            return ""

    if return_df:
        text_content.append(page_text)
        return pd.concat(text_content)
    else:
        print(page_text)
        # page_text = page_text.sort_values(["y0", "x0"], ascending=[True, False])
        # print(page_text)
        # page_text = page_text.sort_values("x0")
        page_text = page_text["str"].apply(lambda x: text_content.append("".join(x)))
        return "".join(text_content) + "\n"


# Processing Pages
def _parse_pages(doc, images_folder, return_df=False):
    """With an open PDFDocument object, get the pages and parse each one
    [this is a higher-order function to be passed to with_pdf()]"""
    rsrcmgr = PDFResourceManager()
    laparams = LAParams(detect_vertical=True, all_texts=True)
    # all_texts will enable layout analysis in LTFigure objs
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    generator = enumerate(PDFPage.create_pages(doc))

    text_content = []
    for i, page in generator:
        interpreter.process_page(page)
        # receive the LTPage object for this page
        layout = device.get_result()
        # layout is an LTPage object which may contain child objects like LTTextBox, LTFigure, LTImage, etc.
        text_content.append(
            parse_lt_objs(
                layout,
                (i + 1),
                images_folder,
                return_df=return_df,
            )
        )

    if return_df:
        return pd.concat(text_content)
    else:
        return text_content


def _get_page_size(doc, images_folder):
    """With an open PDFDocument object, get the pages and parse each one
    [this is a higher-order function to be passed to with_pdf()]"""
    rsrcmgr = PDFResourceManager()
    laparams = LAParams(detect_vertical=True, all_texts=True)
    # all_texts will enable layout analysis in LTFigure objs
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    sizes = []
    for i, page in enumerate(PDFPage.create_pages(doc)):
        interpreter.process_page(page)
        # receive the LTPage object for this page
        layout = device.get_result()
        # layout is an LTPage object which may contain child objects like LTTextBox, LTFigure, LTImage, etc.
        sizes.append(layout.cropbox)
    return sizes


def get_pages(pdf_doc, pdf_pwd="", images_folder="/tmp", return_df=False):
    """Process each of the pages in this pdf file and return a list of strings representing the text found in each page"""
    return with_pdf(pdf_doc, _parse_pages, pdf_pwd, images_folder, return_df)


def get_sizes(pdf_doc, pdf_pwd=""):
    """get the sizes of each page"""
    return with_pdf(pdf_doc, _get_page_size, pdf_pwd)


# =============================================================================================================================

from .input_provider import InputProvider


def pdf_to_text(pdfname, codec="utf-8"):
    # PDFMiner boilerplate
    sio = StringIO()
    pages = get_pages(pdfname)

    sio.write("".join(pages))
    text = sio.getvalue()
    sio.close()

    return text


class PdfFileInputProvider(InputProvider):
    def __init__(self, fid):
        InputProvider.__init__(self, str(fid))
        fn = Path(self.id)
        self.cfn = fn.with_suffix("._txt")

    @property
    def text(self):
        if self.cfn.exists():
            with open(self.cfn) as fd:
                return fd.read()
        else:
            try:
                with open(self.cfn, "w") as fd:
                    data = pdf_to_text(self.id)
                    fd.write(data)
                    return data
            except Exception as ex:
                print("Cannot create cache file", ex)
                return pdf_to_text(self.id)
