#!/usr/bin/env python
import sys
from optparse import OptionParser
from ExecutionEngine import ExecutionEngine
import settings
import os

if __name__ == "__main__":

    parser = OptionParser()

    parser.add_option("--verbose", action="store_true", dest="verbose", default = False,
                      help="Enable verbose output from exploits", metavar="VERBOSE")

    #option for running a single application
    parser.add_option("--manual", action="store_true", dest="manual_config",
                      help="Manual run mode", metavar="APP__CONTAINER")

    #option for running all exploits in a batch
    parser.add_option("--batch", action="store_true", dest="batch_config",
                      help="Batch run mode", metavar="BATCH__RUN")

    parser.add_option("--image", action="store", dest="image",
                      help="Batch run mode", metavar="IMAGE")


    #specify mapped_port_in for the server (the default is "8888" for node.js)
    parser.add_option("--mappedPort", action="store", dest="mapped_port",
                      help="Mapped input port for the web server", metavar="MAPPED_PORT")

    parser.add_option("--results", action="store", dest="results_filename", default = settings.results_filename,
                      help="Destination file of test results", metavar="RESULTS")

    parser.add_option("--exploit", action="store", dest="exploit",
                      help="Exploit that must be run on the target application-specific container", metavar="EXPLOIT.py")

    parser.add_option("--spoiled", action="store_true", dest="spoiled", default=settings.spoiled_mode,
                      help="This flag indicates that app-specific container must be reused (for batch mode only).\n Currently works if '--target' attribute is not specified", metavar="SPOILED")

    parser.add_option("--visible", action="store_true", dest="visible", default=settings.browser_visible,
                      help="This flag indicates if browser is visible during the exploit execution")

    parser.add_option("--disposable", action="store_true", dest="disposable", default=False,
                        help="This flag indicates whether the app-specific container image should be disposed after the run")



    (options, args) = parser.parse_args()

    ex = ExecutionEngine()
    settings.disposable = options.disposable

    if (options.visible):
        settings.browser_visible = options.visible

    if (options.mapped_port):
        settings.mapped_port_in = options.mapped_port

    if (options.verbose):
        settings.report_verbosity = "DEBUG"
    else:
        settings.report_verbosity = "INFO"

    if (options.results_filename):
        settings.results_filename = options.results_filename

    if (options.image):
        options.image = os.path.join(settings.configurations_path, options.image)
        if (options.exploit):
            ex.run(options.image, options.exploit)
        elif(options.manual_config):
            ex.run_manual(options.image)
        else:
            if (options.batch_config):
                settings.spoiled_mode = False if (options.image == None) else options.spoiled
                ex.run_all(options.image)
    else:
        if (options.batch_config):
            ex.run_all(None)
        else:
            parser.print_help()
