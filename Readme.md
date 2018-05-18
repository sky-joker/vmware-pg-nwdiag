# vmware-pg-nwdiag

VMwareのポートグループに紐付いているVMをnwdiagフォーマットで出力するツール

## 必要条件

* python3
* pyvmomi

## インストール

```
$ git clone https://github.com/sky-joker/vmware-pg-nwdiag.git
$ cd vmware-pg-nwdia
$ pip3 install -r requirements.txt
$ chmod +x vmware-pg-nwdiag.py
```

## 使い方

特定のポートグループを指定する場合

```bash
$ ./vmware-pg-nwdiag.py -vc vcenter.local -pg "VM Network" PG01
Password:
```

全ポートグループの情報を取得する場合

```bash
$ ./vmware-pg-nwdiag.py -vc vcenter.local
Password:
```

## 画像へ変換

画像へ変換する場合は [nwdiag](http://blockdiag.com/ja/nwdiag/index.html) が必要です。

```
$ pip3 install nwdiag
```

作成したポートグループの情報をnwdiagで画像に変換します。

```bash
$ nwdiag -f DejaVuSerif.ttf network.diag
```

![](https://sky-joker.tech/wp-content/uploads/2018/05/network.png)