"""
Tools connected to the use of (La)Tex.
"""

import shutil
import os

from varial.toolinterface import Tool


class TexContent(Tool):
    """
    Copies (and converts) content for usage in a tex document.

    For blocks of images, includestatements are printed into .tex files.
    These can be include in the main tex document.

    Image files in eps format are converted to pdf.

    IMPORTANT: absolute paths must be used in ``images`` and ``plain_files``!

    :param images:      ``{'blockname.tex': ['path/to/file1.eps', ...]}``
    :param plain_files: ``{'target_filename.tex': 'path/to/file1.tex', ...}``
    :param include_str: e.g. ``r'\includegraphics[width=0.49\textwidth]
                        {TexContent/%s}'`` where %s will be formatted with the
                        basename of the image
    :param dest_dir:    destination directory (default: tool path)
    """
    def __init__(self,
                 images={},
                 plain_files={},
                 include_str='%s',
                 dest_dir=None,
                 dest_dir_name=None,
                 name=None):
        super(TexContent, self).__init__(name)
        self.images = images
        self.tex_files = plain_files
        self.include_str = include_str
        self.dest_dir = dest_dir
        self.dest_dir_name = dest_dir_name

    def _join(self, *args):
        return os.path.join(self.dest_dir, *args)

    @staticmethod
    def _hashified_filename(path):
        bname, _ = os.path.splitext(os.path.basename(path))
        hash_str = '_' + hex(hash(os.path.dirname(path)))[-7:]
        return bname + hash_str

    def initialize(self):
        if not self.dest_dir:
            self.dest_dir = self.cwd
        if not self.dest_dir_name:
            p_elems = self.dest_dir.split('/')
            self.dest_dir_name = p_elems[-1] or p_elems[-2]

    def copy_image_files(self):
        for blockname, blockfiles in self.images.iteritems():
            hashified_and_path = list(
                (self._hashified_filename(bf), bf) for bf in blockfiles
            )

            # make block file
            with open(self._join(blockname+'.tex'), 'w') as f:

                for hashified, path in hashified_and_path:

                    # prepare image
                    p, ext = os.path.splitext(path)
                    if ext == '.eps':
                        os.system('ps2pdf -dEPSCrop %s.eps %s.pdf' % (p, p))
                        ext = '.pdf'
                    elif not ext in ('.pdf', '.png'):
                        raise RuntimeError(
                            'Only .eps, .pdf and .png images are supported.')

                    # copy image file
                    img_dest = blockname + '_' + hashified.replace('.', '-')
                    shutil.copy(p+ext, self._join(img_dest+ext))

                    # write tex include
                    inc_dest = os.path.join(self.dest_dir_name, img_dest)
                    f.write(self.include_str % inc_dest + '\n')

    def copy_plain_files(self):
        for fname, path, in self.tex_files.iteritems():
            shutil.copy(path, self._join(fname))

    def run(self):
        self.initialize()
        self.copy_image_files()
        self.copy_plain_files()
