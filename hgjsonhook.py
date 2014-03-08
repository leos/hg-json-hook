import re
import os
import traceback

try:
    import simplejson as json
except ImportError:
    import json

check_extension = 'json'
trailing_comma = re.compile('(,)(\s*[\]|}])')

# colors
BLUE = '\033[94m'
GREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

def run(ui, repo, hooktype, **kwargs):

    if hooktype not in ['precommit']:
        ui.write('Hook should be "precommit" not "%s".\n' % hooktype)
        return True

    files = filter(lambda x: x.endswith('.%s' % check_extension), repo[None].files())

    for f in files:
        data = repo[None][f].data()

        # Check for trailing commas
        matches = trailing_comma.finditer(data)
        
        fix_stack = []

        for match in matches:
            line_num = data.count('\n', 0, match.start(1)) + 1

            # catches not found case accidentally, because -1 turns into 0
            line_start = data.rfind('\n', 0, match.start(1)) + 1
            line_end = max(data.index('\n', match.end(2)), match.end(2))

            ui.write('Trailing comma in ' + GREEN + f + ENDC + \
                  ' at line ' + GREEN + str(line_num) + ENDC + \
                  ' char ' + GREEN + str(match.start(1) - line_start + 1) + \
                  ENDC + ':\n')
            ui.write(BLUE + data[line_start:match.start(1)] + \
             FAIL + ',' + BLUE + data[match.end(1):line_end] + ENDC + '\n')

            if ui.promptchoice('Want me to fix it? [Yn]: $$ &no $$ &yes', default = 1):
                fix_stack.append(match)

        # Fix in reverse order so that indexes are correct.
        while fix_stack:
            m = fix_stack.pop()
            data = data[:m.start(1)] + data[m.end(1):]

        with open(os.path.join(repo.root, f), 'wb') as fileobj:
            fileobj.write(data)

        try:
            json_object = json.loads(data)
        except Exception, e:
            ui.write('JSON parsing of ' + GREEN + f + FAIL + ' FAILED:' + ENDC + '\n')
            ui.write(e.message + '\n')
            return True
    return False
