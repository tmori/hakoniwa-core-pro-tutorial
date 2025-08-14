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

各サンプルの詳細な実行手順については、それぞれのディレクトリにある`README.md`ファイルを参照してください。

*   [hello_world](./examples/hello_world/README.md)
*   [pdu_communication](./examples/pdu_communication/README.md)
*   [service](./examples/service/README.md)
