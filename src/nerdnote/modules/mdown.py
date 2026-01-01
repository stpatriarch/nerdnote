#!/usr/bin/env python3

import os
from nerdnote.modules.tools import PATH, Deco
from mdutils import MdUtils
from mdutils.fileutils.fileutils import MarkDownFile
from markdown_pdf import MarkdownPdf, Section
import markdown

class MarkDownInit(MdUtils, MarkDownFile, Deco):
    """
    Manages Markdown documents, including creation and exprt to PDF and HTML formats. 

    This class provides high-level operations for working whith Markdown files,
    such as initializing new documents and exproting them to supported output formats.
    """

    def __init__(self) -> None:

        Deco.__init__(self)

        self.file_name = self.date_now_undercored
        self.note_path = os.path.join(PATH, self.file_name)
        self.note_path_with_ext = "".join([self.note_path, '.md',]) 

        super().__init__(file_name=self.note_path)


    
    def create_note(self, note: str) -> None:
        """
        This function recevies note sting, creates a markdown file
        if it does\'t exist; othervise, append to it.

        :param note: The note content entered by the user.
        :type note: str
        """

        if os.path.exists(self.note_path_with_ext):

            file_content = self.read_file(self.note_path)
        
            self.write(f"{self.time_now}", bold_italics_code='b')
            self.new_paragraph(f'{note}')

            with open(self.note_path_with_ext, 'w', encoding='utf-8') as f:
                f.write(file_content + self.get_md_text())
        
            
        else: 
            self.write(f'# {self.date_now}')
            self.write(' \n')
            self.write(f"{self.time_now}", bold_italics_code='b')
            self.new_paragraph(f'{note}')

            self.message_info.print('Your thoughts are wroten !')
            self.create_md_file()


    def exporter(self, path: str, raw_file: str, pattern: str) -> None:
        """
        The function export a mardown file following the specified pattern.
        Availbale patterns are PDF and HTML.
        
        :param path:
        :type path: str
        :param raw_file:
        :type raw_file: str
        :param pattern:
        :type pattern: str
        """
        
        if pattern in ('pdf',):
            pdf = MarkdownPdf()
            
            pdf.add_section(Section(raw_file, toc=True))
            pdf.save(f'{path}.pdf')

        else:
            html = markdown.markdown(raw_file)

            with open(f'{path}.html', 'w', encoding='utf-8') as file:
                file.write(html)

        return self.message_info.print(f'Thoughts has exported in {path}.{pattern}')    
