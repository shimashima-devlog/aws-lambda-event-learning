# aws-lambda-event-learning

## 概要
- 業務を通してデータ受け渡しの流れを学んだため、おさらいする目的で作成したサンプルコード。
- S3イベントを起点として、3つのLambdaが順番に処理する構成を想定した。
- ローカル環境でLambda間の処理とデータの受け渡しを確認する。

## 目的
- `event`と`Payload`の関係を理解する。
- S3からLambdaへイベントが渡される流れを理解する。
- Lambdaから別のLambdaを呼び出す流れを理解する。
- `InvocationType="Event"`による非同期Invokeの動きを理解する。

## 作成方針
- 業務を通して、S3イベントを起点としたLambdaの実行や、`boto3`を使用したLambda間の非同期連携について学んだ。
- 今回新たに知ったAWS Lambdaの一般的な仕組みを、自分で再確認することを目的としている。
- 業務で扱った処理内容やデータ構造は使用せず、学習用の題材を別途設計した。

## この構成にした理由
- Lambda間でデータがどのように受け渡されるかを確認するため、3つのLambdaを順番に呼び出す構成とした。
- Lambda側はAWS上での実行を想定した`boto3`の書き方を残し、ローカルテスト側でAWSへの通信部分をモックに置き換えた。

## 使用技術
- Python 3.12
- boto3
- unittest.mock

## 学習対象
- AWS Lambda
- Amazon S3
- Lambda間の非同期Invoke
- S3 ObjectCreatedイベント
- CloudWatch Logs

## 処理の流れ
本来のAWS環境では、以下の流れを想定。

```text
[S3]
  │
  │ ObjectCreatedイベント
  ▼
[file_event_handler]
  │
  │ 非同期Invoke
  │ Payload:
  │ ・bucket_name
  │ ・object_key
  ▼
[file_metadata_builder]
  │
  │ 非同期Invoke
  │ Payload:
  │ ・bucket_name
  │ ・object_key
  │ ・file_name
  │ ・file_extension
  ▼
[learning_log_writer]
  │
  │ print()でログ出力
  ▼
[CloudWatch Logs]
```

### file_event_handler
- S3のObjectCreatedイベントを`event`として受け取る想定。
- S3イベントからバケット名とオブジェクトキーを取得。
- 取得した情報を`Payload`として`file_metadata_builder`を非同期で呼び出す。

### file_metadata_builder
- `file_event_handler`から送られた`Payload`を`event`として受け取る。
- オブジェクトキーからファイル名と拡張子を取得。
- ファイル情報を`Payload`として`learning_log_writer`を非同期で呼び出す。

### learning_log_writer
- `file_metadata_builder`から送られた`Payload`を`event`として受け取る。
- 受け取ったファイル情報をログへ出力。
- AWS上で実行する場合、`print()`の出力はCloudWatch Logsで確認する想定。

## ローカルテスト
今回は、AWS環境を使用せずに疎通確認を行うため、AWSへの通信部分を`MagicMock`に置き換えた。
これにより、Lambda側の`boto3`を使用した形式を残したまま、ローカル環境で処理の流れを確認できるようにした。

ローカルテストでは、以下の流れとなる。

```text
[fake_s3_event]
  │
  │ S3イベント形式のテストデータ
  ▼
[file_event_handler]
  │
  │ fake_invoke()
  │ Payload:
  │ ・bucket_name
  │ ・object_key
  ▼
[file_metadata_builder]
  │
  │ fake_invoke()
  │ Payload:
  │ ・bucket_name
  │ ・object_key
  │ ・file_name
  │ ・file_extension
  ▼
[learning_log_writer]
  │
  │ print()でログ出力
  ▼
[PowerShell]
```

## 確認した内容
- S3イベント形式のデータを`file_event_handler`の`event`として受け取れること。
- `file_event_handler`から渡した`Payload`を`file_metadata_builder`の`event`として受け取れること。
- オブジェクトキーからファイル名と拡張子を取得できること。
- `file_metadata_builder`から渡した`Payload`を`learning_log_writer`の`event`として受け取れること。
- 3つ目の処理までデータが渡り、ログを出力できること。

## 実行方法
1. Python 3.12がインストールされている環境で、プロジェクトフォルダを開く。
2. ターミナルでローカルテストを実行する。`python local_test.py`
3. ターミナルに出力されたログにより、`file_event_handler`、`file_metadata_builder`、`learning_log_writer`の順に処理されたことを確認する。

## 補足
- 現時点では、実際のAWS環境へのデプロイおよび動作確認は未実施。