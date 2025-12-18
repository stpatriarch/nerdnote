#!/usr/bin/env python3

import os
from nerdnote.modules.tools import PATH, stamps, messages
from mdutils import MdUtils
from mdutils.fileutils.fileutils import MarkDownFile
from markdown_pdf import MarkdownPdf, Section
import markdown


class MarkDownInit(MdUtils, MarkDownFile):

    def __init__(self, file_name:str=stamps.date_now_undercored) -> None:

        self.note_path = os.path.join(PATH, file_name)
        self.note_path_with_ext = "".join([self.note_path, '.md',]) 

        super().__init__(file_name=self.note_path)

    
    def create_note(self, note: str) -> None:

        if os.path.exists(self.note_path_with_ext):

            file_content = self.read_file(self.note_path)
        
            self.write(f"{stamps.time_now}", bold_italics_code='b')
            self.new_paragraph(f'{note}')

            with open(self.note_path_with_ext, 'w', encoding='utf-8') as f:
                f.write(file_content + self.get_md_text())
        
            
        else: 
            self.write(f'# {stamps.date_now}')
            self.write(' \n')
            self.write(f"{stamps.time_now}", bold_italics_code='b')
            self.new_paragraph(f'{note}')

            messages.info.print('Your thoughts are wroten !')
            self.create_md_file()


    def exporter(self, path: str, raw_file: str, pattern: str) -> None:
        
        if pattern in ('pdf',):
            pdf = MarkdownPdf()
            
            pdf.add_section(Section(raw_file, toc=True))
            pdf.save(f'{path}.pdf')

        else:
            html = markdown.markdown(raw_file)

            with open(f'{path}.html', 'w', encoding='utf-8') as file:
                file.write(html)

        return messages.info.print(f'Thoughts has exported in {path}.{pattern}')
    
if __name__ == '__main__':
    m = MarkDownInit()
    m.create_note('note')
