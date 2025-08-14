# service サンプル

このサンプルでは、アセットがクライアント・サーバーモデルでサービスを提供・利用する方法を学びます。

## 動作手順

本サンプルプログラムを実行するには、2つの端末を利用します。

*   端末A: `asset_server` 実行用
*   端末B: `asset_client` 実行用

### 端末Aでの手順

以下のコマンドを実行して、`asset_server`を起動します。

```bash
./build/service/asset_server examples/service/custom.json normal
```

成功すると、以下のログが出力されます。

```sh
INFO: hako::init() : type: mmap
INFO: HakoProData::init() : type: mmap
INFO: register_master_extension()
INFO: hako::create_master()
INFO: register_asset_extension()
INFO: hako_asset_register :Server
INFO: hako_conductor thread start
Robot: drone1, PduWriter: drone1_pos
channel_id: 0 pdu_size: 80
INFO: drone1 create_lchannel: logical_id=0 real_id=0 size=80
Robot: drone1, PduReader: drone1_pos
channel_id: 0 pdu_size: 80
Robot: drone2, PduWriter: drone2_pos
channel_id: 0 pdu_size: 80
INFO: drone2 create_lchannel: logical_id=0 real_id=1 size=80
Robot: drone2, PduReader: drone2_pos
channel_id: 0 pdu_size: 80
INFO: asset(Server) is registered.
INFO: Service/Add create_lchannel: logical_id=0 real_id=2 size=320
INFO: create_lchannel() serviceName: Service/Add channel_id: 0 total_size: 320
INFO: Service/Add create_lchannel: logical_id=1 real_id=3 size=312
INFO: create_lchannel() serviceName: Service/Add channel_id: 1 total_size: 312
WAIT START
```

### 端末Bでの手順

以下のコマンドを実行して、`asset_client`を起動します。

```bash
./build/service/asset_client examples/service/custom.json
```

成功すると、以下のログが出力されます。

```sh
INFO: hako_asset_register :Client
INFO: hako::create_asset_controller() : type: mmap
INFO: HakoProData::init() : type: mmap
INFO: register_master_extension()
INFO: register_asset_extension()
Robot: drone1, PduWriter: drone1_pos
channel_id: 0 pdu_size: 80
Robot: drone1, PduReader: drone1_pos
channel_id: 0 pdu_size: 80
Robot: drone2, PduWriter: drone2_pos
channel_id: 0 pdu_size: 80
Robot: drone2, PduReader: drone2_pos
channel_id: 0 pdu_size: 80
INFO: asset(Client) is registered.
INFO: create_lchannel() serviceName: Service/Add channel_id: 0 total_size: 320
INFO: create_lchannel() serviceName: Service/Add channel_id: 1 total_size: 312
WAIT START
```


**端末Cでの手順:**

箱庭アセットのシミュレーションを開始するためには、別の端末Cで、以下のコマンドを実行します。

```sh
hako-cmd start
```

成功すると、端末AとBとで以下のようにログ出力されます。出力されているログの内容は、各種コールバックで実装されているものです。


端末A：サーバー側

```sh
WAIT START
INFO: HakoMasterData::load() called: master_ext_ = 0x55ee0b8eba00
INFO: HakoProData::on_pdu_data_load()
INFO: HakoProData::on_pdu_data_load() loaded memory
LOADED: PDU DATA
INFO: PDU is created successfully!
INFO: HakoServiceServer::initialize() called
INFO: Service server initialized successfully: Service/Add
WAIT RUNNING
PDU CREATED
INFO: start simulation
*************** START SERVICE SERVER ***************
INFO: APL poll...
ERORR: APL is not request_in.
SYNC MODE: true
IN: a=1 b=2
OUT: sum=3
```

端末B：クライアント側

```sh
INFO: asset(Reader) is registered.
INFO: HakoMasterData::load() called: master_ext_ = 0x55e6b991ada0
INFO: HakoProData::on_pdu_data_load()
INFO: HakoProData::on_pdu_data_load() loaded memory
LOADED: PDU DATA
INFO: PDU is created successfully!
INFO: my_on_initialize()...
INFO: register_data_recv_event() serviceName: Service/Add channel_id: 1 recv_event_id: 1
INFO: client_id: 0 clientName: Client01
INFO: service_client.initialize() returns 1
WAIT RUNNING
PDU CREATED
INFO: start simulation
*************** START SERVICE CLIENT ***************
INFO: APL request: a=1 b=2
INFO: APL request...
INFO: APL wait for response 1
SYNC MODE: true
OUT: sum=3
*************** FINISH SERVICE CLIENT ***************
```

