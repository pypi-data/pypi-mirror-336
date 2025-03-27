import json
import argparse

from fuzzy_sidc import get_preloaded_SIDCFuzzySearcher


parser = argparse.ArgumentParser()
parser.add_argument('--std', type=str, default='2525d', choices=['2525d', 'app6d'], help='Standard to use')
parser.add_argument('--threshold', type=int, default=70, help='threshold for rapidfuzz')
parser.add_argument('--defaults_set_a', type=str, default=None, help='default values for set A as JSON string')

parser.add_argument('-a', type=str, default='', help='Query to set A')
parser.add_argument('-b', type=str, default='', help='Query to set B')
parser.add_argument('-m1', type=str, default='', help='Query to set B, modifier 1')
parser.add_argument('-m2', type=str, default='', help='Query to set B, modifier 2')
parser.add_argument('--show', type=bool, default=False, action=argparse.BooleanOptionalAction, help='show its meaning of selected SIDC')

parser.add_argument('--svg', type=bool, default=False, action=argparse.BooleanOptionalAction, help='return SVG instead of SIDC')
parser.add_argument('--svg-size', type=int, default=35, help='SVG size')

parser.add_argument('-s', type=str, default='', help='Query to all sets, just show top n results')
parser.add_argument('-n', type=int, default=10, help='n for TOP n')

parser.add_argument('--sidc2svg', type=str, default='', help='Convert SIDC to SVG')
args = parser.parse_args()

# logic for arguments
if args.s and (args.a or args.b or args.m1 or args.m2 or args.svg):
    raise Exception('-s and -n do not mix with other options')
if (args.m1 or args.m2) and not args.b:
    raise Exception('-m1 and -m2 require -b option')


x = get_preloaded_SIDCFuzzySearcher(args.std)
# change threshold
x.score_cutoff = args.threshold

# change defaults
if args.defaults_set_a:
    x.defaults_set_a.update(json.loads(args.defaults_set_a))

# just search
if args.s:
    x.show_top_n(args.s, n=args.n)
# get SIDC
elif (args.a or args.b):
    sidc = x.get_sidc(query_a=args.a, query_b=args.b, mod1=args.m1, mod2=args.m2, show_results=args.show)
    # get SVG
    if args.svg:
        txt = x.get_svg(sidc, size=args.svg_size)
        print(txt)
    else:
        print(sidc)
elif args.sidc2svg:
    txt = x.get_svg(args.sidc2svg, size=args.svg_size)
    print(txt)
