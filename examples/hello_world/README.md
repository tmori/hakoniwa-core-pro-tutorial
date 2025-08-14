# Hello world サンプル

このサンプルでは、箱庭アセットの基本的な作成方法を学びます。箱庭アセットAPIを使用して、アセットの起動と各種コールバック関数の実装方法について説明します。

## コード説明

ここでは、主なコードの部分について説明します。サンプルコードでは、以下の主要な機能が実装されています：

* 箱庭アセットの登録と初期化
* コールバック関数の実装（初期化、シミュレーションステップ、リセット処理など）
* シミュレーションの開始と終了
* コード内の各セクションには、その機能や役割についてのコメントが含まれています。

## 動作手順

**端末Aでの手順：**

hakoniwa-core-cpp-clientでビルドおよびインストール完了後、以下のコマンドを実行します。

```sh
./build/hello_world/hello_world HelloWorld ./examples/hello_world/custom.json 100
```

成功すると、以下のログが出力され、待機状態になります。

```sh
INFO: hako::init() : type: mmap
INFO: HakoProData::init() : type: mmap
INFO: register_master_extension()
INFO: hako::create_master()
INFO: register_asset_extension()
INFO: hako_asset_register :HelloWorld
INFO: hako_conductor thread start
Robot: ROBOT, PduWriter: ROBOT_motor
channel_id: 0 pdu_size: 48
INFO: ROBOT create_lchannel: logical_id=0 real_id=0 size=48
INFO: asset(HelloWorld) is registered.
WAIT START
```

**端末Bでの手順:**

箱庭アセットのシミュレーションを開始するためには、別の端末Bで、以下のコマンドを実行します。

```sh
hako-cmd start
```

成功すると、端末Aで以下のようにログ出力されます。出力されているログの内容は、各種コールバックで実装されているものです。


```sh
INFO: asset(HelloWorld) is registered.
WAIT START
INFO: HakoMasterData::load() called: master_ext_ = 0x557132c0da00
INFO: HakoProData::on_pdu_data_load()
INFO: HakoProData::on_pdu_data_load() loaded memory
LOADED: PDU DATA
INFO: PDU is created successfully!
INFO: my_on_initialize enter
INFO: sleep 1sec
INFO: my_on_initialize exit
WAIT RUNNING
PDU CREATED
INFO: start simulation
SYNC MODE: true
INFO: on_simulation_step enter: 100000
INFO: sleep 1sec
INFO: on_simulation_step exit
INFO: on_simulation_step enter: 200000
INFO: sleep 1sec
INFO: on_simulation_step exit
INFO: on_simulation_step enter: 300000
INFO: sleep 1sec
INFO: on_simulation_step exit
INFO: on_simulation_step enter: 400000
```

次に、以下のコマンドで、シミュレーションを停止およびリセットします。


```sh
hako-cmd stop
hako-cmd reset
```

そうすると、以下のログが出力され、サンプルプログラムが終了します。

```sh
INFO: on_simulation_step enter: 500000
INFO: sleep 1sec
INFO: on_simulation_step exit
NOT RUNNING: curr = 3
WAIT STOP
WAIT RESET
INFO: my_on_reset enter
INFO: sleep 1sec
INFO: my_on_reset exit
INFO: stopped simulation
INFO: hako_asset_start() returns 4
EVENT: reset
```