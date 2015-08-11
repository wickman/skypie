from __future__ import absolute_import, print_function

from collections import defaultdict
import argparse
import sys

from skypie.acquisition import AllCash, Mortgage
from skypie.colorant import breakeven
from skypie.constants import CONSTANTS
from skypie.common import Engine, Prop
from skypie.model import simple, UsageModel
from skypie.planes import PLANES
from skypie.tabulator import table


def setup_argparser():
  parser = argparse.ArgumentParser()
  setup_argparser_usagemodel(parser)
  setup_argparser_acquisition(parser)
  setup_argparser_depreciation(parser)
  setup_argparser_plane_option_overrides(parser)
  setup_argparser_constants_option(parser)

  subcommand_parser = parser.add_subparsers(help='subcommand help')

  setup_argparser_table_command(subcommand_parser)
  setup_argparser_sample_command(subcommand_parser)
  setup_argparser_constants_command(subcommand_parser)

  return parser


def table_command(args):
  plane = PLANES[args.plane]
  h_range = parse_range(args.h_range)
  y_range = parse_range(args.y_range)
  acquisition = parse_acquisition(args)
  usage_model = parse_usage_model(args)
  constants = parse_constants(args)

  def model(plane, acquisition, hours, years):
    outlay = simple(
        plane,
        acquisition,
        hours,
        years,
        usage=usage_model,
        constants=constants,
        sell=args.sell)

    if args.output == 'outlay':
      return outlay
    elif args.output == 'hourly':
      return outlay / hours if hours > 0 else 0
    elif args.output == 'yearly':
      return outlay / years if years > 0 else 0
    else:
      raise ValueError('Unknown outlay type %s' % args.output)

  plane = update_plane(plane, args)

  colorant = None
  if args.breakeven:
    colorant = breakeven(args.breakeven)

  print('Sell or keep: %s' % ('sell' if args.sell else 'keep'))
  table(
      plane,
      acquisition,
      model,
      h_range=h_range,
      y_range=y_range,
      colorant=colorant,
      yearly=args.range_type == 'yearly',
  )
  print('\n')


def setup_argparser_sample_command(parser):
  # args:
  #    plane [h_value or h_range] [y_value or y_range]
  #    da40 2000 0,180,24
  table_parser = parser.add_parser('sample', help='Provide tabular representation of a model.')
  table_parser.set_defaults(func=sample_command)
  table_parser.add_argument('plane', choices=PLANES)
  table_parser.add_argument('hours', type=int, help='Hours per year of flight.')
  table_parser.add_argument('years', type=int, help='Years of ownership.')


def sample_command(args):
  plane = PLANES[args.plane]
  hours = args.hours
  years = args.years
  acquisition = parse_acquisition(args)
  usage_model = parse_usage_model(args)
  constants = parse_constants(args)

  plane = update_plane(plane, args)

  hours = hours * years

  balance = simple(
      plane,
      acquisition,
      hours,
      years,
      usage=usage_model,
      constants=constants)

  #for month in range(years * 12):
  #  print('month %d: %s' % (month, ' '.join(map(str, balance.at_month(month)))))

  for year in range(years):
    print('year %d: %s' % (year, ' '.join(map(str, balance.at_year(year)))))
    print('  -> profit: %.2f, income: %.2f' % balance.aggregate_year(
        year, 1 - usage_model.personal_rate))


def setup_argparser_table_command(parser):
  # args:
  #    plane [h_value or h_range] [y_value or y_range]
  #    da40 2000 0,180,24
  table_parser = parser.add_parser('table', help='Provide tabular representation of a model.')
  table_parser.set_defaults(func=table_command)
  table_parser.add_argument('plane', choices=PLANES)
  table_parser.add_argument('h_range', help='Hours of flight, or range.')
  table_parser.add_argument('y_range', help='Years of ownership, or range.')
  table_parser.add_argument('--debug', action='store_true')
  table_parser.add_argument('--output', choices=['hourly', 'yearly', 'outlay'], default='hourly')
  table_parser.add_argument('--range-type', choices=['yearly', 'total'], default='yearly',
    help='If --range-type=yearly, interpret the hour value as hours per year. If '
         '--range-type=total, interpret the hour value as total hours.')
  table_parser.add_argument('--breakeven', type=float, default=None,
    help='The cost breakeven point.  Colorizes the table based on this value if specified.')


def setup_argparser_usagemodel(parser):
  group = parser.add_argument_group('usage model')

  group.add_argument('--usage-rate', default=1.0, type=float,
      help='The percentage of owner use vs leaseback use, where 1.0 is 100%% owner use and 0.0 is '
           '100%% leaseback use.  Anything less than 1.0 requires 100-hour inspections and will '
           'raise the hourly cost.  Example: A usage rate of .25 means that the owner flies 1 '
           'hour (tach) for every 3 hours (hobbs) of leaseback operation.')

  group.add_argument('--usage-hobbs-ratio', default=1.2, type=float,
      help='The hobbs to tach ratio. For flight school operation, this number will be high '
           'since certain pre-takeoff operations run more slowly during training. The '
           'default of 1.2 means that for every 5 hours of tach time, 6 hours of hobbs is '
           'billed.')

  group.add_argument('--usage-revenue', default=0, type=float,
      help='The per-hobbs-hour revenue generated by the plane when leased.')

  group.add_argument('--usage-salary', default=0, type=float,
      help='The per-hobbs-hour salary paid as cost of revenue.')


def parse_usage_model(args):
  return UsageModel(
      personal_rate=args.usage_rate,
      hobbs_ratio=args.usage_hobbs_ratio,
      salary=args.usage_salary,
      revenue=args.usage_revenue,
  )


def setup_argparser_acquisition(parser):
  group = parser.add_argument_group('acquisition options')
  group.add_argument('--acquisition-type', default='finance', choices=['cash', 'finance'])
  group.add_argument('--financing-term', default=120, type=int,
      help='Financing term in months.')
  group.add_argument('--financing-rate', default=6.25, type=float,
      help='Financing rate e.g. 6.25 for 6.25%%.')
  group.add_argument('--financing-down', default=15, type=float,
      help='Financing down payment percentage, e.g. 15 for 15%%.')


def parse_acquisition(args):
  if args.acquisition_type == 'cash':
    return AllCash()
  elif args.acquisition_type == 'finance':
    return Mortgage(
        args.financing_down / 100.0,
        args.financing_term,
        args.financing_rate / 100.0,
    )
  else:
    die('Unknown acquisition type: %s' % args.acquisition_type)


def setup_argparser_depreciation(parser):
  # TODO implement
  # --depreciation=fixed:percent
  # --depreciation=exponential:amount:rate
  # --depreciation=linear:months
  # --help-depreciation
  # => multiple invocations uses the combinator
  pass


class SaleAction(argparse.Action):
  def __init__(self, option_strings, dest, nargs=None, **kwargs):
    if nargs is not None:
      raise ValueError('nargs is not allowed.')
    super(SaleAction, self).__init__(option_strings, dest, nargs=0, **kwargs)

  def __call__(self, parser, namespace, values, option_string=None):
    if option_string == '--keep':
      setattr(namespace, self.dest, False)
    elif option_string == '--sell':
      setattr(namespace, self.dest, True)
    else:
      raise argparse.ArgumentError


def setup_argparser_plane_option_overrides(parser):
  # TODO: --upgrade=name
  group = parser.add_argument_group('plane options')
  group.add_argument('--keep', '--sell', dest='sell', action=SaleAction,
      help='Whether to keep or sell the plane following calculation; default is to keep.')
  group.add_argument('--price', type=float, default=None,
      help='Override the price of the airplane.')
  group.add_argument('--annual', type=float, default=None,
      help='Override the expected annual price.')
  group.add_argument('--insurance', type=float, default=None,
      help='Override the insurance rate.')
  group.add_argument('--engine-smoh', type=int, default=0,
      help='Override the time since engine overhaul.')
  group.add_argument('--prop-spoh', type=int, default=0,
      help='Override the time since prop overhaul.')
  group.add_argument('--housing', type=float, default=0,
      help='Yearly housing price for the plane, e.g. tie-downs at KHWD will be '
           'approximately 800/yr.')


def update_plane(plane, args):
  if args.price is not None:
    plane = plane(price=args.price)

  if args.annual is not None:
    plane = plane(annual=args.annual)

  if args.insurance is not None:
    plane = plane(insurance=args.insurance)

  if args.housing:
    plane = plane(yearly_costs=plane.yearly_costs + args.housing)

  if args.engine_smoh:
    engine = Engine(
        overhaul=plane.engine.overhaul,
        tbo=plane.engine.tbo,
        fuel=plane.engine.fuel,
        smoh=args.engine_smoh)
    plane = plane(engine=engine)

  if args.prop_spoh:
    prop = Prop(
        overhaul=plane.prop.overhaul,
        tbo=plane.prop.tbo,
        spoh=args.prop_spoh)
    plane = plane(prop=prop)

  return plane


def show_constants(args):
  for constant, value in CONSTANTS.items():
    print('%s = %s' % (constant, value))


def parse_constants(args):
  constants = CONSTANTS.copy()

  for constant in args.constant:
    try:
      key, value = constant.split('=')
    except IndexError:
      die('Invalid value for --constant: %s' % constant)

    constants[key] = float(value)

  return constants


def setup_argparser_constants_command(parser):
  constants_parser = parser.add_parser('constants', help='List set of constants.')
  constants_parser.set_defaults(func=show_constants)


def setup_argparser_constants_option(parser):
  group = parser.add_argument_group('constant options')
  group.add_argument('--constant', metavar='key=value', action='append', default=[],
      help='Override a constant by setting key=value')


def die(error):
  print(error, file=sys.stderr)
  sys.exit(1)


def parse_range(range_string):
  try:
    return [int(range_string)]
  except ValueError:
    pass

  try:
    start, stop, extent = range_string.split(',', 3)
    return range(int(start), int(stop) + int(extent), int(extent))
  except ValueError:
    die('Invalid number or range string: %s' % range_string)


def main():
  parser = setup_argparser()
  args = parser.parse_args()
  sys.exit(args.func(args))
