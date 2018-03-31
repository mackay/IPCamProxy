import sys
import traceback


def trace_narrative(line_prefix=""):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)

    err_body = ''.join(line_prefix + line for line in lines)

    return err_body
