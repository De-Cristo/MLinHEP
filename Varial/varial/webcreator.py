import traceback
import itertools
import datetime
import sys
import os

import toolinterface
import settings
import analysis
import wrappers
import sparseio
import diskio
import util


class WebCreator(toolinterface.Tool):
    """
    Generates webpages for all directories.

    WebCreator instanciates itself recursively for every directory.

    :param name:            str, tool name
    :param working_dir:     str, directory to start with.
    :param no_tool_check:   bool, only run in dirs that ran as a tool before
    :param is_base:         bool, **Do not touch! =)**
    """
    image_postfix = ''

    css_block = """
    body {
      font-family: 'Lucida Grande', 'Helvetica Neue', Helvetica, sans-serif;
      font-size: 9pt;
      background: #fff;
      margin: 8px;
    }
    h2 {
      margin-top:35px;
      margin-bottom:10px;
    }
    a {
      color: #555;
    }
    p {
      margin-top: 3px;
    }
    table {
      border: 0px;
    }
    td {
      padding: 0px;
    }
    div.msg {
      position: fixed;
      margin-left: -8px;
      bottom: 0px;
      width: 100%;
      z-index: 100;
    }
    div.msg pre {
      margin: 0px;
      bottom: 0px;
      padding: 4px;
      background: #cfa;
      color: #333;
    }
    div.msg pre.warn {
        background: #fb4;
    }
    div.msg pre.err {
        background: #f22;
    }
    form {
      margin-top: 5px;
      margin-bottom:12px;
    }
    ul {
      text-align: left;
      display: inline;
      margin: 0;
      padding: 2px 2px 2px 0;
      list-style: none;
    }
    ul li {
      background: #fff;
      color: #888;
      font: 12px/18px sans-serif;
      display: inline-block;
      margin-right: 0px;
      position: relative;
      padding: 0px 2px;
      cursor: pointer;
      -webkit-transition: all 0.2s;
      -moz-transition: all 0.2s;
      -ms-transition: all 0.2s;
      -o-transition: all 0.2s;
      transition: all 0.2s;
    }
    ul li:hover {
      background: #555;
      color: #fff;
    }
    ul li ul {
      padding: 0;
      position: absolute;
      top: 18px;
      left: 0;
      -webkit-box-shadow: none;
      -moz-box-shadow: none;
      box-shadow: none;
      display: none;
      opacity: 0;
      visibility: hidden;
      -webkit-transiton: opacity 0.2s;
      -moz-transition: opacity 0.2s;
      -ms-transition: opacity 0.2s;
      -o-transition: opacity 0.2s;
      -transition: opacity 0.2s;
      -webkit-box-shadow: 0 0 7px rgba(0, 0, 0, 0.35);
      -moz-box-shadow: 0 0 7px rgba(0, 0, 0, 0.35);
      box-shadow: 0 0 7px rgba(0, 0, 0, 0.35);
      z-index: 10;
    }
    ul li ul li {
      background: #fafafa;
      display: block;
    }
    ul li ul li:hover {
      background: #555;
    }
    ul li ul li:hover a {
      color: #fff;
    }
    ul li:hover ul {
      display: block;
      opacity: 1;
      visibility: visible;
    }
    div.img {
      background: #fff;
      margin-top: 25px;
      margin-bottom: 45px;
    }
    div.img a {
      color: #888;
      font: 12px/18px sans-serif;
    }
    div.img img {
      margin: 0px;
      margin-right: 7px;
      -webkit-box-shadow: 0 0 7px rgba(0, 0, 0, 0.15);
      -moz-box-shadow: 0 0 7px rgba(0, 0, 0, 0.15);
      box-shadow: 0 0 7px rgba(0, 0, 0, 0.15);
    }
    """

    javascript_block = """
    function ToggleDiv(d) {
      if(document.getElementById(d).style.display == "none") {
        document.getElementById(d).style.display = "block";
      } else {
        document.getElementById(d).style.display = "none";
      }
    }
    """

    rootjs_cont = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN">
    <html lang="en">
       <head>
          <meta http-equiv="X-UA-Compatible" content="IE=Edge">
          <title>Read a ROOT file</title>
          <link rel="shortcut icon" href="img/RootIcon.ico">
          <script
            type="text/javascript"
            src="https://root.cern.ch/js/latest/scripts/JSRootCore.js?gui&mathjax">
          </script>
       </head>
       <body>
          <div id="simpleGUI" path="" files="">
             loading scripts ...
          </div>
       </body>
    </html>
    """
    rootjs_dir_level = 0  # number of directories above base wd

    def __init__(self, name=None, working_dir='', no_tool_check=False,
                 is_base=True, cross_link_images=None, use_jsroot=True):
        super(WebCreator, self).__init__(name)
        self.working_dir = working_dir
        self.web_lines = []
        self.subfolders = []
        self.image_names = []
        self.plain_info = []
        self.plain_tex = []
        self.html_files = []
        self.no_tool_check = no_tool_check
        self.is_base = is_base
        self.webcreate_request = False
        self.cross_link_images = cross_link_images
        self.use_jsroot = use_jsroot

        if self.name == 'WebCreator':
            self.name = 'VarialWebCreator'

        # structure of self.cross_link_images
        # { pathlen: {
        #         'path/one': {'imagename1', 'imagename2'},
        #         'path/two': {'imagename1', 'imagename2'},
        #     }
        # }

    def base_configure(self):
        self.cross_link_images = {}

        # get image format
        for pf in ['.png', '.jpg', '.jpeg']:
            if pf in settings.rootfile_postfixes:
                self.__class__.image_postfix = pf
                break
        if not self.image_postfix:
            self.message('ERROR No image formats for web available!')
            self.message('ERROR settings.rootfile_postfixes:'
                         + str(settings.rootfile_postfixes))
            self.message('ERROR html production aborted')
            raise RuntimeError('No image postfixes')

        # get base directory
        if not self.working_dir:
            if self.cwd:
                self.working_dir = os.path.join(*self.cwd.split('/')[:-2])
            else:
                self.working_dir = os.path.normpath(analysis.cwd)

        # write rootjs file
        self.__class__.rootjs_dir_level = self.working_dir.count('/')
        with open(os.path.join(self.working_dir, 'rootjs.html'), 'w') as f:
            f.write(self.rootjs_cont)

    def configure(self):
        if self.is_base:
            self.base_configure()

        if os.path.exists(os.path.join(self.working_dir, 'webcreate_denial')):
            return

        if os.path.exists(os.path.join(self.working_dir, 'webcreate_request')):
            self.webcreate_request = True

        # collect folders and images
        for _, dirs, files in os.walk(self.working_dir):
            self.subfolders += list(  # check that tools have worked there..
                d for d in dirs
                if (self.no_tool_check
                    or analysis.lookup_path(os.path.join(self.working_dir, d)))
            )

            # tex files
            res, files = util.project_items(lambda f: f.endswith('.tex'), files)
            self.plain_tex += res

            # websites
            res, files = util.project_items(
                lambda f: (
                    (f.endswith('.html') or f.endswith('.htm'))
                    and f not in ('index.html', 'rootjs.html')
                ),
                files,
            )
            self.html_files += res

            # plain info
            pf = self.image_postfix
            info, files = util.project_items(
                lambda f: f.endswith('.info'), files)
            res, img_info = util.project_items(
                lambda f: f[:-5] + pf not in files, info)
            self.plain_info += res

            # images
            imgs, files = util.project_items(lambda f: f.endswith(pf), files)
            imgs = list(f[:-len(pf)] for f in imgs)  # remove postfixes
            self.image_names += imgs

            break

    def go4subdirs(self):
        for sf in self.subfolders[:]:
            path = os.path.join(self.working_dir, sf)
            inst = self.__class__(
                self.name, path, self.no_tool_check, False,
                cross_link_images=self.cross_link_images
            )
            inst.run()
            if not os.path.exists(os.path.join(path, 'index.html')):
                self.subfolders.remove(sf)

    def make_html_head(self):
        self.web_lines += [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            '<title>',
            self.name + ': ' + self.working_dir,
            '</title>',
            '<style type="text/css">',
            self.css_block,
            '</style>',
            '<script type="text/javascript" language="JavaScript"><!--',
            '<!-- javascript -->',
            self.javascript_block,
            '//--></script>',
            '<META name="robots" content="NOINDEX, NOFOLLOW" />',
            '</head>',
            '<body>',
            '',
        ]

    def make_headline(self):
        breadcrumb = list(d1 for d1 in self.working_dir.split('/') if d1)
        n_folders = len(breadcrumb) - 1
        self.web_lines += (
            '<!-- MESSAGE -->',
            '<!-- headline -->',
            '<h1>' + self.name + '</h1>',
            '<h2>Section</h2>',
            'location: ',
            '/'.join('<a href="%sindex.html">%s</a>' % ('../'*(n_folders-i), d)
            for i, d in enumerate(breadcrumb)),
            '<!-- SECTION CREATE FORM -->',
            '<!-- SECTION UPDATE FORM -->',
            '',
        )

    def make_subfolder_links(self):
        if not self.subfolders:
            return
        self.web_lines += (
            '<!-- subdirectories -->',
            '<br />subdirectories: <br />',
        )
        for sf in sorted(self.subfolders):
            self.web_lines += (
                '<a href="%s">%s</a><br />' % (
                    os.path.join(sf, 'index.html'), sf),
            )
        self.web_lines += ('',)

    def make_html_file_links(self):
        if not self.html_files:
            return
        self.web_lines += (
            '<!-- html file links -->',
            '<h2>HTML files</h2>',
        )
        for hf in self.html_files:
            self.web_lines += (
                '<p><a href="%s">%s</a></p>' % (hf, hf),
            )
        self.web_lines += ('',)

    def make_info_file_divs(self):
        if not self.plain_info:
            return
        self.web_lines += (
            '<!-- info files -->',
            '<h2>Info files</h2>',
        )
        for nfo in self.plain_info:
            p_nfo = os.path.join(self.working_dir, nfo)
            try:
                wrp = diskio.read(p_nfo)
                self.web_lines += (
                    '<div>',
                    '<p>',
                    '<b>' + nfo + '</b>',
                    '<p>',
                    '<pre>',
                    str(wrp),
                    '</pre>',
                    '</div>',
                )
            except (SyntaxError, ValueError, IOError):
                self.message('WARNING Could not read info file at %s' % p_nfo)
                etype, evalue, _ = sys.exc_info()
                traceback.print_exception(etype, evalue, None)
        self.web_lines += ('',)

    def make_tex_file_divs(self):
        if not self.plain_tex:
            return
        self.web_lines += (
            '<!-- tex files -->',
            '<h2>Tex files</h2>',
        )
        for tex in self.plain_tex:
            with open(os.path.join(self.working_dir, tex), 'r') as f:
                self.web_lines += (
                    '<div>',
                    '<p>',
                    '<b>' + tex + '</b>',
                    '<p>',
                    '<pre>',
                )
                self.web_lines += f.readlines()
                self.web_lines += (
                    '</pre>',
                    '</div>',
                )
        self.web_lines += ('',)

    def make_image_divs(self):
        if not self.image_names:
            self.web_lines += ('<!-- NO IMAGES -->', )
            return

        # lin/log pairs
        image_names = sorted(self.image_names)
        image_name_tuples = []
        for i in xrange(len(image_names)):
            try:
                a, b = image_names[i], image_names[i+1]
            except IndexError:
                a, b = image_names[i], ''
            if (a.endswith('_log')
                and image_name_tuples
                and image_name_tuples[-1][1] == a
            ):
                continue
            elif (a.endswith('_lin')
                  and b.endswith('_log')
                  and a[:-4] == b[:-4]
            ):
                image_name_tuples.append((a, b))
            else:
                image_name_tuples.append((a, None))

        # toc
        self.web_lines += (
            '<!-- image files -->',
            '<a name="toc"></a>',
            '<h2>Figures</h2>',
            '<div><table>',
        ) + tuple(
            '<tr><td><a href="#%s">%s%s</a></td></tr>' % (
                (img[:-4], img, ' (+ log)')
                if img_log else
                (img, img, '')
            )
            for img, img_log in image_name_tuples
        ) + (
            '</table></div>',
            '<!-- HISTO CREATE FORM -->',
            '',
        )

        # build rootjs base link (without item yet)
        rootjs_base_link = '../' * (self.working_dir.count('/')
                                    - self.rootjs_dir_level)
        rootjs_base_link += 'rootjs.html?file='
        rootjs_base_link += os.path.normpath(
            ('../' * self.rootjs_dir_level) +
            os.path.join(self.working_dir, sparseio._rootfile)
        )

        # images
        crosslink_set = set()
        sparse_dict = sparseio.bulk_read_info_dict(self.working_dir)
        for img_lin, img_log in image_name_tuples:

            if img_lin.endswith('_lin'):
                img = img_lin[:-4]
            else:
                img = img_lin
                img_lin = ''

            # try to get from sparseio
            wrp = sparse_dict.get(img)

            # else look for info file on disk
            img_path = os.path.join(self.working_dir, img_lin or img)
            if (not wrp) and os.path.exists(img_path + '.info'):
                with open(img_path + '.info') as f:
                    wrp = wrappers.Wrapper(**diskio._read_wrapper_info(f))

            # else create a dummy wrapper
            if not wrp:
                wrp = wrappers.Wrapper(name=img, history='no history available')

            if settings.no_toggles:
                toggles = ('<!-- TOGGLES -->',)
                toggled_divs = ('<!-- TOGGLE_DIVS -->',)
            else:
                i_id = 'info_' + img
                h_id = 'history_' + img
                history_lines = str(wrp.history)
                info_lines = wrp.pretty_writeable_lines()
                toggles = (
                    '<!-- TOGGLES -->',
                    '<a href="javascript:ToggleDiv(\'' + h_id   # toggle history
                    + '\')">(toggle history)</a>',
                    '<a href="javascript:ToggleDiv(\'' + i_id   # toggle info
                    + '\')">(toggle info)</a>',
                )
                toggled_divs = (
                    '<!-- TOGGLE_DIVS -->',
                    '<div id="' + h_id                          # history div
                    + '" style="display:none;"><pre>',
                    history_lines,
                    '</pre></div>',
                    '<div id="' + i_id                          # info div
                    + '" style="display:none;"><pre>',
                    info_lines,
                    '</pre></div>',
                )
                if os.path.exists(img_path+'.png'):
                    toggles += (
                        '<a href="%s.png" target="new">(png)</a>' % img_lin or img,
                    )
                if os.path.exists(img_path+'.pdf'):
                    toggles += (
                        '<a href="%s.pdf" target="new">(pdf)</a>' % img_lin or img,
                    )

            rootjs_link = rootjs_base_link + '&item={0}/{0}'.format(wrp.name)

            self.web_lines += (
                '<!-- IMAGE:%s: -->' % img,
                '<div class="img">',
                ('<a name="%s"></a>' % img),                    # anchor
                '<!-- CROSSLINK MENU:%s: -->' % img,
                '<p>',                                          # image headline
                ('<b>%s%s</b><br />' % (img, '_lin (+ _log)'
                                             if img_log else '')),
            ) + toggles + (
                '<a href="%s" target="new">(open in rootjs)</a>' % rootjs_link,
                '<a href="#toc">(back to top)</a>',
                '</p>',
            ) + toggled_divs + (
                ('<img src="%s" />' %                          # the images
                    ((img_lin or img) + self.image_postfix)),
                ('<img src="%s" />' %
                    (img_log + self.image_postfix)) if img_log else '',
                '<!-- SELECTION FORM -->',
                '</div>',
                '',
            )
            crosslink_set.add(img)

        # store structured information for cross link menu
        if crosslink_set:
            path = os.path.normpath(self.working_dir)
            path_depth = path.count('/')
            if not path_depth in self.cross_link_images:
                self.cross_link_images[path_depth] = {}
            self.cross_link_images[path_depth][path] = crosslink_set

    def finalize_page(self):
        self.web_lines += [
            '<p style="margin-top:50px; margin-bottom:600px;">Created on '
            + datetime.datetime.now().strftime('%Y-%m-%d %H:%M') +
            ' with '
            '<a href="https://github.com/HeinerTholen/Varial" target="new">'
            'varial_webcreator'
            '</a>.'
            '</p>',
            '</body>',
            '</html>',
        ]

    def write_page(self):
        for i, l in enumerate(self.web_lines):
            self.web_lines[i] += '\n'
        with open(os.path.join(self.working_dir, 'index.html'), 'w') as f:
            f.writelines(self.web_lines)

    def make_cross_link_menus(self):
        def n_path_elements_different(p1, p2):
            return sum(not a == b for a, b in itertools.izip(p1, p2))

        def path_different_at_index(p1, p2):
            return sum(itertools.takewhile(
                int,
                (a == b for a, b in itertools.izip(p1, p2))
            ))

        def rel_path(other_path, nth_elem, img):
            rel_path = '../' * (len(other_path) - nth_elem)
            rel_path += '/'.join(other_path[nth_elem:])
            rel_path += '/index.html#' + img
            return rel_path

        def find_paths_for_image(img, path, paths_with_same_len):
            p = path.split('/')                 # 1st items are current path
            menu_items = list([elem] for elem in p)
            for other_path, other_img_set in paths_with_same_len.iteritems():
                if path == other_path:
                    continue
                if img not in other_img_set:
                    continue
                op = other_path.split('/')
                if n_path_elements_different(p, op) != 1:
                    continue

                index = path_different_at_index(p, op)
                menu_items[index].append(
                    '<a href="%s">%s</a>'%(rel_path(op, index, img), op[index])
                )
            return menu_items

        def convert_to_web_line(menu_items):
            def sort_key(l):
                # pull out my_plot from either 'my_plot' or '<a href="#my_plot">my_plot</a>''
                return l.replace('</a>', '').replace('</font>', '').split('>')[-1]

            def make_submenu(link_list):
                res = '<li>' + link_list[0]
                if len(link_list) > 1:
                    res += '<ul>'
                    for lnk in sorted(
                        ['<font color="000">'+link_list[0]+'</font>'] + link_list[1:],
                        key=sort_key
                    ):
                        res += '<li>%s</li>' % lnk
                    res += '</ul>'
                res += '</li>'
                return res

            line = '<div class="crosslinks"><ul>' + '<li>/</li>'.join(
                make_submenu(link_list) for link_list in menu_items
            ) + '</ul></div>\n'
            return line

        def write_code_for_page(path, image_menus_items):
            with open(path + '/index.html') as f:
                web_lines = f.readlines()

            for line_no, line in enumerate(web_lines):
                if line.startswith('<!-- CROSSLINK MENU:'):
                    img = line.split(':')[1]
                    web_lines[line_no] = convert_to_web_line(
                                            image_menus_items[img])

            with open(path + '/index.html', 'w') as f:
                f.writelines(web_lines)

        for paths_with_same_len in self.cross_link_images.itervalues():
            for path, img_set in paths_with_same_len.iteritems():
                img_menu_items = {}
                for img in img_set:
                    res = find_paths_for_image(img, path, paths_with_same_len)
                    res.append([img] + list(
                        '<a href="#%s">%s</a>' % (img_, img_)
                        for img_ in img_set
                        if img_ != img
                    ))
                    img_menu_items[img] = res
                write_code_for_page(path, img_menu_items)

    def run_procedure(self):
        self.configure()
        self.go4subdirs()

        items_to_process = (
            self.subfolders,
            self.image_names,
            self.plain_info,
            self.plain_tex,
            self.html_files,
            self.webcreate_request
        )

        if any(items_to_process):
            self.message('INFO Building page in ' + self.working_dir)
            self.make_html_head()
            self.make_headline()
            self.make_subfolder_links()
            self.make_html_file_links()
            self.make_info_file_divs()
            self.make_tex_file_divs()
            self.make_image_divs()
            self.finalize_page()
            self.write_page()

    def run(self):
        if self.is_base:
            with util.Switch(diskio, 'use_analysis_cwd', False):
                with util.Switch(sparseio, 'use_analysis_cwd', False):
                    self.run_procedure()
                    self.message('INFO Making cross-link menus.')
                    self.make_cross_link_menus()
        else:
            self.run_procedure()


# TODO load info and history of images with ajax
