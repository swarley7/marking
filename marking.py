from collections import OrderedDict
import sys
import pyperclip

def test_stat(stattype, stat_max):
    while True:
        try:
            stat = float(raw_input('{} (/{}): '.format(stattype, stat_max)))
        except ValueError:
            pass
        else:
            if stat <= stat_max:
                return stat

stats = OrderedDict()
with open('marking_key.txt') as f:
    for line_num, line in enumerate(f.readlines()):
        if line.startswith('#'):
            continue
        line = line.strip().split(',')
        if not line:
            continue
        criteria = ' '.join(line[:-1])
        max_mark = line[-1]
        stats[criteria] = int(max_mark)

comments = OrderedDict()
with open('comments.txt') as f:
    for line_num, comment in enumerate(f.readlines()):
        comments[str(line_num)] = comment.strip()

total_vals = sum(stats.values())

while True:
    scores = {}
    for i in stats:
        scores[i] = test_stat(i, stats[i])
    total = sum(scores.values())
    text = ''
    sentinel = '..' # ends when this string is seen
    print('Comment: (type .. to finish)\n')
    scores['Comments'] = ''
    for i in comments:
        print('{}. {}'.format(i, comments[i]))
    while True:
        comment_num = raw_input('')
        if comment_num in comments.keys():
            scores['Comments'] += comments[comment_num] + '\n'
        if comment_num == '..':
            break
    print('Additional comment (type .. to finish):\n')
    for line in iter(raw_input, sentinel):
        text += '\n' + line # do things here
    scores['Comments'] += text

    sys.stdout.flush()
    feedback = ['Design\n {}/{}\n'.format(scores['Design'], stats['Design']),
        'Files read and write properly. Skills works as expected\n {}/{}\n'.format(scores['File I/O'], stats['File I/O']),
        'Functions called correctly and parameters passed correctly\n {}/{}\n'.format(scores['Functions'], stats['Functions']),
        'Code is written legibly (formatting, comments, etc)\n {}/{}\n'.format(scores['Formatting'], stats['Formatting']),
        'Program compiles correctly\n {}/{}\n'.format(scores['Compile'], stats['Compile']),
        'Output is as indicated\n {}/{}\n'.format(scores['Output'], stats['Output']),
        'Additional comments\n {}\n'.format(scores['Comments']),
        'Total\n {}/{}\n'.format(total, total_vals)]
    # copy text to clipboard
    pyperclip.setcb(''.join(feedback))

    # local echo of results
    print "*" * 40 + '\n'
    print ''.join(feedback)
    print "*" * 40 + '\n'