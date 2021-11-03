# compare variables files

import sys
from tfvcomp import tfvcomp
import traceback


if __name__ == '__main__':
    # get args
    files = sys.argv[1:]

    try:
        tfvcomp.checkexist(files)
        tfvcomp.createoutput(files)
        tfvcomp.appendvariables(files)
    except Exception as e:
        print(str(e))
        print((traceback.format_exc()))
        print("Aborting")