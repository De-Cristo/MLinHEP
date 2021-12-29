import collections
import functools
import sys
import re

import wrappers


class History(object):
    """
    Tracking of operations provenance.

    >>> h = History('some_op')
    >>> print str(h)
    some_op()
    >>> h.add_args(['w1', 'w2'])
    >>> print str(h)
    some_op(
        'w1',
        'w2',
    )
    >>> h.add_kws({'a_keyword': 'a_value'})
    >>> print str(h)
    some_op(
        'w1',
        'w2',
        a_keyword='a_value',
    )
    >>> h
    some_op('w1','w2',a_keyword='a_value',)
    >>> h2 = History('another_op')
    >>> h2.add_args(['foo'])
    >>> h.add_args([h2])
    >>> print str(h)
    some_op(
        another_op(
            'foo',
        ),
        a_keyword='a_value',
    )
    >>> # new history test
    >>> h = History('other_op')
    >>> h.add_args([[History('w1'), History('w2')], 'bar'])
    >>> print str(h)
    other_op(
        [
            w1(),
            w2(),
        ],
        'bar',
    )
    """
    def __init__(self, operation):
        self.op   = str(operation)
        self.args = None
        self.kws  = None

    def __str__(self):
        string = ''
        if self.args:
            def arg_str(arg):
                if (
                    isinstance(arg, list)
                    and arg
                    and isinstance(arg[0], History)
                ):
                    return '[\n        ' + ',\n        '.join(
                        str(a).replace('\n', '\n        ') for a in arg
                    ) + ',\n    ]'
                elif isinstance(arg, History):
                    return str(arg).replace('\n', '\n    ')
                else:
                    return repr(arg)

            string += '\n'.join('    %s,' % arg_str(a) for a in self.args)
        if self.kws:
            string += '\n'
            string += '\n'.join(
                '    %s=%s,' % (k, repr(v)) for k, v in self.kws.iteritems())
        if string:
            return self.op + '(\n' + string + '\n)'
        else:
            return self.op + '()'

    def __repr__(self):
        pat = re.compile(r'\s+')
        return pat.sub('', str(self))

    def add_args(self, args):
        self.args = args

    def add_kws(self, kws):
        self.kws = kws


def _gen_catch_history(wrps, list_of_histories):
    for wrp in wrps:
        if hasattr(wrp, 'history'):
            list_of_histories.append(wrp.history)
        yield wrp


def track_history(func):
    """
    Python decorator for Wrapper operations.

    >>> @track_history
    ... def noop(wrps, arg, kw):
    ...     wrps = list(wrps)
    ...     return wrps[0]
    >>>
    >>> w1 = wrappers.Wrapper(history=History('w1'))
    >>> w2 = wrappers.Wrapper(history=History('w2'))
    >>> w3 = noop([w1,w2], 'an_arg', kw='a_kw')
    >>> print w3.history
    noop(
        [
            w1(),
            w2(),
        ],
        'an_arg',
        kw='a_kw',
    )
    """
    @functools.wraps(func)
    def history_tracker(*args, **kws):
        history = History(func.__name__)
        if len(args):
            func_args = list(args)
            hist_args = list(args)
            for i, arg in enumerate(args):
                if isinstance(arg, collections.Iterable) and not i:
                    list_of_histories = []
                    func_args[i] = _gen_catch_history(arg, list_of_histories)
                    hist_args[i] = list_of_histories
                elif isinstance(arg, wrappers.Wrapper):
                    hist_args[i] = arg.history
            history.add_args(hist_args)
            args = func_args
        if len(kws):
            history.add_kws(kws)
        try:
            ret = func(*args, **kws)
        except:
            etype, evalue, etb = sys.exc_info()
            if not 'history for unfinished wrapper: ' in evalue.message:
                evalue = etype(
                    '%s\nhistory for unfinished wrapper: %s' % (
                        evalue, str(history))
                )
            raise etype, evalue, etb
        ret.history = history
        return ret
    return history_tracker


if __name__ == '__main__':
    import doctest
    doctest.testmod()


