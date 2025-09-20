 " This is the Vim syntax file for Blade.
" Author: Chen Feng <phongchen@tencent.com>

if version < 600
    syntax clear
elseif exists("b:current_syntax")
    finish
endif

" Read the python syntax to start with
if version < 600
    so <sfile>:p:h/python.vim
else
    runtime! syntax/python.vim
    unlet b:current_syntax
endif

syn case match

" Sorted by alphabet order, grouped by targets

" General functions
syn keyword bladeTarget blade build_target enable_if include load native

syn keyword bladeTarget glob
syn keyword bladeArg allow_empty exclude

" General args
syn keyword bladeArg name srcs deps tags visibility deprecated

" Test args
syn keyword bladeArg always_run exclusive testdata

" C/C++ targets

" C/C++ general args
syn keyword bladeArg always_optimize defs incs extra_cppflags extra_cuflags optimize warning

syn keyword bladeTarget cc_library prebuilt_cc_library
syn keyword bladeArg allow_undefined binary_link_only export_incs hdrs
syn keyword bladeArg link_all_symbols prebuilt secret secret_revision_file

syn keyword bladeTarget foreign_cc_library
syn keyword bladeArg libpath_pattern has_dynamic

syn keyword bladeTarget cc_binary
syn keyword bladeArg dynamic_link embed_version export_dynamic extra_linkflags

syn keyword bladeTarget cc_test
syn keyword bladeArg heap_check heap_check_debug

syn keyword bladeTarget cc_benchmark

syn keyword bladeTarget cc_plugin
syn keyword bladeArg prefix strip suffix linker_scripts version_scripts

syn keyword bladeTarget lex_yacc_library
syn keyword bladeTarget resource_library

syn keyword bladeTarget cu_binary cu_library cu_test

" Protobuf Targets
syn keyword bladeTarget proto_library
syn keyword bladeArg generate_descriptors plugins target_languages

" Thrift Targets
syn keyword bladeTarget thrift_library

syn keyword bladeTarget package
syn keyword bladeArg out

" This is the last rule
syn keyword bladeTarget gen_rule
syn keyword bladeArg cmd cmd_name cleans outs src_exts generate_hdrs generated_incs heavy

if version >= 508 || !exists("did_blade_syn_inits")
    if version < 508
        let did_blade_syn_inits = 1
        command! -nargs=+ HiLink hi link <args>
    else
        command! -nargs=+ HiLink hi def link <args>
    endif

    HiLink bladeTarget   Function
    HiLink bladeArg      Special
    delcommand HiLink
endif

let b:current_syntax = "blade"
