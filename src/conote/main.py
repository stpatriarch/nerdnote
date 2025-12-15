#!/usr/bin/env python3


from conote.modules import NoteCommandController
import click

control = NoteCommandController()

@click.group()
def main() -> None:
    pass

@main.command(help='Create or add note. | Կստեղծի կամ կավելցնի նշում:')
@click.argument('notes', nargs=-1)
def add(notes: str) -> None:
    note = ' '.join(notes)
    control.add(note)


@main.command(help='Show all notes and ids. | Կցուցադրի բոլոր գրացնումները:')
def ls() -> None:
    control.ls()



@main.command(help='Remove existing note file and record. | Կջնջի առկա նշում-ֆայլը և գրանցումը:')
@click.argument('note_id', type=int)
def rm(note_id: int) -> None:
    control.rm(note_id)


@main.command(help='Show markdown file in terminal. | Կցուցադրի մարկդաուն ֆայլը տերմինալում:')
@click.argument('note_id', type=int)
def cat(note_id: int) -> None:
    control.cat(note_id)



@main.command(help='Export markdown in html or pdf format. | Մարկդաուն ֆայլը կվերափոխի html կամ pdf:')
@click.argument('note_id', type=int)
@click.argument('file_type', type=click.Choice(['pdf', 'html'], case_sensitive=False))
def export(note_id: int, file_type: str) -> None:
    control.export(note_id, pattern=file_type)
    

if __name__ == '__main__':
    main()
