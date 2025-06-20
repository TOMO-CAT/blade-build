# Copyright (c) 2011 Tencent Inc.
# All rights reserved.
#
# Author: Chong peng <michaelpeng@tencent.com>
# Date:   October 20, 2011


"""
This is the CmdOptions module which parses the users'
input and provides hint for users.
"""

from __future__ import absolute_import
from __future__ import print_function

import argparse

# 支持命令行自动补全
# @see https://pypi.org/project/argcomplete/
# pyright: reportMissingImports=false
try:
    import argcomplete
except ImportError:
    argcomplete = None

from blade import console
from blade import constants
from blade.toolchain import BuildArchitecture
from blade.toolchain import ToolChain

# The 'blade_version.py' is generated by the dist script, then it only exists in blade.zip
try:
    from blade.blade_version import VERSION
except ImportError:
    VERSION = '(developing, unversioned)'


class CommandLineParser(object):
    """Command Line Parser.

    Parses user's input and provides hint.
    blade {command} [options] targets

    """

    def __init__(self):
        """Init the class."""
        self._arg_parser = self._build_arg_parser()
        if argcomplete:
            argcomplete.autocomplete(self._arg_parser)

    def parse(self, argv):
        """Parse command line."""

        options, others = self._arg_parser.parse_known_args(argv)

        # If '--' in arguments, use all other arguments after it as run
        # arguments
        if '--' in others:
            pos = others.index('--')
            targets = others[:pos]
            options.args = others[pos + 1:]
        else:
            targets = others
            options.args = []

        for t in targets:
            if t.startswith('-'):
                console.fatal('Unrecognized option %s, use blade [action] '
                              '--help to get all the options' % t)

        command = options.command
        # Check the options with different sub command
        self._check_subcommand(command, options, targets)

        return command, options, targets

    def _check_subcommand(self, command, options, targets):
        """Check correctness of subcommand."""
        actions = {
            'build': self._check_build_command,
            'clean': self._check_clean_command,
            'dump': self._check_dump_command,
            'query': self._check_query_command,
            'run': self._check_run_command,
            'test': self._check_test_command,
        }
        actions[command](options, targets)

    def _check_run_targets(self, options, targets):
        """check that run command should have only one target."""
        if len(targets) != 1 or ':' not in targets[0] or targets[0].endswith('...'):
            console.fatal('Please specify a single target to run: '
                          'blade run //target_path:target_name (or '
                          'a_path:target_name)')

    def _check_test_options(self, options, targets):
        """check that test command options."""

    def _check_plat_and_profile_options(self, options, targets):
        """check platform and profile options."""
        compiler_arch = self._compiler_target_arch()
        arch = BuildArchitecture.get_canonical_architecture(compiler_arch)
        if arch is None:
            console.fatal('Unknown architecture: %s' % compiler_arch)

        m = options.m
        if not m:
            options.arch = arch
            options.bits = BuildArchitecture.get_architecture_bits(arch)
            assert options.bits
        else:
            options.bits = m
            options.arch = BuildArchitecture.get_model_architecture(arch, m)
            if options.arch is None:
                console.fatal('"-m%s" is not supported by the architecture %s' % (m, compiler_arch))

    def _check_clean_options(self, options, targets):
        """check the clean options."""
        self._check_plat_and_profile_options(options, targets)

    def _check_query_options(self, options, targets):
        """check query action options."""
        if not options.deps and not options.dependents:
            console.fatal('Please specify --deps, --dependents or both to query target')

    def _check_build_options(self, options, targets):
        """check the building options."""
        self._check_plat_and_profile_options(options, targets)

    def _check_build_command(self, options, targets):
        """check build options."""
        self._check_build_options(options, targets)

    def _check_dump_command(self, options, targets):
        """check build options."""
        self._check_build_options(options, targets)

    def _check_run_command(self, options, targets):
        """check run options and the run targets."""
        self._check_build_options(options, targets)
        self._check_run_targets(options, targets)

    def _check_test_command(self, options, targets):
        """check test optios."""
        self._check_build_options(options, targets)
        self._check_test_options(options, targets)

    def _check_clean_command(self, options, targets):
        """check clean options."""
        self._check_clean_options(options, targets)

    def _check_query_command(self, options, targets):
        """check query options."""
        self._check_plat_and_profile_options(options, targets)
        self._check_query_options(options, targets)

    def __add_plat_profile_arguments(self, parser):
        """Add plat and profile arguments."""
        parser.add_argument('-m',
                            dest='m',
                            choices=['32', '64'],
                            default='',
                            help=('Generate code for a 32-bit(-m32) or '
                                  '64-bit(-m64) environment, '
                                  'default is autodetect'))

        parser.add_argument('-p',
                            '--profile',
                            dest='profile',
                            choices=['debug', 'release'],
                            default='release',
                            help=('Build profile, default is release'))

        parser.add_argument('--debug-info-level',
                            dest='debug_info_level',
                            choices=['no', 'low', 'mid', 'high'],
                            help='Produces how much debug information')

        # DEPRECATED, see above
        parser.add_argument('--no-debug-info',
                            dest='debug_info_level',
                            action='store_const',
                            const='no',
                            help=argparse.SUPPRESS)

    def __add_generate_arguments(self, parser):
        """Add generate related arguments."""
        parser.add_argument(
            '--generate-dynamic', dest='generate_dynamic',
            action='store_true', default=False,
            help='Generate dynamic libraries')

        parser.add_argument(
            '--generate-package', dest='generate_package',
            action='store_true', default=False,
            help='Generate packages for package target')

        parser.add_argument(
            '--generate-java', dest='generate_java',
            action='store_true', default=False,
            help='Generate java files for proto_library, thrift_library and '
                 'swig_library')

        parser.add_argument(
            '--generate-php', dest='generate_php',
            action='store_true', default=False,
            help='Generate php files for proto_library and swig_library')

        parser.add_argument(
            '--generate-python', dest='generate_python',
            action='store_true', default=False,
            help='Generate python files for proto_library and thrift_library')

        parser.add_argument(
            '--generate-go', dest='generate_go',
            action='store_true', default=False,
            help='Generate go files for proto_library')

    def __add_build_actions_arguments(self, parser):
        """Add build related action arguments."""
        parser.add_argument(
            '--backend-builder', dest='backend_builder', choices=['ninja'],
            help='Specify the underlying backend builder (currently only support ninja)')

        # Add extra backend builder options arguments.
        parser.add_argument(
            '--backend-builder-options', dest='backend_builder_options', metavar='OPTIONS',
            help='Specifies extra backend builder options, for debug purpose')

        parser.add_argument(
            '-j', '--jobs', dest='build_jobs', type=int,
            help=(constants.HELP.build_jobs))

        parser.add_argument(
            '-k', '--keep-going', dest='keep_going',
            action='store_true', default=False,
            help='Continue as much as possible after an error')

        parser.add_argument(
            '--no-test', dest='no_test', action='store_true',
            default=False, help='Do not build the test targets')

        parser.add_argument(
            '-n', '--dry-run', dest='dry_run', action='store_true', default=False,
            help='Dry run (don\'t run commands but act like they succeeded)')

        parser.add_argument(
            '--show-builds-slower-than', dest='show_builds_slower_than', metavar='SECONDS', type=float,
            help='Show build commands which are slower than specified seconds')

    def __add_coverage_arguments(self, parser):
        """Add coverage arguments."""
        parser.add_argument(
            '--gprof', dest='gprof',
            action='store_true', default=False,
            help='Add build options to support GNU gprof')

        parser.add_argument(
            '--coverage', dest='coverage',
            action='store_true', default=False,
            help='Add build options to support coverage test')

        # DEPRECATED, please use --coverage
        parser.add_argument(
            '--gcov', dest='coverage',
            action='store_true', default=False,
            help=argparse.SUPPRESS)

    def __add_pgo_arguments(self, parser):
        """Add Profile-guided Optimization arguments."""
        parser.add_argument(
            '--profile-generate', dest='profile-generate', metavar='path',
            action='store', type=str, nargs='?', const='',
            help='Add build options to support profile-generate')

        parser.add_argument(
            '--profile-use', dest='profile-use', metavar='path',
            action='store', type=str, nargs='?', const='',
            help='Add build options to support profile-use')

    def _add_query_arguments(self, parser):
        """Add query arguments for parser."""
        self.__add_plat_profile_arguments(parser)
        parser.add_argument(
            '--deps', dest='deps',
            action='store_true', default=False,
            help='Show all targets that depended by the target being queried')
        parser.add_argument(
            '--dependents', dest='dependents',
            action='store_true', default=False,
            help='Show all targets that depends on the target being queried')
        parser.add_argument(
            '--path-to', dest='query_path_to', type=str, default='',
            help='The targets to be depended on, comma separated')
        parser.add_argument(
            '--output-file', dest='output_file', type=str,
            help='The name of file to output query results, default to stdout')
        parser.add_argument(
            '--output-format', dest='output_format', type=str,
            choices=('plain', 'tree', 'dot'), default='plain',
            help='Specify the format of query results')

    def _add_clean_arguments(self, parser):
        """Add clean arguments for parser."""
        self.__add_plat_profile_arguments(parser)
        self.__add_build_actions_arguments(parser)
        self.__add_generate_arguments(parser)

    def _add_test_arguments(self, parser):
        """Add test command arguments."""
        parser.add_argument(
            '--full-test', action='store_true',
            dest='full_test', default=False,
            help='Enable full test, default is incremental test')

        parser.add_argument(
            '-t', '--test-jobs', dest='test_jobs', type=int,
            help=(constants.HELP.test_jobs))

        parser.add_argument(
            '--show-details', action='store_true',
            dest='show_details', default=False,
            help='Shows the test result in detail and provides a file')

        parser.add_argument(
            '--show-tests-slower-than', type=float, metavar='SECONDS',
            dest='show_tests_slower_than',
            help='Show tests which are slower than specified seconds')

        parser.add_argument(
            '--no-build', action='store_true',
            dest='no_build', default=False,
            help='Run tests directly without build')

        parser.add_argument(
            '--exclude-tests', dest='exclude_tests', default='', metavar='TARGET_LIST',
            help='Exclude tests which matches this comma seperated target pattern list')

        parser.add_argument(
            '--run-unrepaired-tests', dest='run_unrepaired_tests', action='store_true',
            help=constants.HELP.run_unrepaired_tests)

    def _add_run_arguments(self, parser):
        """Add run command arguments."""

    def _add_build_arguments(self, *parsers):
        """Add building arguments for parsers."""
        for parser in parsers:
            self.__add_plat_profile_arguments(parser)
            self.__add_build_actions_arguments(parser)
            self.__add_generate_arguments(parser)
            self.__add_coverage_arguments(parser)
            self.__add_pgo_arguments(parser)

    def _add_common_arguments(self, *parsers):
        for parser in parsers:
            parser.add_argument(
                '--profiling', dest='profiling', action='store_true',
                help='Blade performance profiling, for blade developing')
            parser.add_argument(
                '--stop-after', dest='stop_after', type=str,
                choices=['load', 'analyze', 'generate', 'build', 'all'], default='all',
                help='Stop after specified phase')
            parser.add_argument(
                '--color', dest='color', choices=['yes', 'no', 'auto'], default='auto',
                help='Output color mode selection')
            parser.add_argument(
                '--load-local-config', dest='load_local_config',
                default=True, action='store_true',
                help='Load BLADE_ROOT.local')
            parser.add_argument(
                '--no-load-local-config', dest='load_local_config',
                action='store_false',
                help='Do not load BLADE_ROOT.local')
            parser.add_argument(
                '--verbose', dest='verbosity', action='store_const', const='verbose',
                default='normal', help='Show all details')
            parser.add_argument(
                '--quiet', dest='verbosity', action='store_const', const='quiet',
                help='Only show warnings and errors')
            parser.add_argument(
                '--exclude-targets', dest='exclude_targets', type=str, default='',
                help='Comma separated target patterns to be excluded from loading')
            parser.add_argument(
                '--jar-compression-level', dest='jar_compression_level', type=str, choices=['', '0'],
                help=constants.HELP.jar_compression_level)
            parser.add_argument(
                '--fat-jar-compression-level', dest='fat_jar_compression_level', type=str,
                choices=([''] + [str(i) for i in range(9)]),
                help=constants.HELP.fat_jar_compression_level)
            parser.add_argument(
                '--tags-filter', dest='tags_filter', type=str,
                help='Tags filter expression, see documents for details')

    def _add_dump_arguments(self, parser):
        """Add dump arguments for parser."""
        parser.add_argument(
            '--to-file', dest='dump_to_file', action='store', metavar='FILEPATH',
            default='/dev/stdout',
            help='Specifies the path of file to write the dump result')
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '--compdb', dest='dump_compdb', default=False, action='store_true',
            help='Dump compilation database')
        group.add_argument(
            '--config', dest='dump_config', default=False, action='store_true',
            help='Dump blade configuration')
        group.add_argument(
            '--targets', dest='dump_targets', default=False, action='store_true',
            help='Dump attributes of targets in json format')
        group.add_argument(
            '--all-tags', dest='dump_all_tags', default=False, action='store_true',
            help='Dump all tags of targets in json format')

    def _build_arg_parser(self):
        """Add command options, add options within this method."""
        blade_cmd_help = 'blade <subcommand> [options...] [targets...]'
        arg_parser = argparse.ArgumentParser(prog='blade', description=blade_cmd_help)
        arg_parser.add_argument('--version', action='version', version='%(prog)s ' + VERSION)
        sub_parser = arg_parser.add_subparsers(dest='command', help='Available subcommands')

        sub_parser.required = True

        # subcommands
        build_parser = sub_parser.add_parser(
            'build',
            help='Build specified targets')

        run_parser = sub_parser.add_parser(
            'run',
            help='Build and runs a single target',
            epilog='Any arguments after the empty "--" will be passed to the program')

        test_parser = sub_parser.add_parser(
            'test',
            help='Build the specified targets and runs tests',
            epilog='Any arguments after the empty "--" will be passed to the program')

        clean_parser = sub_parser.add_parser(
            'clean',
            help='Remove all blade-created output')

        query_parser = sub_parser.add_parser(
            'query',
            help='Execute a dependency graph query')

        dump_parser = sub_parser.add_parser(
            'dump',
            help='Dump specified internal information')

        # add subcommand's common args
        self._add_common_arguments(build_parser, run_parser, test_parser,
                                   clean_parser, query_parser, dump_parser)
        # add subcommand's specific args
        self._add_build_arguments(build_parser, run_parser, test_parser, dump_parser)
        self._add_run_arguments(run_parser)
        self._add_test_arguments(test_parser)
        self._add_clean_arguments(clean_parser)
        self._add_query_arguments(query_parser)
        self._add_dump_arguments(dump_parser)

        return arg_parser

    def _compiler_target_arch(self):
        """Compiler(gcc) target architecture."""
        arch = ToolChain.get_cc_target_arch()
        pos = arch.find('-')
        if pos == -1:
            console.fatal('Unknown target architecture %s from gcc.' % arch)
        return arch[:pos]


def parse(argv):
    """Parse argv into command, options and targets"""
    parser = CommandLineParser()
    return parser.parse(argv)
