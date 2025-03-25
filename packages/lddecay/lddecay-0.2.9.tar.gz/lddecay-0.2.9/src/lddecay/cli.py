"""
Copyright 2025 Stéphane De Mita

This file is part of the lddecay

egglib-ld-decay is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

lddecay is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

A copy of the GNU General Public License should be found in the home
directory. If not, see <http://www.gnu.org/licenses/>.
"""

from .version import __version__
from matplotlib import pyplot
import click, egglib

@click.group(help=f"""
    EggLib-powered LD decay analyzer

    Version: {__version__}
""")
def main():
    pass

@main.command(no_args_is_help=True, help="""compute LD between pairs of sites""")
@click.option('-i', '--input', 'input_', required=True, type=click.Path(exists=True), help='input VCF/BCF')
@click.option('-o', '--output', required=True, type=click.Path(exists=False), help='output file')
@click.option('-m', '--maf', default=0, type=float, help='minimal minor allele frequency')
@click.option('-d', '--distance', default=100000, type=int, help='maximal pairwise distance (bp)')
@click.option('-n', '--missing', default=0, type=int, help='maximal number of missing data')
@click.option('-s', '--samples', default=None, type=click.Path(exists=True), help='file containing list of samples to include')
@click.option('-f', '--first', default=False, is_flag=True, help='consider only the first allele of genotypes')
@click.option('-x', '--skip', default=[], multiple=True, help='name of contig to skip (can be used several times)')
def compute(input_, output, maf, distance, missing, samples, first, skip):
    skip = dict.fromkeys(skip, False)

    vcf = egglib.io.VCF(input_)

    # process struct
    if samples is None:
        struct = None
    else:
        with open(samples) as f:
            select = f.read().split()
            samples = vcf.get_samples()
            struct = egglib.struct_from_dict(
                {None: {None: {name: [samples.index(name)] for name in select}}}, None)

    # initialize cache of sites (from the same chromosome)
    cache = []
    chrom = None
    n = 0
    np = 0
    cs = egglib.stats.ComputeStats(struct=struct)
    cs.add_stats('Aing', 'maf')
    if first:
        alph = egglib.alphabets.DNA
    else:
        alph = egglib.Alphabet('string', ['AA', 'AC', 'AG', 'AT', 'CC',
                                          'CG', 'CT', 'GG', 'GT', 'TT'],
                                         ['NN']) 
    # process sites
    with open(output, mode='wb') as f:
        while vcf.read():

            # skip chromosome if requested
            if vcf.get_chrom() in skip:
                if not skip[vcf.get_chrom()]: skip[vcf.get_chrom()] = True
                continue

            # import site from VCF
            if len(vcf.get_alleles()) < 2: continue
            site = vcf.as_site()
            stats = cs.process_site(site)
            if stats['Aing'] != 2 or stats['maf'] <  maf or site.num_missing > missing: continue

            # remove all sites if chromosome has changed
            if vcf.get_chrom() != chrom:
                cache.clear()
                chrom = vcf.get_chrom()
                print('current chrom:', chrom)

            # remove all sites that are before max_dist bp before current
            while len(cache) > 0 and site.position - cache[0].position - 0.1 > distance: # remove 0.1 to cope with rounding errors
                cache.pop(0)

            # compute pairwise LD
            for other in cache:
                rsq = egglib.stats.pairwise_LD(other, site, struct=struct)['rsq']
                if rsq is not None:
                    f.write(b'%(d)d %(rsq).4f\n' %{b'd': site.position-other.position, b'rsq': rsq})
                np += 1

            cache.append(site)
            n += 1
    print('number of sites:', n)
    print('number of pairs:', np)

    for ctg, flag in skip.items():
        if not flag:
            print(f'warning: {ctg} not found in VCF')


@main.command(no_args_is_help=True, help="""generate graphical representation of LD decay""")
@click.option('-i', '--input', 'input_', required=True, type=click.Path(exists=True), help='input LD data')
@click.option('-o', '--output', required=True, type=click.Path(exists=False), help='output file name')
@click.option('-b', '--bounds', required=True, type=str, help='list of distance bounds, separated by commas')
@click.option('-p', '--points', default=False, is_flag=True, help='draw individuals points in addition to curves')
def plot(input_, output, bounds, points):
    wins = [[] for _ in bounds]
    bounds = list(map(int, bounds.split(',')))
    if points:
        array_d = []
        array_rsq = []
    with open(input_, 'rb') as f:
        for line in f:
            d, rsq = line.split()
            d = int(d)
            rsq = float(rsq)
            for b, win in zip(bounds, wins):
                if d <= b:
                    win.append(rsq)
                    break
            if points:
                array_d.append(d)
                array_rsq.append(rsq)
    cur=0
    X = []
    Y = []
    Z = []
    Q1 = []
    Q2 = []
    Q3 = []
    Q4 = []
    for b, win in zip(bounds, wins):
        mid = (b+cur)/2
        cur = b
        win.sort()
        num = len(win)
        if num > 1:
            med = win[int(num/2)]
            q025 = win[int(0.025*num)]
            q25 = win[int(0.25*num)]
            q75 = win[int(0.75*num)]
            q975 = win[int(0.975*num)]
            med = win[int(num/2)]
            avg = sum(win)/num
            print(f'lim={b} mid={mid} num={num} med={med} avg={avg}')
            X.append(mid)
            Y.append(med)
            Z.append(avg)
            Q1.append(q25)
            Q2.append(q75)
            Q3.append(q025)
            Q4.append(q975)
    if points:
        pyplot.plot(array_d, array_rsq, 'k.', alpha=0.25)
    pyplot.plot(X, Y, 'b-', label='median')
    pyplot.plot(X, Z, 'r-', label='mean')
    pyplot.fill_between(X, Q1, Q2, color='b', alpha=0.2, label='50%')
    pyplot.fill_between(X, Q3, Q4, color='b', alpha=0.1, label='95%')
    pyplot.xlabel('Window midpoint')
    pyplot.ylabel(r'$r^2$')
    pyplot.legend()
    pyplot.ylim(0, 1.01)
    pyplot.savefig(output)
    pyplot.clf()

if __name__ == '__main__':
    main()
