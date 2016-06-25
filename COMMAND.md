## コマンド
``` bash
# set
etcdctl set /message Hello

# mkdir and set
etcdctl mkdir /foo-service
etcdctl set /foo-service/container1 localhost:1111

# set with ttl
etcdctl set /foo "Expiring Soon" --ttl 20

# get
etcdctl get /message Hello

# watch
etcdctl watch --recursive /foo-service

# watch and exec sh
etcdctl exec-watch --recursive /foo-service -- sh -c 'echo "\"$ETCD_WATCH_KEY\" key was updated to \"$ETCD_WATCH_VALUE\" value by \"$ETCD_WATCH_ACTION\" action"'
```

## クラスタ コマンド
https://coreos.com/etcd/docs/latest/clustering.html
```
# クラスタの状態
etcdctl cluster-health

# リーダーの確認
curl http://localhost:2379/v2/stats/leader

# メンバの確認
etcdctl member list
curl http://localhost:2379/v2/members

#メンバの削除
etcdctl member remove id
curl http://localhost:2379/v2/members/id -XDELETE

# メンバの追加
curl http://localhost:2379/v2/members -XPOST -H "Content-Type: application/json" -d '{"node":"value"}'
```
