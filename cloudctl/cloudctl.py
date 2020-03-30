import click
import logging
import functools
from tabulate import tabulate
from .functions import *

logging.basicConfig(format=(
    '%(asctime)s %(name)-12s %(funcName)-8s %(message)s'))
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def common_options(f):
    options = [
        click.option('-d', '--debug', envvar="CLOUDCTL_DEBUG", show_default=True,
                     is_flag=True, help='Enable debug mode'),

        click.option('--dry-run', envvar="CLOUDCTL_DRY_RUN", show_default=True,
                     is_flag=True, help='Dry Run mode'),

        click.option('-a', '--auto-approve', envvar="CLOUDCTL_AUTO_APPROVE", show_default=True,
                     is_flag=True, help='Auto Approve operation'),

        click.option('-c', '--cloud', type=click.Choice(['aws', 'gcp', 'azure'], case_sensitive=False),
                     envvar="CLOUDCTL_CLOUD", default='aws', show_default=True, help='Cloud provider to query'),

        click.option('-t', '--tags', multiple=True,
                     type=click.Tuple([str, str]), help='Query resources by tags'),

        click.option('-r', '--role', multiple=False,
                     type=str, help='Query resource by role Tag'),
    ]
    return functools.reduce(lambda x, opt: opt(x), options, f)


@click.group()
@common_options
@click.pass_context
def cloudctl(ctx, **kwargs):
    """ Cloud Manager cli """
    if kwargs["debug"]:
        logger.setLevel(logging.DEBUG)
    ctx.obj['logger'] = logger


@cloudctl.group()
@click.pass_context
def get(ctx):
    """get action"""


@cloudctl.group()
@click.pass_context
def stop(ctx):
    """stop action"""


@common_options
@get.command('instances')
@click.pass_context
def get_instances_cmd(ctx, **kwargs):
    if kwargs["debug"]:
        logger.setLevel(logging.DEBUG)
    ctx.obj['cloud'] = kwargs['cloud']

    # create tags dict for query
    tags = create_tags_dict(kwargs['tags'], kwargs['role'])
    logger.debug("tags=" + str(tags))

    print_instances(instances=list_instances(
        logger=ctx.obj['logger'], tags=tags))


@common_options
@get.command('instances-api')
@click.pass_context
def get_instances_api(ctx, **kwargs):
    if kwargs["debug"]:
        logger.setLevel(logging.DEBUG)
    ctx.obj['cloud'] = kwargs['cloud']

    # create tags dict for query
    tags = create_tags_dict(kwargs['tags'], kwargs['role'])
    logger.debug("tags=" + str(tags))

    print_instances(instances=list_instances_api(
        logger=ctx.obj['logger'], tags=tags))


@common_options
@stop.command('instances')
@click.pass_context
def stop_instance_cmd(ctx, **kwargs):
    if kwargs["debug"]:
        logger.setLevel(logging.DEBUG)
    logger.debug(kwargs.keys())
    # create tags dict for query
    tags = create_tags_dict(kwargs['tags'], kwargs['role'])
    logger.debug("tags=" + str(tags))

    instances = list_instances(logger=ctx.obj['logger'], tags=tags)
    print_instances(instances)
    auto_approve = kwargs['auto_approve']
    logger.debug("auto approve=" + str(auto_approve))

    if not auto_approve:
        if click.confirm('Are you sure you want to stop instance/s above?', default=False):
            pass
        else:
            click.echo('Operation aborted')
            exit
    ids = [ins['Id'] for ins in instances if 'Id' in ins]
    logger.debug(ids)
    stop_instances(ids=ids)


def print_instances(instances):
    if len(instances) == 0:
        click.echo('No instances found by criteria')

    else:
        headers = instances[0].keys()
        table_values = [x.values() for x in instances]
        click.echo(tabulate(table_values, headers))


def create_tags_dict(tags_tuple, role):
    tags = dict((k, v) for k, v in tags_tuple)
    if role:
        tags['role'] = role

    return tags


def start():

    try:
        cloudctl(obj={})
    except Exception as e:
        print(e)


if __name__ == '__main__':
    start()
