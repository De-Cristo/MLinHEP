"""hQuery"""

import multiprocessing as mp
import Queue
import html
import ast


def _start_backend(kws, q_in, q_out):
    from backend import HQueryBackend
    HQueryBackend(kws, q_in, q_out).start()


def _start_job_submitter(n_jobs, backend):
    if backend == 'jug':
        from varial_ext.treeprojector_jug_sge import SGESubmitter
        import varial_ext.treeprojector_jug as tp
        SGESubmitter(n_jobs, tp.jug_work_dir_pat, tp.jug_file_search_pat).start()

    if backend.startswith('spark://'):
        from varial_ext.treeprojector_spark_sge import SGESubmitter
        SGESubmitter(n_jobs, backend).start()


class HQueryEngine(object):
    def __init__(self, kws):
        self.messages = []

        self.backend_q_in = mp.Queue()
        self.backend_q_out = mp.Queue()
        self.backend_proc = None
        self.job_proc = None
        self.status = 'task pending'
        self.redirect = ''
        self.params = {}
        self.sel_info = {}

        self.start_job_submitter(kws)
        self.start_backend(kws)

    def start_job_submitter(self, kws):
        backend = kws.get('backend')
        if backend == 'local':
            return

        n_jobs = kws.pop('n_jobs', 100)
        self.job_proc = mp.Process(target=_start_job_submitter, args=(n_jobs, backend))
        self.job_proc.start()

    def start_backend(self, kws):
        self.backend_proc = mp.Process(
            target=_start_backend,
            args=(kws, self.backend_q_in, self.backend_q_out)
        )
        self.backend_proc.start()
        try:
            msg = self.backend_q_out.get(timeout=60)
        except Queue.Empty:
            msg = ''
        if msg != 'backend alive':
            raise RuntimeError('backend did not start after 60 seconds')

    def check_procs(self):
        if self.status == 'error':
            return

        if not self.backend_proc.is_alive():
            self.messages.append('ERROR: backend terminated.')
            self.status = 'error'

        if self.job_proc and not self.job_proc.is_alive():
            self.messages.append('ERROR: job submitter terminated.')
            self.status = 'error'

    def read_backend_q(self, timeout=None):
        block = bool(timeout)
        while True:
            try:
                item = self.backend_q_out.get(block, timeout)
            except Queue.Empty:
                break

            if item == 'task done' and self.status == 'task pending':
                self.status = 'ready'
                self.messages.append(item)
                with open('params.py') as f:
                    self.params, _, self.sel_info = ast.literal_eval(f.read())
            elif item.startswith('redirect:'):
                self.redirect = item.split(':')[1]
            else:
                self.messages.append(item)

    @staticmethod
    def _format_message(m):
        if m.startswith('WARN'):
            cls = 'warn'
        elif m.startswith('ERRO'):
            cls = 'err'
        else:
            cls = 'info'
        fmt = '<pre class="{cls}">{msg}</pre>'
        return fmt.format(cls=cls, msg=m)

    def write_messages(self, cont):
        placeholder = '<!-- MESSAGE -->'
        if 'task done' in self.messages:
            messages = self.messages
            while 'task done' in self.messages:
                messages.remove('task done')
            if html.msg_reload in messages:
                messages.remove(html.msg_reload)
            self.messages = []
        else:
            messages = self.messages
        message = '\n'.join(self._format_message(m) for m in messages)
        message = '<div class="msg">\n' + message + '\n</div>'

        return cont.replace(placeholder, message)

    def post(self, args, kws):
        self.read_backend_q()
        if self.status != 'ready':
            msg = 'WARNING: please wait for the last task to finish'
            if msg not in self.messages:
                self.messages.append(msg)
            return

        # submit task and wait for first answer
        self.backend_q_in.put(('post', args, kws))
        self.status = 'task pending'
        self.read_backend_q(.5)

    def get(self, path, cont):
        # check backend
        self.read_backend_q()
        self.check_procs()

        # compile html site
        depth = path.count('/')
        if not depth:
            cont = html.add_section_create_form(cont)
        elif depth == 1:
            section = path.split('/')[0]
            cont = html.add_section_manipulate_forms(cont, section)
            cont = html.add_histo_create_form(cont)
            cont = html.add_histo_manipulate_forms(
                cont, self.params, self.sel_info.get(section, {}))
        if self.redirect:
            cont = html.add_refresh(cont, 1, self.redirect)
            self.redirect = ''
        elif self.status == 'task pending':
            if html.msg_reload not in self.messages:
                self.messages.append(html.msg_reload)
            cont = html.add_refresh(cont, 3)
        cont = self.write_messages(cont)

        return cont

    def __del__(self):
        self.backend_q_in.put('terminate')
        self.backend_proc.join()
        if self.job_proc:
            self.job_proc.terminate()
            self.job_proc.join()
