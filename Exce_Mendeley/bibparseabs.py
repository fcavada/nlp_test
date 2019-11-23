#!/usr/bin/env python3

import biblib.bib
import biblib.messages
import biblib.algo
import argparse
import sys
import re



def main():
    arg_parser = argparse.ArgumentParser(
        description='Parse .bib database(s) and print basic fields as text')
    arg_parser.add_argument('bib', nargs='+', help='.bib file(s) to process',
                            type=open)
    args = arg_parser.parse_args()

    try:
        # Load databases
        db = biblib.bib.Parser().parse(args.bib, log_fp=sys.stderr).get_entries()

        # Resolve cross-references
        db = biblib.bib.resolve_crossrefs(db)

        # Print entries
        recoverer = biblib.messages.InputErrorRecoverer()
        for ent in db.values():
            with recoverer:
                print_entry(ent)
        recoverer.reraise()
    except biblib.messages.InputError:
        sys.exit(1)

def print_entry(ent):
    # print('{ent.key} ({ent.typ}):'.format(ent=ent))
    # if 'title' in ent:
    #     print('  ' + biblib.algo.tex_to_unicode(biblib.algo.title_case(
    #         ent['title'], pos=ent.field_pos['title'])))

    # if 'author' in ent:
    #     authors = [
    #         biblib.algo.tex_to_unicode(author.pretty(),
    #                                    pos=ent.field_pos['author'])
    #         for author in ent.authors()]
    #     if len(authors) == 0:
    #         author = None
    #     elif len(authors) == 1:
    #         author = authors[0]
    #     else:
    #         author = ', '.join(authors[:-1])
    #         if len(authors) > 2:
    #             author += ','
    #         if ent.authors()[-1].is_others():
    #             author += ' et al.'
    #         else:
    #             author += ' and ' + authors[-1]
    #     if author:
    #         print('  By ' + author)

    # if 'year' in ent:
    #     if 'month' in ent:
    #         mnum = ent.month_num()
    #         print('  {} {}'.format(MONTHS[mnum - 1], ent['year']))
    #     else:
    #         print('  {}'.format(ent['year']))
    nw_treshold = 80
    if 'abstract' in ent:
        #print('  {}'.format(ent['abstract']))
        #print('id---')
        #print(ent.key)
        #remove tabs
        abstract= ent['abstract'].replace('\t','')
        #remove new lines
        abstract= abstract.replace('\n','')
        #remove return of car
        abstract= abstract.replace('\r','')
        #print('abstract---')
        #print(abstract)
        #remove special characters in Latex format i.e. within curly brackets
        abstract=re.sub('{.*}','',abstract)
        # '.*' means any quantity and any type
        words=abstract.split() 
        num_words=len(words)
        if num_words > nw_treshold:
        #print(ent.key,'\t',len(abstract),'\t',abstract)
        # comment previous line and activate below to only get key and num of characters to do a hystogram
            print(ent.key,'\t',abstract)

if __name__ == '__main__':
    main()
