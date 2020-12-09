from platform import version
import lib.v2 as lib

import argparse
import os
import sys
import glob
import json


def run_for(args_role, args_dir, args_out, args_lang, args_config):
    assert args_role in ('server', 'client'), f'Unexpected role {args_role}, must be server or client'
    role = lib.generator.Role.SERVER if args_role == 'server' else lib.generator.Role.CLIENT

    versioning = lib.versioning.Versioning()
    lexer = lib.lexer.lg.build()
    parser = lib.parser.pg.build()
    messages = {}
    programs = {}
    queues = {}

    path = os.path.realpath(args_dir)
    files = sorted(glob.glob(os.path.join(path, '*.kumo')))
    for file in files:
        with open(file) as fp:
            print(f'Parsing file {file}')
            contents = fp.read()
            versioning.digest_file(contents)
            mainbox = parser.parse(lexer.lex(contents))
            for result in mainbox.eval():
                name = result.name.eval()
                
                if isinstance(result, lib.boxes.MessageBox):
                    if name in messages:
                        raise NotImplementedError(f'Message `{name}` already parsed')

                    messages[name] = result

                elif isinstance(result, lib.boxes.ProgramBox):
                    if name in programs:
                        raise NotImplementedError(f'Program `{name}` already parsed')

                    programs[name] = result

                elif isinstance(result, lib.boxes.QueueBox):
                    if name in queues:
                        raise NotImplementedError(f'Queue `{name}` already parsed')

                    queues[name] = result

    # Check that all queues are valid
    for name, queue in queues.items():
        lib.semantic.check_queue_base(name, queue)
        lib.semantic.check_queue_specifier(name, queue, messages, programs)

    # Check all messages are valid
    for name, message in messages.items():
        lib.semantic.check_message_types(name, message, messages)

    # And finally check programs
    for name, program in programs.items():
        lib.semantic.check_program_queue(name, program, queues)
        lib.semantic.check_program_message(name, program, messages)
        lib.semantic.check_program_arguments(name, program, messages, queues)

    # Read config if any
    config = {}
    if args_config:
        with open(args_config) as fp:
            config = json.load(fp)

    # Chose generator based on language selected
    try:
        LangModule = getattr(lib.lang, args_lang.replace('-', '_'))
        generator = LangModule.LangGenerator(config, role, queues, messages, programs)
    except:
        raise NotImplementedError(f'Language {args_lang} is not yet supported')

    generator.generate(versioning.generate())
    generator.dump(args_out)

def main():
    parser = argparse.ArgumentParser(description='Generates network marshalling code.')
    parser.add_argument('--role', help='Either server or client', required=True, action='append')
    parser.add_argument('--dir', help='folder containing .kumo files', required=True, action='append')
    parser.add_argument('--out', help='folder to output files', required=True, action='append')
    parser.add_argument('--lang', help='Generator language', required=True, action='append')
    parser.add_argument('--config', help='Path with options to the generator language', default=None, action='append')
    args = parser.parse_args()

    assert len(args.role) == len(args.dir) == len(args.out) == len(args.lang) == len(args.config), "All arguments must be provided the same amount of times"
    
    for args_role, args_dir, args_out, args_lang, args_config in zip(args.role, args.dir, args.out, args.lang, args.config):
        run_for(args_role, args_dir, args_out, args_lang, args_config)


if __name__ == '__main__':
    main()
