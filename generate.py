#!python2
import os
import sys
import re


def checkWeekPresence(dirs):
    dirs = [int(x.split('_')[0]) for x in dirs]
    return dirs[-1] == len(dirs)

out = open('./notebook.tex', 'w+')
preamble = open('preamble.txt', 'r').read()

out.write(preamble)
out.write('\n')
out.writelines([r'\begin{document}', r'\tableofcontents', r'\newpage', r'\contentsfalse'])

weekDirs = [x for x in os.listdir('.') if x[:2].isdigit()]
print weekDirs
if not checkWeekPresence(weekDirs): sys.exit('week missing or misnamed')

for week in weekDirs:
    note = ''
    description = ''
    if 'note.txt' in os.listdir(week):
        noteLines = open(week + '/note.txt', 'r').read().split('\n')
        if len(noteLines) < 2 or len(noteLines[0]) < 1 or len(noteLines[1]) < 1:
            sys.exit('problem in note week' + week)
        note = '(' + noteLines[0] + ')'
        description = noteLines[1]

    out.write(r'\clearpage \newpage \section{Week \thesection} ' + note + '\n')
    if len(description) > 1:
        out.write(r'\subsubsection{' + description + '}\n')

    files = [x for x in os.listdir(week) if '.tex' in x]
    goals = []
    responses = []
    for file in files:
        i = 0
        name = ''
        prefix = ''
        if file[0] == 'h' or file[0]== 'H':
            name = 'Hardware'
            prefix = 'H'
        elif file[0] == 'b' or file[0] == 'B':
            name = 'Business'
            prefix = 'B'
        elif file[0] == 's' or file[0] == 'S':
            name = 'Software'
            prefix = 'S'
        else: sys.exit('invalid tex file week{} file {}'.format(week, file))

        content = open(week + '/' + file).read()
        start = content.find(r'\begin{document}')+16
        end = content.find(r'\end{document}')
        content = content[start:end]

        start = [m.start() for m in re.finditer('subsection{', content)] + [m.start() for m in re.finditer('subsection {', content)]
        if len(start) < 1:
            print 'week {} {} team is empty'.format(week, name)
            continue

        out.write(r'\subsection{' + name + ' Goals}\n')

        end = start[1:] + [len(content)]
        ranges = [(x-1, y-1) for x, y in zip(start, end)]
        for range in ranges:
            i += 1
            range = content[range[0]:range[1]]
            goal = range[range.find('{')+1:range.find('}')]
            goal = prefix + str(i) + ': ' + goal
            goals.append(goal)

            description = range[range.find('%!')+2:range.find('\n', range.find('%!'))]

            response = range[range.find('\n', range.find('%!')):]
            responses.append(response)

            out.write(r'\paragraph{' + goal + '}\n')
            out.write(description + '\n')

    out.write(r'\newpage' + '\n')
    for goal, response in zip(goals, responses):
        out.write(r'\subsection{' + goal + '}\n')
        out.write(response)

out.write(r'\end{document}')
out.close()
