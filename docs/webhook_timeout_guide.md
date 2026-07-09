# LINE Messaging API Webhookタイムアウト（2秒制限）に関する補足

LINE Messaging APIのWebhookにおけるタイムアウトの仕様と、それを回避するための実装についての補足情報です。

---

## 1. 2秒タイムアウト仕様（根拠）

LINEプラットフォームは、Webhook送信後にボットサーバーから2秒以内にレスポンスを受信できなかった場合、エラーとして記録します。

* **公式仕様の根拠（URL）**:
  [LINE Developers: Webhookのエラーの原因と統計情報を確認する](https://developers.line.biz/ja/docs/messaging-api/check-webhook-error-statistics/#check-error-reason)
  > ※ ページ内の「エラーが発生した原因を確認する」項目に、`request_timeout`（ボットサーバーがWebhookを受信してから2秒以内にLINEプラットフォームにレスポンスを返さなかった場合に発生する）の記述があります。

---

## 2. 同期処理と非同期処理の違い

* **同期処理（現在の教材の標準実装）**:
  Webhook受信スレッドでそのまま時間のかかる処理（AIのAPI呼び出しなど）を行う構成。ユーザーへの返信は届くものの、2秒を超えるとLINE Developersコンソールのエラー統計にエラーが蓄積します。
* **非同期処理（推奨される回避策）**:
  Webhook受信時は即座に `200 OK` を返却し、時間のかかる処理と返信はバックグラウンドスレッドで実行する構成。これによりエラー統計への記録を防ぐことができます。

---

## 3. 実装参考コード

非同期スレッド処理を実装した具体的な参考コードは、以下を参照してください。

* [chapter5/app_async.py](../chapter5/app_async.py)
