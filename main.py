import argparse
import sys
import os
from interval_projector.interval_projector import IntervalProjector

def normalize_args(args, skip_list=[]):
    """Converts all relative path arguments to absolute ones relatively to the current working directory"""
    normalized_args = {}
    for key,value in args.__dict__.iteritems():
        if key not in skip_list:
            normalized_args[key] = value if not value or os.path.isabs(value) else os.path.normpath(os.path.join(os.getcwd(), value))
        else:
            normalized_args[key]=value
    return argparse.Namespace (**normalized_args)

def get_arg_parser():
    general_parser = argparse.ArgumentParser()
    general_parser.add_argument("-b", "--bed",    help="Input TAB-separated bedGraph file <chrom><start><end><value>",  required=True)
    general_parser.add_argument("-r", "--refmap", help="Input TAB-separated refmap file <chrom><pose><shift>",          required=True)
    general_parser.add_argument("-o", "--output", help="Output TAB-separated bedGraph file <chrom><start><end><value>", required=True)
    return general_parser

def main(argsl=None):
    if argsl is None:
        argsl = sys.argv[1:]
    args,_ = get_arg_parser().parse_known_args(argsl)
    args = normalize_args(args)
    interval_projector = IntervalProjector(args.refmap, args.bed, args.output)
    interval_projector.project()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))