# pdu_communication サンプル

このサンプルでは、PDUデータの基本的な通信方法を学びます。箱庭アセットAPIを使用して、箱庭アセット間のデータ交換方法について説明します。

## サンプルプログラムの概要

本サンプルプログラムをビルドすると、`asset_plant` と　`asset_controller`　という２つのバイナリが生成されます。

`asset_plant` は、モーター指示値を読み込み、プラントモデルの観測データを出力します。

`asset_controller` は、プラントモデルの観測データを読み込み、モーター指示値を出力します。

本サンプルでは、簡単のため、制御プログラムおよびプラントの数値計算プログラムは含めず、PDUデータのやり取りがわかるようにしています。

## ファイル内訳

本サンプルでは、以下のファイルを用意しています。

* src/asset_plant.c
* src/asset_controller.c
* src/pdu_info.h
* custom.json

## ファイルの役割

* `asset_plant.c` は、箱庭アセットであり、プラントモデル側の役割を想定したものです。
* `asset_controller.c` は、箱庭アセットであり、制御側の役割を想定したものです。
* `pdu_info.h` は、箱庭アセット間の通信データであるPDUデータを定義したものです。
  * PDUデータそのものは、`geometry_msgs/pdu_ctype_Twist.h`のデータ型を利用しています。
  * また、そのデータのインスタンスは２つあります。
    * PDU_MOTOR_CHANNLE_ID：プラントモデルへの指示値
    * PDU_POS_CHANNEL_ID：プラントモデルの観測データ
* `custom.json`は、上記のPDUデータを箱庭アセットAPIに理解してもらうためのコンフィグファイルです。


## 動作手順

本サンプルプログラムを実行するには、３つの端末を利用します。

* 端末A：asset_plant実行用
* 端末B：asset_controller実行用
* 端末C：箱庭コマンド実行用

**端末Aでの手順：**

hakoniwa-core-cpp-clientでビルドおよびインストール完了後、以下のコマンドを実行します。

```sh
./cmake-build/examples/pdu_communication/asset_plant  examples/pdu_communication/custom.json
```

成功すると、以下のログが出力され、待機状態になります。

```sh
INFO: hako::init() : type: mmap
INFO: HakoProData::init() : type: mmap
INFO: register_master_extension()
INFO: hako::create_master()
INFO: register_asset_extension()
INFO: hako_asset_register :Writer
INFO: hako_conductor thread start
Robot: Robot, PduWriter: Robot_pos
channel_id: 1 pdu_size: 72
INFO: Robot create_lchannel: logical_id=1 real_id=0 size=72
Robot: Robot, PduReader: Robot_motor
channel_id: 0 pdu_size: 72
INFO: Robot create_lchannel: logical_id=0 real_id=1 size=72
INFO: asset(Writer) is registered.
WAIT START
```

**端末Bでの手順：**

以下のコマンドを実行します。

```sh
./cmake-build/examples/pdu_communication/asset_controller examples/pdu_communication/custom.json 
```

成功すると、以下のログが出力され、待機状態になります。

```sh
INFO: hako_asset_register :Reader
INFO: hako::create_asset_controller() : type: mmap
INFO: HakoProData::init() : type: mmap
INFO: register_master_extension()
INFO: register_asset_extension()
Robot: Robot, PduWriter: Robot_motor
channel_id: 0 pdu_size: 72
Robot: Robot, PduReader: Robot_pos
channel_id: 1 pdu_size: 72
INFO: asset(Reader) is registered.
WAIT START
```

**端末Cでの手順:**

箱庭アセットのシミュレーションを開始するためには、別の端末Cで、以下のコマンドを実行します。

```sh
hako-cmd start
```

成功すると、端末AとBとで以下のようにログ出力されます。出力されているログの内容は、各種コールバックで実装されているものです。


端末A：プラントモデル側

```sh
INFO: asset(Writer) is registered.
WAIT START
INFO: HakoMasterData::load() called: master_ext_ = 0x56509102ca00
INFO: HakoProData::on_pdu_data_load()
INFO: HakoProData::on_pdu_data_load() loaded memory
LOADED: PDU DATA
INFO: PDU is created successfully!
WAIT RUNNING
PDU CREATED
INFO: start simulation
INFO: on_manual_timing_control enter
INFO: on_recv: 0
1000: motor data(1001.000000, 1002.000000, 1003.000000)
INFO: on_recv: 0
2000: motor data(1002.000000, 1003.000000, 1004.000000)
INFO: on_recv: 0
3000: motor data(1003.000000, 1004.000000, 1005.000000)
```

端末B：制御側

```sh
INFO: asset(Reader) is registered.
WAIT START
INFO: HakoMasterData::load() called: master_ext_ = 0x55a46287fd20
INFO: HakoProData::on_pdu_data_load()
INFO: HakoProData::on_pdu_data_load() loaded memory
LOADED: PDU DATA
INFO: PDU is created successfully!
WAIT RUNNING
PDU CREATED
INFO: start simulation
INFO: on_manual_timing_control enter
INFO: on_recv: 1
1000: pos data(1.000000, 2.000000, 3.000000)
INFO: on_recv: 1
2000: pos data(2.000000, 3.000000, 4.000000)
INFO: on_recv: 1
3000: pos data(3.000000, 4.000000, 5.000000)
```

次に、以下のコマンドで、シミュレーションを停止およびリセットします。


```sh
hako-cmd stop
hako-cmd reset
```

そうすると、端末AとBとでそれぞれ、以下のログが出力され、サンプルプログラムが終了します。

```sh
NOT RUNNING: curr = 3
WAIT STOP
WAIT RESET
EVENT: reset
INFO: on_manual_timing_control exit
INFO: hako_asset_start() returns 0
```