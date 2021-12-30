# cfg_diff
Show differences in config files omitting some types of changes

    usage: dixf.py [-h] [--old OLD] [--new NEW] [--out OUT] [--ln_numbers]
                   [--forced_show] [--focus_in FOCUS_IN] [--run_tests] [-v]
    optional arguments:
      -h, --help           show this help message and exit
      --old OLD            Previous file name
      --new NEW            Next file name
      --out OUT            Output file name with simplified changes
      --ln_numbers         Show line numbers with insert/replace/equal/... actions
      --forced_show        Show difference lines before discarding known/ignored
                           replacements
      --focus_in FOCUS_IN  Focus on lines in old/previous file, for example: 4132,
                           4132-4162, 50- or -100
      --run_tests          Run tests
      -v, --verbose        Verbose output
