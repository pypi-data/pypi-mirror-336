# -*- coding: UTF-8 -*-
import json
import re
from optparse import SUPPRESS_HELP, OptionParser

import koji
from koji_cli.lib import _, get_usage_str, get_epilog_str

from ctdy_koji import CtdyKoji

TS_10YEAR = 10 * 365 * 86400


def get_rpms_by_srpm(koji_ip: str, srpm: str, redis_cache=None) -> dict:
    """
    根据srpm获取所有的rpm，区分架构
    Args:
        koji_ip: koji的IP
        srpm: 源码包名称（可能会带.src.rpm） 或者 build id（是个数字）
        redis_cache : redis cache
    Returns:
        {
            "arch":[rpms],
        }

    """
    r = None
    cache_key = f"s_get_rpms_by_srpm_{koji_ip}_{srpm}"
    if redis_cache:
        r = redis_cache.get(cache_key)
    try:
        if r and json.loads(r):
            return json.loads(r)
    except Exception as e:
        print(f"cache error:{koji_ip}_{srpm}. E:{e}")
    srpm = re.sub(".src.rpm$", "", srpm)
    srpm = srpm.replace("--", "-")
    client = CtdyKoji(baseurl=koji_ip)
    build_info = client.get_build_info(srpm)
    rpm_arch_fullname_map = {}
    if build_info:
        rpm_info_list = client.get_rpm_info_list(build_info.get("build_id"))
        for rpm_info in rpm_info_list:
            arch = rpm_info.get("arch")
            nvr = rpm_info.get("nvr")
            fullname = f"{nvr}.{arch}.rpm"
            if arch in rpm_arch_fullname_map:
                rpm_arch_fullname_map[arch].append(fullname)
            else:
                rpm_arch_fullname_map[arch] = [fullname]
    else:
        print(f"NO build_info：{koji_ip}  {srpm} ")
    if rpm_arch_fullname_map and redis_cache:
        redis_cache.set(cache_key, json.dumps(rpm_arch_fullname_map), timeout=TS_10YEAR)
    return rpm_arch_fullname_map


def get_tags(koji_ip, build_id: int, logger) -> list:
    return CtdyKoji(baseurl=koji_ip, logger=logger).get_tags(build_id)


def dict_to_argv(dict_info):
    """dict convert"""
    fake_argv = []
    for key, value in dict_info.items():
        arg_str = f"--{key}={value}"
        fake_argv.append(arg_str)
    return fake_argv


def get_task_method_by_cmd(cmd):
    """get task method name by cmd"""
    if cmd == "image-build":
        return 'image'
    else:
        return cmd


def parse_koji_cli_top_args(args):
    """process options from command line and config file"""

    common_commands = ['build', 'help', 'download-build',
                       'latest-build', 'search', 'list-targets']
    usage = _("%%prog [global-options] command [command-options-and-arguments]"
              "\n\nCommon commands: %s" % ', '.join(sorted(common_commands)))
    parser = OptionParser(usage=usage)
    parser.disable_interspersed_args()
    progname = 'koji'
    parser.__dict__['origin_format_help'] = parser.format_help
    parser.__dict__['format_help'] = lambda formatter=None: (
            "%(origin_format_help)s%(epilog)s" % ({
        'origin_format_help': parser.origin_format_help(formatter),
        'epilog': get_epilog_str()}))
    parser.add_option("-c", "--config", dest="configFile",
                      help=_("use alternate configuration file"), metavar="FILE")
    parser.add_option("-p", "--profile", default=progname,
                      help=_("specify a configuration profile"))
    parser.add_option("--keytab", help=_("specify a Kerberos keytab to use"), metavar="FILE")
    parser.add_option("--principal", help=_("specify a Kerberos principal to use"))
    parser.add_option("--cert", help=_("specify a SSL cert to use"), metavar="FILE")
    parser.add_option("--runas", help=_("run as the specified user (requires special privileges)"))
    parser.add_option("--user", help=_("specify user"))
    parser.add_option("--password", help=_("specify password"))
    parser.add_option("--noauth", action="store_true", default=False,
                      help=_("do not authenticate"))
    parser.add_option("--force-auth", action="store_true", default=False,
                      help=_("authenticate even for read-only operations"))
    parser.add_option("--authtype", help=_("force use of a type of authentication, options: "
                                           "noauth, ssl, password, or kerberos"))
    parser.add_option("-d", "--debug", action="store_true",
                      help=_("show debug output"))
    parser.add_option("--debug-xmlrpc", action="store_true",
                      help=_("show xmlrpc debug output"))
    parser.add_option("-q", "--quiet", action="store_true", default=False,
                      help=_("run quietly"))
    parser.add_option("--skip-main", action="store_true", default=False,
                      help=_("don't actually run main"))
    parser.add_option("-s", "--server", help=_("url of XMLRPC server"))
    parser.add_option("--topdir", help=_("specify topdir"))
    parser.add_option("--weburl", help=_("url of the Koji web interface"))
    parser.add_option("--topurl", help=_("url for Koji file access"))
    parser.add_option("--pkgurl", help=SUPPRESS_HELP)
    parser.add_option("--plugin-paths", metavar='PATHS',
                      help=_("specify additional plugin paths (colon separated)"))
    parser.add_option("--help-commands", action="store_true", default=False,
                      help=_("list commands"))
    # parser.add_option("--keycloakcert", action="store_true", default=True,
    #                   help=_("keycloak authenticate"))
    parser.add_option("--keycloakcert", default='True',
                      help=_("keycloak authenticate"))
    return parser.parse_args(args)


def parse_image_build_args(args):
    """[build] Create a disk image given an install tree"""
    formats = ('vmdk', 'qcow', 'qcow2', 'vdi', 'vpc', 'rhevm-ova',
               'vsphere-ova', 'vagrant-virtualbox', 'vagrant-libvirt',
               'vagrant-vmware-fusion', 'vagrant-hyperv', 'docker', 'raw-xz',
               'liveimg-squashfs', 'tar-gz')
    usage = _("usage: %prog image-build [options] <name> <version> "
              "<target> <install-tree-url> <arch> [<arch> ...]")
    usage += _("\n       %prog image-build --config <FILE>\n")
    parser = OptionParser(usage=get_usage_str(usage))
    parser.add_option("--background", action="store_true",
                      help=_("Run the image creation task at a lower priority"))
    parser.add_option("--config",
                      help=_("Use a configuration file to define image-build options "
                             "instead of command line options (they will be ignored)."))
    parser.add_option("--disk-size", default=10,
                      help=_("Set the disk device size in gigabytes"))
    parser.add_option("--distro",
                      help=_("specify the RPM based distribution the image will be based "
                             "on with the format RHEL-X.Y, CentOS-X.Y, SL-X.Y, or Fedora-NN. "
                             "The packages for the Distro you choose must have been built "
                             "in this system."))
    parser.add_option("--format", default=[], action="append",
                      help=_("Convert results to one or more formats "
                             "(%s), this option may be used "
                             "multiple times. By default, specifying this option will "
                             "omit the raw disk image (which is 10G in size) from the "
                             "build results. If you really want it included with converted "
                             "images, pass in 'raw' as an option.") % ', '.join(formats))
    parser.add_option("--kickstart", help=_("Path to a local kickstart file"))
    parser.add_option("--ksurl", metavar="SCMURL",
                      help=_("The URL to the SCM containing the kickstart file"))
    parser.add_option("--ksversion", metavar="VERSION",
                      help=_("The syntax version used in the kickstart file"))
    parser.add_option("--noprogress", action="store_true",
                      help=_("Do not display progress of the upload"))
    parser.add_option("--nowait", action="store_false", dest="wait",
                      help=_("Don't wait on image creation"))
    parser.add_option("--ova-option", action="append",
                      help=_("Override a value in the OVA description XML. Provide a value "
                             "in a name=value format, such as 'ovf_memory_mb=6144'"))
    parser.add_option("--factory-parameter", nargs=2, action="append",
                      help=_("Pass a parameter to Image Factory. The results are highly specific "
                             "to the image format being created. This is a two argument parameter "
                             "that can be specified an arbitrary number of times. For example: "
                             "--factory-parameter docker_cmd '[ \"/bin/echo Hello World\" ]'"))
    parser.add_option("--release", help=_("Forcibly set the release field"))
    parser.add_option("--repo", action="append",
                      help=_("Specify a repo that will override the repo used to install "
                             "RPMs in the image. May be used multiple times. The "
                             "build tag repo associated with the target is the default."))
    parser.add_option("--scratch", action="store_true",
                      help=_("Create a scratch image"))
    parser.add_option("--skip-tag", action="store_true",
                      help=_("Do not attempt to tag package"))
    parser.add_option("--can-fail", action="store", dest="optional_arches",
                      metavar="ARCH1,ARCH2,...", default="",
                      help=_("List of archs which are not blocking for build "
                             "(separated by commas."))
    parser.add_option("--specfile", metavar="URL",
                      help=_("SCM URL to spec file fragment to use to generate wrapper RPMs"))
    parser.add_option("--wait", action="store_true",
                      help=_("Wait on the image creation, even if running in the background"))

    return parser.parse_args(args)


def get_task_label_by_task(task_info):
    """get koji task label by task info"""
    method = task_info['method']
    label = task_info['arch']
    if method in ('livecd', 'appliance', 'image', 'livemedia') and 'request' in task_info:
        stuff = task_info['request']
        label = f'{stuff[0]}-{stuff[1]}'
    return label


def get_latest_koji_task_id(owner, cmd, cmd_label, create_time, session, all=False):
    """get latest koji task id"""
    task_id = None
    tasks = list_tasks(owner, cmd, create_time, session, all)
    if not tasks:
        tasks = list_tasks(owner, cmd, None, session, all)
    if tasks:
        tasks.reverse()
        for task_info in tasks:
            if cmd_label:
                task_lable = get_task_label_by_task(task_info)
                if cmd_label == task_lable:
                    task_id = task_info['id']
                    break
            else:
                task_id = task_info['id']
                break
    return task_id


def list_tasks(owner, cmd, create_time, session, all=False):
    "Retrieve a list of tasks"
    method = get_task_method_by_cmd(cmd)
    user = session.getUser(owner)
    callopts = {
        'decode': True,
        'createdAfter': create_time,
        'owner': user['id'],
        'method': method,
    }
    if not all:
        callopts['state'] = [0, 1, 4]
    qopts = {'order': 'priority,create_time'}
    tasklist = session.listTasks(callopts, qopts)
    tasks = dict([(x['id'], x) for x in tasklist])

    # thread the tasks
    for t in tasklist:
        if t['parent'] is not None:
            parent = tasks.get(t['parent'])
            if parent:
                parent.setdefault('children', [])
                parent['children'].append(t)
                t['sub'] = True

    if not tasklist:
        return None
    print_task_headers()
    for t in tasklist:
        if t.get('sub'):
            # this subtask will appear under another task
            continue
        print_task_recurse(t)
    return tasklist


def print_task_headers():
    """Print the column headers"""
    print("ID       Pri  Owner                State    Arch       Name")


def print_task_recurse(task, depth=0):
    """Print a task and its children"""
    print_task(task, depth)
    for child in task.get('children', ()):
        print_task_recurse(child, depth + 1)


def print_task(task, depth=0):
    """Print a task"""
    task = task.copy()
    task['state'] = koji.TASK_STATES.get(task['state'], 'BADSTATE')
    fmt = "%(id)-8s %(priority)-4s %(owner_name)-20s %(state)-8s %(arch)-10s "
    if depth:
        indent = "  " * (depth - 1) + " +"
    else:
        indent = ''
    label = koji.taskLabel(task)
    print(''.join([fmt % task, indent, label]))
