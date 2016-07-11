import angr
import nose
import identifier

import os
bin_location = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../binaries-private'))

import logging
logging.getLogger("identifier").setLevel("DEBUG")

# smoketest
def test_palindrome():
    """
    Test identification of functions in palindrome.
    """

    p = angr.Project(os.path.join(bin_location, "cgc_scored_event_1/cgc/0b32aa01_01"))
    idfer = identifier.Identifier(p)

    seen = dict()
    for addr, symbol in idfer.run():
        seen[addr] = symbol

    nose.tools.assert_equals(seen[134513765], "receive_n4")

def test_comparison_identification():
    """
    Test identification of common comparison functions
    """

    true_symbols = {0x804a0f0: 'strcmp', 0x8048e60: 'memcmp', 0x8049f40: 'strcasecmp'}

    p = angr.Project(os.path.join(bin_location, "tests/i386/identifiable"))
    idfer = identifier.Identifier(p)

    seen = dict()
    for addr, symbol in idfer.run():
        seen[addr] = symbol

    for addr, symbol in true_symbols.items():
        nose.tools.assert_equal(true_symbols[addr], seen[addr])

def run_all():
    functions = globals()
    all_functions = dict(filter((lambda (k, v): k.startswith('test_')), functions.items()))
    for f in sorted(all_functions.keys()):
        if hasattr(all_functions[f], '__call__'):
            all_functions[f]()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        globals()['test_' + sys.argv[1]]()
    else:
        run_all()
