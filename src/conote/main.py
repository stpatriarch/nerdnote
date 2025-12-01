#!/usr/bin/env python3


from conote.modules import NoteCommandController
import click

control = NoteCommandController()

@click.group()
def main():
    pass

@main.command(help='Create or add note | Կստեղծի կամ կավելցնի նշում')
@click.argument('notes', nargs=-1)
def add(notes):
    note = ' '.join(notes)
    control.add(note)
    click.echo('wroten !')


@main.command(help='Show all notes and ids | Կցուցադրի բոլոր գրացնումները')
def ls():
    control.ls()



@main.command(help='Remove existing note file and record | Կջնջի առկա նշում-ֆայլը և գրանցումը')
@click.argument('note_id', type=int)
def rm(note_id):
    control.rm(note_id)

    click.echo('remvoed !')


@main.command(help='Show markdown file in terminal | Կցուցադրի մարկդաուն ֆայլը տերմինալում')
@click.argument('note_id', type=int)
def cat(note_id):
    control.cat(note_id)



@main.command(help='Export markdown in html or pdf format | Մարկդաուն ֆայլը կվերափոխի html կամ pdf')
@click.argument('note_id', type=int)
def export(note_id):
    click.echo('exported !')
    
    pass

if __name__ == '__main__':
    main()
