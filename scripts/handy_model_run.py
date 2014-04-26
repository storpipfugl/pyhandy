#!/usr/bin/env python
import argparse
from pyhandy import handy


def main():
    """Run the HANDY model using comand line input
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('society', help='Society. One of {egalitarian, equitable, unequal}')
    parser.add_argument('type', help='Socity type. Supported types for socities are: egalitarian : {soft, oscillatory, cyclic, collapse}, equitable : {soft, oscillatory, cyclic, collapse, inverse}, unequal : {type-l, collapse, soft, oscillatory}')
    parser.add_argument('years', help='Years to run society model')
    args = parser.parse_args()
    society = handy.create_society(args.society, args.type)
    result = society.evolve(int(args.years))
    handy.plot_society(*result)


if __name__ == '__main__':
    main()
