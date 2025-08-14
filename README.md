# Hakoniwa Core Pro Tutorial Examples

このリポジトリには、Hakoniwa Core Proの機能を示すサンプルプログラムが含まれています。

## 概要

各サンプルは`examples`ディレクトリ以下に格納されています。

*   **hello_world**: Hakoniwaアセットの基本的な作成方法とライフサイクルを示します。
*   **pdu_communication**: 2つのアセット（コントローラとプラント）がPDU（Protocol Data Unit）を介して通信する方法を示します。
*   **service**: アセットがクライアント・サーバーモデルでサービスを提供・利用する方法を示します。

## 前提環境

*   **OS**: Ubuntu 24.04 LTS 以上
*   **Python**: 3.12 
    *   `hakoniwa-pdu`のインストール:
        ```bash
        pip install hakoniwa-pdu
        ```
*   **その他**: `git`, `cmake`, `build-essential`

### 環境構築

以下のコマンドを実行して、必要なパッケージをインストールしてください。

```bash
echo "deb [trusted=yes] https://hakoniwalab.github.io/apt stable main" \
 | sudo tee /etc/apt/sources.list.d/hakoniwa.list
```

```bash
sudo apt update
```

```bash
sudo apt install -y git cmake build-essential
```

```bash
sudo apt install -y hakoniwa-core-full
```

```bash
sudo usermod -aG hakoniwa <your-username>
```

```bash
newgrp hakoniwa
```

## ビルド方法

1.  ビルド用のディレクトリを作成します。
    ```bash
    mkdir build
    cd build
    ```
2.  CMakeを実行してビルドファイルを生成します。`examples`ディレクトリを指定してください。
    ```bash
    cmake ../examples
    ```
3.  makeコマンドでビルドを実行します。
    ```bash
    make
    ```
4.  ビルドが成功すると、`build`ディレクトリ以下に各サンプルの実行ファイルが生成されます。
    *   `hello_world/hello_world`
    *   `pdu_communication/asset_controller`
    *   `pdu_communication/asset_plant`
    *   `service/asset_client`
    *   `service/asset_server`

## 各サンプルの実行方法

各サンプルは、複数の端末（ターミナル）を使用して実行します。

### hello_world

1.  **端末A**でアセットを起動します。

    ```bash
    ./build/hello_world/hello_world HelloWorld examples/hello_world/custom.json 20
    ```

2.  **端末B**でシミュレーションを開始します。

    ```bash
    hako-cmd start
    ```

### pdu_communication

1.  **端末A**で`asset_plant`を起動します。

    ```bash
    ./build/examples/pdu_communication/asset_plant examples/pdu_communication/custom.json
    ```

2.  **端末B**で`asset_controller`を起動します。

    ```bash
    ./build/examples/pdu_communication/asset_controller examples/pdu_communication/custom.json
    ```

3.  **端末C**でシミュレーションを開始します。

    ```bash
    hako-cmd start
    ```

### service

1.  **端末A**で`asset_server`を起動します。

    ```bash
    ./build/examples/service/asset_server examples/service/custom.json normal
    ```

2.  **端末B**で`asset_client`を起動します。

    ```bash
    ./build/examples/service/asset_client examples/service/custom.json
    ```
