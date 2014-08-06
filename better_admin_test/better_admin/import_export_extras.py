'''
Excel format support in django import export
'''
import warnings
import tablib
from xlrd import xldate_as_tuple, error_text_from_code

try:
    from tablib.compat import xlrd
    XLS_IMPORT = True
except ImportError:
    try:
        import xlrd  # NOQA
        XLS_IMPORT = True
    except ImportError:
        xls_warning = "Installed `tablib` library does not include"
        warnings.warn(xls_warning, ImportWarning)
        XLS_IMPORT = False

from import_export.formats import base_formats


def formatcell(book, celltype, cellvalue, wanttupledate):
    '''
    Properly formats the various cell types in an excel sheet.
    Deals with floats, dates and errors currently.
    '''
    # deal with floats
    if celltype == 2:
        if cellvalue == int(cellvalue):
            cellvalue = int(cellvalue)
        else:
            cellvalue = round(float(cellvalue), 5)
    # deal with dates
    elif celltype == 3:
        datetuple = xldate_as_tuple(cellvalue, book.datemode)
        if wanttupledate:
            cellvalue = datetuple
        else:
            cellvalue = stddate(datetuple)
    # deal with errors
    elif celltype == 5:
        cellvalue = error_text_from_code[cellvalue]
    return cellvalue


def stddate(tupledate):
    '''
    Converts tupledate to a valid date string.
    '''
    (y, m, d, H, M, S) = tupledate
    if not any([y, m, d]):
        return "%02d:%02d:%02d" % (H, M, S)
    else:
        return "%04d-%02d-%02d %02d:%02d:%02d" % (y, m, d, H, M, S)


class CustomXLS(base_formats.XLS):
    '''
    Custom XLS class of django-import-export XLS class define in
    import_export/formats/base_formats
    '''
    def create_dataset(self, in_stream):
        """
        Create dataset from first sheet.
        """
        assert XLS_IMPORT
        xls_book = xlrd.open_workbook(file_contents=in_stream)
        formatter = lambda(t, v): formatcell(xls_book, t, v, False)
        dataset = tablib.Dataset()
        sheet = xls_book.sheets()[0]
        for i in xrange(sheet.nrows):
            if i == 0:
                dataset.headers = sheet.row_values(0)
            else:
                (types, values) = (sheet.row_types(i), sheet.row_values(i))
                line = map(formatter, zip(types, values))
                dataset.append(line)
        return dataset
