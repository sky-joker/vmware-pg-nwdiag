#!/usr/bin/env python3
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
from getpass import getpass
import argparse
import ssl

def options():
    """
    コマンドラインオプション設定

    :rtype: class
    :return: argparse.Namespace
    """
    parser = argparse.ArgumentParser(prog='vmware-pg-nwdiag.py',
                                     add_help=True,
                                     description='VMwareのポートグループに紐付いているVMをnwdiagフォーマットで出力するツール')
    parser.add_argument('--host', '-vc',
                        type=str, required=True,
                        help='vCenterのIP又はホスト名')
    parser.add_argument('--username', '-u',
                        type=str, default='administrator@vsphere.local',
                        help='vCenterのログインユーザー名(default:administrator@vsphere.local)')
    parser.add_argument('--password', '-p',
                        type=str,
                        help='vCenterのログインユーザーパスワード')
    parser.add_argument('--output', '-o',
                        type=str, default='network.diag',
                        help='出力するファイル名(default:network.diag)')
    parser.add_argument('--portgroup', '-pg',
                        type=str, nargs='+',
                        help='ポートグループを指定する場合はポートグルー名を指定する')
    args = parser.parse_args()

    if(not(args.password)):
        args.password = getpass()

    return args

if __name__ == "__main__":
    args = options()

    # SSL証明書対策
    context = None
    if hasattr(ssl, '_create_unverified_context'):
        context = ssl._create_unverified_context()

    # 接続
    si = SmartConnect(host = args.host,
                      user = args.username,
                      pwd = args.password,
                      sslContext = context)

    content = si.content
    objs = content.viewManager.CreateContainerView(content.rootFolder,
                                                   [vim.Network],
                                                   True)

    if(args.portgroup):
        tmp_array = []
        for n in args.portgroup:
            tmp_array.append(list(filter(lambda x: x.name == n, objs.view))[0])
        objs = tmp_array
    else:
        objs = objs.view

    nw_dict = {}
    for nw in objs:
        if(len(nw.vm) > 0):
            nw_dict.update({nw.name:[]})
            for vm in nw.vm:
                nw_dict[nw.name].append(vm.name)

    tmp_array = ["nwdiag"," {\n"]
    for nw_name in nw_dict.keys():
        tmp_array.append("  network ")
        tmp_array.append("\"" + nw_name + "\"" + " {\n")
        for vm in nw_dict[nw_name]:
            tmp_array.append("    " + vm + ";\n")
        tmp_array.append("  }\n")
    tmp_array.append("}")

    with open(args.output, 'w') as f:
        f.write(''.join(tmp_array))
