#!/usr/bin/env python

import sys, time

sys.dont_write_bytecode = True

from env_check.utils import TheRock, cstring
from env_check.device import Device
from env_check.check_tools import *
from env_check import check_therock


def main():
    therock_detect_start = time.perf_counter()
    device = Device()
    TheRock.__logo__()

    device.summary

    # check_therock.test_list().run()

    check_therock.test_list().summary

    therock_detect_terminate = time.perf_counter()
    therock_detect_time = float(therock_detect_terminate - therock_detect_start)
    therock_detect_runtime = cstring(f"{therock_detect_time:2f}", "hint")
    print(
        f"""
        ===========    TheRock build pre-diagnosis script completed in {therock_detect_runtime} seconds    ===========
    """
    )


if __name__ == "__main__":
    main()
