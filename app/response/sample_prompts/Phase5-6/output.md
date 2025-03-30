了解しました。フェーズ5とフェーズ6に関する専門的で丁寧な日本語解説資料を作成します。モバイルアプリと通信セキュリティ、そしてSSLピンニングに関する理論と実装方法を、図解とコード例を交えて、情報系大学院生向けにわかりやすく網羅的にまとめます。

資料の完成までしばらくお待ちください。でき次第お知らせします。

# モバイルアプリのセキュリティとSSLピンニング 詳細解説（フェーズ5・6）

ここでは、情報系大学院1年生を対象として**モバイルアプリのセキュリティ**（フェーズ5）および**SSLピンニング**（フェーズ6）について専門的かつ分かりやすく解説します。モバイルアプリ特有の通信セキュリティ上の課題と、その対策であるSSLピンニングの原理と実装方法を中心に説明します（他のフェーズの内容には触れません）。

## フェーズ5: モバイルアプリのセキュリティ

### モバイルアプリと通信セキュリティの課題
モバイルアプリでは、ユーザーのスマートフォン上で動作するクライアントアプリと遠隔のサーバーが通信を行います。この通信を安全に保つことには、Webブラウザとは異なるモバイルアプリ特有の課題があります。

- **ユーザーに見えない証明書エラー**: Webブラウザではサーバー証明書に問題があるとユーザーに警告が表示されますが、ネイティブアプリでは証明書の検証処理はアプリ内部で行われ、ユーザーには直接見えません。開発者が適切に実装しないと、不正な証明書を検知できずに通信を続行してしまう恐れがあります。
- **多様なネットワーク環境**: モバイル端末は公共Wi-Fiやモバイル通信網など様々なネットワークに接続します。不特定多数が利用するネットワークでは通信が盗聴・改ざんされるリスクが高く、アプリ側で常にネットワークが信頼できるとは限りません。そのため通信経路自体を安全に保護する必要があります。
- **クライアント側の脆弱性**: モバイルアプリは端末上で動作するため、ユーザーや攻撃者にコードを解析・改変されるリスクもあります。例えば証明書検証の処理を意図的に無効化するような改変や、モバイルOS自体のセキュリティ破り（ルート化・脱獄）によって、通信内容を傍受される可能性も考慮する必要があります。
- **認証情報や個人情報のやりとり**: モバイルアプリはログイン認証や個人データの送受信など機密性の高い情報を扱うことが多く、もし通信が保護されていないと深刻な情報漏洩につながります。特に銀行や決済、健康情報を扱うアプリでは通信セキュリティ上の脅威が高くなります。

上記のような理由から、モバイルアプリでは通信経路の安全性（機密性・完全性・認証）を確保するための対策が極めて重要です。次に、アプリとサーバー間の通信を守る基本的な方法について具体的に説明します。

### アプリとサーバー間の通信を保護する基本対策
モバイルアプリの通信を安全に保つために、以下の基本的なセキュリティ対策を講じます。それぞれについて包括的に解説します。

- **TLSによる通信暗号化の徹底**: アプリとサーバー間の通信には必ずHTTPS（TLS）プロトコルを使用し、盗聴や改ざんを防ぎます。TLSは通信内容を暗号化すると同時にサーバーの正当性を証明する仕組みを提供します。平文のHTTP通信は原則禁止し、最新のTLSバージョン（TLS 1.2以降）のみを許可します。AndroidではAPIレベル28（Android 9）以降、デフォルトでクリアテキスト通信（HTTP）が禁止されており ([Network security configuration  |  Security  |  Android Developers](https://developer.android.com/privacy-and-security/security-config#:~:text=Opt%20out%20of%20cleartext%20traffic))、iOSでも**App Transport Security (ATS)**により新規アプリでの安全でない通信（HTTP）がデフォルトでブロックされます ([アプリ転送セキュリティ | iOS - Google for Developers](https://developers.google.com/admob/ios/privacy/app-transport-security?hl=ja#:~:text=%E3%82%A2%E3%83%97%E3%83%AA%E8%BB%A2%E9%80%81%E3%82%BB%E3%82%AD%E3%83%A5%E3%83%AA%E3%83%86%E3%82%A3%20%7C%20iOS%20,Security%EF%BC%88ATS%EF%BC%89%E3%81%AF%E3%80%81%E5%AE%89%E5%85%A8%E3%81%AA%E6%8E%A5%E7%B6%9A%E3%82%92%E5%BC%B7%E5%88%B6%E3%81%99%E3%82%8B%E3%83%97%E3%83%A9%E3%82%A4%E3%83%90%E3%82%B7%E3%83%BC%E6%A9%9F%E8%83%BD%E3%81%A7%E3%81%99%E3%80%82%E6%96%B0%E3%81%97%E3%81%84%E3%82%A2%E3%83%97%E3%83%AA%E3%81%A7%E3%81%AF%E3%83%87%E3%83%95%E3%82%A9%E3%83%AB%E3%83%88%E3%81%A7%E6%9C%89%E5%8A%B9%E3%81%AB%E3%81%AA%E3%81%A3%E3%81%A6%E3%81%84%E3%81%BE%E3%81%99%E3%80%82%20ATS%20%E3%81%AB%E6%BA%96%E6%8B%A0%E3%81%97%E3%81%A6%E3%81%84%E3%81%AA%E3%81%84%E3%82%A2%E3%83%97%E3%83%AA%E3%81%8C%20HTTP))。これらプラットフォームの仕組みを活用し、暗号化されていない通信が発生しないようにします。またTLS証明書や暗号スイートは強度の高いものを使用し、古いバージョン（例: TLS 1.0/1.1）や脆弱なアルゴリズムは無効化します。

- **サーバー証明書の正当性検証**: サーバーから提示される証明書をアプリ側で厳格に検証します。通常、この検証にはモバイルOSに組み込まれた信頼できる認証局(CA)のリスト（ルート証明書ストア）が利用されます。検証では①証明書が有効な期間内であること、②信頼できるルートCAまでの**証明書チェーン**が正しく構築できること、③サーバーのホスト名と証明書の対象名（CN/SAN）が一致すること、を確認します。プラットフォームの提供するAPI（例えばAndroidの`HttpsURLConnection`や`OkHttp`、iOSの`URLSession`など）を正しく使えば通常これらは自動的に実施されます。しかし、開発者がデバッグ目的で証明書検証を無効化したり、不適切な実装をすると検証がスキップされてしまいます。例えばAndroidでカスタムの`X509TrustManager`を用いて常に`true`を返すようにしてしまうと、どんな証明書でも受け入れてしまい**本来の検証が無効化**されます ([安全でない X.509 TrustManager  |  Security  |  Android Developers](https://developer.android.com/privacy-and-security/risks/unsafe-trustmanager?hl=ja#:~:text=Android%20%E3%82%A2%E3%83%97%E3%83%AA%E3%81%AB%20))。その結果、攻撃者が自己署名証明書や不正な証明書を提示してもアプリが「正当なサーバー」とみなして通信を続けてしまいます。こうした実装上の脆弱性を避けるため、証明書検証は基本的にOSやライブラリの標準挙動に任せ、独自に無効化しないことが重要です。

- **開発・テスト時と本番時の証明書設定の分離**: 開発中はローカルサーバーや自己署名証明書を使う必要がある場合があります。その際にも本番ビルドで証明書検証を無効化したコードが残らないよう、環境ごとに設定を分離します。AndroidではNetwork Security Configurationを用いてデバッグビルド時のみ特定の自己署名CAを信頼させる設定（`debug-overrides`）が可能であり、コードを変更せずに開発用証明書を許可できます ([Network security configuration  |  Security  |  Android Developers](https://developer.android.com/privacy-and-security/security-config#:~:text=When%20debugging%20an%20app%20that,release%20builds)) ([安全でない X.509 TrustManager  |  Security  |  Android Developers](https://developer.android.com/privacy-and-security/risks/unsafe-trustmanager?hl=ja#:~:text=NetworkSecurityConfig,%E3%82%92%E5%AE%9F%E8%A3%85%E3%81%9B%E3%81%9A%E3%81%AB%20NetworkSecurityConfig%20%E3%81%AE%E4%BD%BF%E7%94%A8%E3%82%92%E6%A4%9C%E8%A8%8E%E3%81%97%E3%81%A6%E3%81%8F%E3%81%A0%E3%81%95%E3%81%84%E3%80%82))。これによりデバッグ用の例外的な信頼設定が本番アプリに混入するのを防げます。iOSでもATSの例外や証明書を信頼する処理は、本番では無効になるようXcodeのビルドフラグやスキームで管理します。こうした工夫で、本番環境では常に正式なサーバー証明書のみを受け入れる状態を維持します。

- **ユーザー入力データの保護と認可**: 通信路の暗号化に加え、送信するデータ自体の安全性確保も重要です。例えばログイン認証情報やAPIトークンなどは必ずTLS上で送信し、可能であればさらにサーバー側で短寿命のセッションに置き換えるなど漏洩リスクを下げます。またサーバーからの応答についても改ざん検知のためにデジタル署名やHMACを使う設計も考えられます。ただしこれらは通信経路の保護というよりアプリケーションレベルの対策となりますので、本フェーズでは詳細は割愛します。

以上の基本対策により、アプリとサーバー間の通信における機密性・完全性・認証を担保します。しかし、開発の現場では証明書検証の実装ミスが起きやすく、それが深刻な脆弱性につながっている実態があります。次に、そのような**証明書検証の脆弱性**とそれを悪用した中間者攻撃（MITM攻撃）の具体例について解説します。

### 証明書検証の脆弱性と中間者（MITM）攻撃の例
サーバー証明書の検証不備はモバイルアプリにおける代表的な脆弱性の一つです。証明書を正しく検証していないアプリでは、攻撃者による**中間者攻撃（Man-in-the-Middle attack）**が成立してしまいます。中間者攻撃とは、通信の間に攻撃者が割り込み、クライアントとサーバー双方になりすまして機密情報を傍受・改ざんする攻撃です。

 ([
        Certificate Pinning iOS
      ](https://www.netguru.com/blog/certificate-pinning-in-ios)) *図1: クライアント（スマホアプリ）とサーバー間の通信に、攻撃者（中央）が不正に割り込んでいる中間者攻撃の模式図。攻撃者はクライアントにはサーバーを装った偽の証明書を提示し、サーバー側とは通常のTLS通信を成立させる。アプリが攻撃者の証明書を信頼してしまうと、暗号化された通信も攻撃者に解読されてしまい、結果としてユーザーの機密データが盗聴・改ざんされる ([安全でない X.509 TrustManager  |  Security  |  Android Developers](https://developer.android.com/privacy-and-security/risks/unsafe-trustmanager?hl=ja#:~:text=%E5%AE%89%E5%85%A8%E3%81%A7%E3%81%AA%E3%81%84%20,%E3%83%87%E3%83%BC%E3%82%BF%E3%81%8C%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF%E6%94%BB%E6%92%83%E8%80%85%E3%81%AB%EF%BC%88%E3%83%AA%E3%83%A2%E3%83%BC%E3%83%88%E3%81%BE%E3%81%9F%E3%81%AF%E3%83%AD%E3%83%BC%E3%82%AB%E3%83%AB%E3%81%A7%EF%BC%89%E4%BE%B5%E5%AE%B3%E3%81%95%E3%82%8C%E3%82%8B%E5%8F%AF%E8%83%BD%E6%80%A7%E3%81%8C%E3%81%82%E3%82%8A%E3%81%BE%E3%81%99%E3%80%82%E3%81%9D%E3%81%AE%E5%BD%B1%E9%9F%BF%E3%81%AF%E3%80%81%E6%84%8F%E5%9B%B3%E3%81%9B%E3%81%9A%E5%85%AC%E9%96%8B%E3%81%95%E3%82%8C%E3%81%A6%E3%81%97%E3%81%BE%E3%81%86%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF%20%E3%83%88%E3%83%A9%E3%83%95%E3%82%A3%E3%83%83%E3%82%AF%E3%81%AE%E5%86%85%E5%AE%B9%EF%BC%88%E5%80%8B%E4%BA%BA%E6%83%85%E5%A0%B1%E3%80%81%E9%9D%9E%E5%85%AC%E9%96%8B%E6%83%85%E5%A0%B1%E3%80%81%E6%A9%9F%E5%AF%86%E6%80%A7%E3%81%AE%E9%AB%98%E3%81%84%E3%82%BB%E3%83%83%E3%82%B7%E3%83%A7%E3%83%B3%E5%80%A4%E3%80%81%E3%82%B5%E3%83%BC%E3%83%93%E3%82%B9%E8%AA%8D%E8%A8%BC%E6%83%85%E5%A0%B1%E3%81%AA%E3%81%A9%EF%BC%89%E3%81%AB%E3%82%88%E3%81%A3%E3%81%A6%E7%95%B0%E3%81%AA%E3%82%8A%E3%81%BE%E3%81%99%E3%80%82))。*

証明書検証の不備によってこのような攻撃が現実に発生し得ます。例えば、開発者が誤って「すべての証明書を信頼する」実装を残してしまったアプリでは、攻撃者は自分の用意した不正なサーバー証明書を使ってTLSハンドシェイクを完了させることができます。クライアント（アプリ）は本来信頼されないはずの証明書を受け入れてしまうため、攻撃者は通信を傍受できるようになります。攻撃者はターゲットユーザーを自分の管理するWi-Fiアクセスポイントに誘導し、中間に配置したプロキシで通信を盗聴・改ざんします。実際に**オンラインバンキング**のアプリがこの手口で狙われたケースもあり、攻撃者が偽の無線LAN環境を用意して被害者を接続させ、中間者攻撃により暗号化通信を復号してログイン情報を窃取したり、送金先を書き換えるといった犯行が報告されています ([不正なSSL証明書で中間者攻撃の恐れ。モバイルアプリも注意が必要](https://product.sct.co.jp/blog/security/fear-of-man-in-the-middle-attacks-with-rogue-ssl-certificates#:~:text=%E4%B8%AD%E9%96%93%E8%80%85%E6%94%BB%E6%92%83%E3%81%AF%E4%B8%8D%E6%AD%A3%E3%81%AA%E8%A8%BC%E6%98%8E%E6%9B%B8%E3%81%A0%E3%81%91%E3%81%A7%E3%81%AF%E5%AE%9F%E8%A1%8C%E3%81%A7%E3%81%8D%E3%81%AA%E3%81%84%E3%82%82%E3%81%AE%E3%81%AE%E3%80%81%E4%BE%8B%E3%81%88%E3%81%B0%E4%B8%8D%E6%AD%A3%E3%81%AA%E7%84%A1%E7%B7%9ALAN%E3%82%92%E8%A8%AD%E5%AE%9A%E3%81%99%E3%82%8B%E3%81%AA%E3%81%A9%E3%81%AE%E6%89%8B%E5%8F%A3%E3%82%92%E7%B5%84%E3%81%BF%E5%90%88%E3%82%8F%E3%81%9B%E3%82%8C%E3%81%B0%E3%80%81%E3%82%AA%E3%83%B3%E3%83%A9%E3%82%A4%E3%83%B3%E3%83%90%E3%83%B3%E3%82%AD%E3%83%B3%E3%82%B0%E3%81%AE%E3%83%88%E3%83%A9%E3%83%95%E3%82%A3%E3%83%83%E3%82%AF%E3%81%AB%E4%BB%8B%E5%85%A5%E3%81%97%E3%81%A6%E9%80%9A%E4%BF%A1%20%E3%81%AE%E6%9A%97%E5%8F%B7%E3%82%92%E8%A7%A3%E9%99%A4%E3%81%97%E3%80%81%E3%82%B5%E3%82%A4%E3%83%B3%E3%82%AA%E3%83%B3%E6%83%85%E5%A0%B1%E3%82%92%E7%9B%97%E3%82%93%E3%81%A0%E3%82%8A%E3%80%81%E9%87%91%E9%A1%8D%E3%82%84%E6%8C%AF%E8%BE%BC%E5%85%88%E3%82%92%E6%93%8D%E4%BD%9C%E3%81%99%E3%82%8B%E3%81%93%E3%81%A8%E3%81%8C%E3%81%A7%E3%81%8D%E3%81%A6%E3%81%97%E3%81%BE%E3%81%86%E6%81%90%E3%82%8C%E3%82%82%E3%81%82%E3%82%8B%E3%81%A8Netcraft%E3%81%AF%E6%8C%87%E6%91%98%E3%81%97%E3%81%A6%E3%81%84%E3%81%BE%E3%81%99%E3%80%82))。

この問題の深刻さは複数の調査でも裏付けられています。2014年にFireEye社が行った調査では、Google Play上位1000件のAndroidアプリのうち73%がサーバー証明書を**まったく検証せずに**通信を行っており、無作為に選んだ1万件のアプリ中でも約40%が証明書未検証だったと報告されています ([SSL Vulnerabilities in Your Mobile Apps](https://cloudsecurityalliance.org/articles/ssl-vulnerabilities-in-your-mobile-apps-what-could-possibly-go-wrong#:~:text=number%20of%20the%20apps%20are,their%20servers%20to%20potential%20theft))。その後も状況は大きく改善せず、2023年に公表されたIOActive等の調査では**金融機関のモバイルバンキングアプリ**の約40%（iOS）、41%（Android）にサーバー証明書の検証不備の脆弱性が見つかったとされています ([不正なSSL証明書で中間者攻撃の恐れ。モバイルアプリも注意が必要](https://product.sct.co.jp/blog/security/fear-of-man-in-the-middle-attacks-with-rogue-ssl-certificates#:~:text=%E5%AE%9F%E9%9A%9B%E3%80%81IO%20Active%E3%82%84%E5%AD%A6%E8%A1%93%E6%A9%9F%E9%96%A2%E3%81%8C%E8%A1%8C%E3%81%A3%E3%81%9F%E8%AA%BF%E6%9F%BB%E3%81%A7%E3%81%AF%E3%80%81iOS%E5%90%91%E3%81%91%E3%81%AE%E3%83%90%E3%83%B3%E3%82%AD%E3%83%B3%E3%82%B0%E3%82%A2%E3%83%97%E3%83%AA%E3%81%AE40%EF%BC%85%E3%80%81Android%E3%82%A2%E3%83%97%E3%83%AA%E3%81%AE41%EF%BC%85%E3%81%A7%E3%80%81SSL%E8%A8%BC%E6%98%8E%E6%9B%B8%E3%81%AE%E8%AA%8D%E8%A8%BC%E3%81%AB%E4%B8%8D%E5%82%99%E3%81%8C%E3%81%82%E3%82%8B%E3%81%A8%E3%81%84%E3%81%86%E7%B5%90%20%E6%9E%9C%E3%82%82%E5%87%BA%E3%81%A6%E3%81%84%E3%82%8B%E3%81%9D%E3%81%86%E3%81%A7%E3%81%99%E3%80%82))。つまり相当数のモバイルアプリが、本来なら検知できるはずの不正な証明書を受け入れてしまう状態にあり、実際に中間者攻撃に利用され得るのです ([不正なSSL証明書で中間者攻撃の恐れ。モバイルアプリも注意が必要](https://product.sct.co.jp/blog/security/fear-of-man-in-the-middle-attacks-with-rogue-ssl-certificates#:~:text=%E3%82%A4%E3%83%B3%E3%82%BF%E3%83%BC%E3%83%8D%E3%83%83%E3%83%88%E3%82%B5%E3%83%BC%E3%83%93%E3%82%B9%E4%BA%8B%E6%A5%AD%E8%80%85%E3%81%AENetcraft%E3%81%AF%E3%80%81%E3%82%AA%E3%83%B3%E3%83%A9%E3%82%A4%E3%83%B3%E3%83%90%E3%83%B3%E3%82%AD%E3%83%B3%E3%82%B0%E3%82%84%E9%9B%BB%E5%AD%90%E5%95%86%E5%8F%96%E5%BC%95%E3%80%81%E3%82%BD%E3%83%BC%E3%82%B7%E3%83%A3%E3%83%AB%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AD%E3%83%B3%E3%82%B0%E3%81%AA%E3%81%A9%E3%81%AEWeb%E3%82%B5%E3%82%A4%E3%83%88%E3%82%92%E6%A8%99%E7%9A%84%E3%81%A8%E3%81%97%E3%81%9F%E4%B8%8D%E6%AD%A3%E3%81%AASSL%E8%A8%BC%E6%98%8E%E6%9B%B8%E3%81%8C%20%E3%82%A4%E3%83%B3%E3%82%BF%E3%83%BC%E3%83%8D%E3%83%83%E3%83%88%E4%B8%8A%E3%81%AB%E5%A4%9A%E6%95%B0%E5%AD%98%E5%9C%A8%E3%81%97%E3%81%A6%E3%81%84%E3%82%8B%E3%81%93%E3%81%A8%E3%81%8C%E5%88%86%E3%81%8B%E3%81%A3%E3%81%9F%E3%81%A8%E7%99%BA%E8%A1%A8%E3%81%97%E3%81%BE%E3%81%97%E3%81%9F%E3%80%82%E3%83%A2%E3%83%90%E3%82%A4%E3%83%AB%E3%82%A2%E3%83%97%E3%83%AA%E3%81%A7%E3%81%AFSSL%E8%A8%BC%E6%98%8E%E6%9B%B8%E3%81%AE%E3%83%81%E3%82%A7%E3%83%83%E3%82%AF%E3%81%8C%E9%81%A9%E5%88%87%E3%81%AB%E8%A1%8C%E3%82%8F%E3%82%8C%E3%81%AA%E3%81%84%E3%82%B1%E3%83%BC%E3%82%B9%E3%82%82%E5%A4%9A%E3%81%8F%E3%80%81%E9%80%9A%E4%BF%A1%E3%81%AB%E5%89%B2%E3%82%8A%E8%BE%BC%E3%82%80%E3%80%8C%E4%B8%AD%E9%96%93%E8%80%85%E6%94%BB%20%E6%92%83%E3%80%8D%E3%81%AB%E5%88%A9%E7%94%A8%E3%81%95%E3%82%8C%E3%82%8B%E6%81%90%E3%82%8C%E3%81%8C%E3%81%82%E3%82%8B%E3%81%A8%E8%AD%A6%E5%91%8A%E3%81%97%E3%81%A6%E3%81%84%E3%81%BE%E3%81%99%E3%80%82))。

不適切な証明書検証による脆弱性が悪用されると、ユーザーの送信する個人情報、認証情報、セッションIDなどあらゆる重要データが攻撃者に筒抜けとなる危険があります ([安全でない X.509 TrustManager  |  Security  |  Android Developers](https://developer.android.com/privacy-and-security/risks/unsafe-trustmanager?hl=ja#:~:text=%E5%AE%89%E5%85%A8%E3%81%A7%E3%81%AA%E3%81%84%20,%E3%83%87%E3%83%BC%E3%82%BF%E3%81%8C%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF%E6%94%BB%E6%92%83%E8%80%85%E3%81%AB%EF%BC%88%E3%83%AA%E3%83%A2%E3%83%BC%E3%83%88%E3%81%BE%E3%81%9F%E3%81%AF%E3%83%AD%E3%83%BC%E3%82%AB%E3%83%AB%E3%81%A7%EF%BC%89%E4%BE%B5%E5%AE%B3%E3%81%95%E3%82%8C%E3%82%8B%E5%8F%AF%E8%83%BD%E6%80%A7%E3%81%8C%E3%81%82%E3%82%8A%E3%81%BE%E3%81%99%E3%80%82%E3%81%9D%E3%81%AE%E5%BD%B1%E9%9F%BF%E3%81%AF%E3%80%81%E6%84%8F%E5%9B%B3%E3%81%9B%E3%81%9A%E5%85%AC%E9%96%8B%E3%81%95%E3%82%8C%E3%81%A6%E3%81%97%E3%81%BE%E3%81%86%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF%20%E3%83%88%E3%83%A9%E3%83%95%E3%82%A3%E3%83%83%E3%82%AF%E3%81%AE%E5%86%85%E5%AE%B9%EF%BC%88%E5%80%8B%E4%BA%BA%E6%83%85%E5%A0%B1%E3%80%81%E9%9D%9E%E5%85%AC%E9%96%8B%E6%83%85%E5%A0%B1%E3%80%81%E6%A9%9F%E5%AF%86%E6%80%A7%E3%81%AE%E9%AB%98%E3%81%84%E3%82%BB%E3%83%83%E3%82%B7%E3%83%A7%E3%83%B3%E5%80%A4%E3%80%81%E3%82%B5%E3%83%BC%E3%83%93%E3%82%B9%E8%AA%8D%E8%A8%BC%E6%83%85%E5%A0%B1%E3%81%AA%E3%81%A9%EF%BC%89%E3%81%AB%E3%82%88%E3%81%A3%E3%81%A6%E7%95%B0%E3%81%AA%E3%82%8A%E3%81%BE%E3%81%99%E3%80%82))。特にモバイルアプリは前述のようにユーザーに警告が表示されないため、ユーザーが攻撃に気づかないまま被害が進行する恐れがあります。この種の脆弱性は「サーバ証明書の検証不備」などと呼ばれ、OWASP Mobile Top 10でも通信の不備（M3: Insecure Communicationなど）として常に取り上げられる重要項目となっています。

以上、フェーズ5ではモバイルアプリの通信セキュリティ上の課題と基本対策、そして証明書検証を怠った場合に生じる脆弱性と攻撃例について説明しました。総じて言えば、**「通信の暗号化」と「正しい証明書検証」**がモバイルアプリ通信のセキュリティ確保には不可欠です。しかし実際には暗号化（TLS）を使っていても検証が甘いケースが多々あり、それを根本的に防ぐための手段の一つが**SSLピンニング**です。次のフェーズ6では、このSSLピンニングについて詳細に解説します。

## フェーズ6: SSLピンニング

### SSLピンニングの目的と通常の証明書検証との違い
**SSLピンニング（証明書ピンニング）**とは、サーバー証明書の検証方法を強化するために、特定の証明書または公開鍵をクライアントアプリ側に「固定」（ピン留め）しておく技術です。通常、クライアント（アプリ）はOSにあらかじめインストールされた多数の認証局(CA)の中から一つでも有効なチェーンが見つかればサーバーを信頼します。しかしこの方法では、万が一信頼されたCA自体が侵害された場合や、ユーザー端末に悪意のあるCA証明書がインストールされてしまった場合に、攻撃者がそのCAから不正な証明書を発行しても通信が成立してしまいます ([3 Immediate Actions to Protect Mobile Apps from Man-in-the-Middle Attacks](https://approov.io/blog/three-actions-you-should-take-right-now-to-stop-mobile-mitm-attacks#:~:text=Unfortunately%20%2C%20if%20an%20attacker,devices%2C%20this%20threat%20is%20real))。実際、モバイル環境では企業や利用者が端末に独自CAを追加するケースもあり、攻撃者が物理的/マルウェア的手段で端末の証明書ストアを書き換えることも現実的な脅威です ([3 Immediate Actions to Protect Mobile Apps from Man-in-the-Middle Attacks](https://approov.io/blog/three-actions-you-should-take-right-now-to-stop-mobile-mitm-attacks#:~:text=Unfortunately%20%2C%20if%20an%20attacker,devices%2C%20this%20threat%20is%20real))。SSLピンニングはこのリスクに対処するため、**アプリが信頼する証明書を開発者が指定したものに限定**し、想定外の証明書ではたとえOS的には信頼されていても接続を拒否します。

通常の証明書検証では「OSが信頼するどの認証局によって署名された証明書でも許容する」のに対し、ピンニングを導入した場合、「**あらかじめアプリに組み込まれた特定の証明書（あるいは鍵）と一致するものしか信頼しない**」という追加条件が課されます ([Certificate Pinning | CyberArk](https://venafi.com/machine-identity-basics/what-is-certificate-pinning/#:~:text=Certificate%20pinning%20is%20a%20cybersecurity,the%20risk%20of%20an%20attack)) ([3 Immediate Actions to Protect Mobile Apps from Man-in-the-Middle Attacks](https://approov.io/blog/three-actions-you-should-take-right-now-to-stop-mobile-mitm-attacks#:~:text=Certificate%20pinning%20replaces%20dependence%20on,is%20known%20as%20static%20pinning))。これにより、たとえ攻撃者がデバイスの信頼リストを書き換えたり不正な証明書を入手・呈示したりしても、アプリ内にピン留めされた証明書と一致しないため接続は成立しません ([Certificate Pinning | CyberArk](https://venafi.com/machine-identity-basics/what-is-certificate-pinning/#:~:text=With%20cyber%20threats%20constantly%20evolving%2C,doesn%E2%80%99t%20match%20the%20pinned%20certificate))。極端に言えば、攻撃者がルートCAを完全に乗っ取ったとしても、そのCAから発行された証明書はピンニングチェックで弾かれるため通信を乗っ取れないことになります ([Certificate Pinning | CyberArk](https://venafi.com/machine-identity-basics/what-is-certificate-pinning/#:~:text=In%20a%20typical%20certificate,doesn%E2%80%99t%20match%20the%20pinned%20certificate))。このようにSSLピンニングは中間者攻撃に対する強力な防御策となり、金融・医療など敏感なデータを扱うアプリでは特に有効とされています ([Certificate Pinning | CyberArk](https://venafi.com/machine-identity-basics/what-is-certificate-pinning/#:~:text=,the%20sensitive%20information%20being%20transmitted))。OWASPでもモバイルアプリの通信防御策として証明書ピンニングの実装を推奨しており ([3 Immediate Actions to Protect Mobile Apps from Man-in-the-Middle Attacks](https://approov.io/blog/three-actions-you-should-take-right-now-to-stop-mobile-mitm-attacks#:~:text=Certificate%20pinning%20replaces%20dependence%20on,is%20known%20as%20static%20pinning))、近年では一般的なセキュリティ強化手段の一つとなっています。

ただし、SSLピンニングを導入すると**証明書の更新管理**が必要になる点に注意が必要です。ピン留めする証明書や鍵は固定されるため、サーバー側で証明書を更新・変更した際にはアプリ側も対応してアップデートしなければ通信が切れてしまいます ([3 Immediate Actions to Protect Mobile Apps from Man-in-the-Middle Attacks](https://approov.io/blog/three-actions-you-should-take-right-now-to-stop-mobile-mitm-attacks#:~:text=approach%20is%20recommended%20by%20OWASP,is%20known%20as%20static%20pinning))。この問題と、具体的なピンニングの手法については次で詳しく説明します。

### ピンニングの種類と仕組み
SSLピンニングにはいくつかの実装方法（種類）があり、それぞれ特徴があります ([Certificate Pinning & Public Key Pinning](https://www.vaadata.com/blog/certificate-and-public-key-pinning/#:~:text=Certificate%20Pinning%2C%20Key%20Pinning%20and,Hash))。以下では主要な3種類のピンニング手法「証明書ピンニング」「公開鍵ピンニング」「ハッシュピンニング」について、その違いと利点・欠点を解説します。

- **証明書ピンニング**: サーバーのSSLサーバー証明書そのものをアプリに組み込み、接続時にサーバーから提示された証明書と**バイトレベルで照合**する方法です。例えばあらかじめ信頼するサーバー証明書（または中間CA証明書）のDER形式ファイルをアプリ内に保存し、通信時にサーバーの証明書と一致するか比較します。一致しない場合は通信を拒否することで、想定外の証明書を排除します ([Certificate Pinning & Public Key Pinning](https://www.vaadata.com/blog/certificate-and-public-key-pinning/#:~:text=Certificate%20Pinning))。この方式は実装が比較的簡単であり、特にモバイルアプリでは開発者が証明書ファイルをアプリに含めやすいため採用例が多いです ([Certificate Pinning & Public Key Pinning](https://www.vaadata.com/blog/certificate-and-public-key-pinning/#:~:text=The%20use%20of%20certificate%20pinning,to%20include%20the%20expected%20certificate))。一方で**証明書自体**にピン留めしているため、その証明書が有効期限切れやサーバー側の都合で差し替えになった場合にアプリも更新しないと新しい証明書を受け入れられない欠点があります ([Certificate Pinning & Public Key Pinning](https://www.vaadata.com/blog/certificate-and-public-key-pinning/#:~:text=mobile%20app%2C%20as%20it%20is,to%20include%20the%20expected%20certificate))。証明書の有効期限は通常1～2年程度なので、そのたびにアプリのアップデートが必要になる点は運用上の負担です。

- **公開鍵ピンニング**: 証明書ではなく、その中に含まれる**公開鍵**（正確にはSubject Public Key Info）をピン留めする方法です ([Certificate Pinning & Public Key Pinning](https://www.vaadata.com/blog/certificate-and-public-key-pinning/#:~:text=Public%20Key%20Pinning))。アプリにサーバー証明書の公開鍵情報（またはそのハッシュ）を保持しておき、サーバーから提示された証明書から抽出した公開鍵と比較します。一致すればその証明書は発行元や有効期限に関係なく受け入れます。公開鍵ピンニングでは証明書全体ではなく鍵だけを見るため、仮に証明書が失効・更新され別の証明書に変わっても**同じ公開鍵を使って新しい証明書を発行すればアプリ側の更新なしに通信を維持可能**というメリットがあります ([
        Certificate Pinning iOS
      ](https://www.netguru.com/blog/certificate-pinning-in-ios#:~:text=certificate))。例えば有効期限が近づいた際、サーバー側で新しい証明書を旧証明書と同じ鍵ペアで発行すれば、アプリの公開鍵ピンニングはそのまま通用します。ただし公開鍵を長期間使い回すことになるため、セキュリティポリシー上の鍵ローテーション（定期的な鍵対の再生成）がしにくくなる点に留意が必要です ([
        Certificate Pinning iOS
      ](https://www.netguru.com/blog/certificate-pinning-in-ios#:~:text=certificate))。また、万一サーバーの秘密鍵が漏洩した場合にはピン留めを意味なく突破されてしまう（攻撃者がその鍵でサーバーになりすませる）ため、秘密鍵の厳重管理が前提となります。

- **ハッシュピンニング**: 証明書や公開鍵そのものではなく、それらの**ハッシュ値**（フィンガープリント）をアプリに保持し、接続時にサーバー側から得た証明書あるいは鍵のハッシュ値と比較する方法です ([Certificate Pinning & Public Key Pinning](https://www.vaadata.com/blog/certificate-and-public-key-pinning/#:~:text=Hashing))。ハッシュ値（例えばSHA-256）を用いることで、アプリに組み込むデータ量を小さく抑えられ、ピン留め対象の情報（証明書や鍵そのもの）を直接アプリ内に置かずに済む利点があります ([Certificate Pinning & Public Key Pinning](https://www.vaadata.com/blog/certificate-and-public-key-pinning/#:~:text=,libraries%20provide%20digital%20fingerprint%20certificate))。また証明書の指紋（ダイジェスト）は多くのSSL/TLSライブラリで取得関数が提供されており、実装も容易です ([Certificate Pinning & Public Key Pinning](https://www.vaadata.com/blog/certificate-and-public-key-pinning/#:~:text=,libraries%20provide%20digital%20fingerprint%20certificate))。ハッシュピンニング自体は「何をハッシュ化するか」によって実質的に証明書ピンニングにも公開鍵ピンニングにもなり得ます。例えば証明書全体をハッシュ化して比較すれば証明書ピンニングと同等であり、公開鍵情報（SPKI）をハッシュ化すれば公開鍵ピンニングと同等です。したがってハッシュピンニングは実装上の選択肢であり、運用面の特性はハッシュ化する対象に依存します。いずれにせよ、ハッシュを用いることでアプリに埋め込むピン情報が匿名化され直接には判別しづらくなるという付加的メリットがあります ([Certificate Pinning & Public Key Pinning](https://www.vaadata.com/blog/certificate-and-public-key-pinning/#:~:text=,libraries%20provide%20digital%20fingerprint%20certificate))（もっとも、強力なハッシュ関数を使えば衝突しない限り元の証明書や鍵を推測することは現実的に不可能です）。

以上のように、ピンニングには方式ごとの特徴があります。一般的には、**公開鍵ピンニング**が証明書更新によるアプリ改修頻度を下げられるため実用上バランスが良いとされています ([
        Certificate Pinning iOS
      ](https://www.netguru.com/blog/certificate-pinning-in-ios#:~:text=certificate))。ただし証明書更新の頻度が低く常に同じCAを利用する場合などは証明書ピンニングでも問題にならないこともあります。また実運用では、万一に備えて**複数のピンを用意する（バックアップピン）**ことが推奨されます ([Network security configuration  |  Security  |  Android Developers](https://developer.android.com/privacy-and-security/security-config#:~:text=Note%20that%2C%20when%20using%20certificate,the%20app%20to%20restore%20connectivity))。例えば現在使用中の公開鍵に加え、将来更新時に使う予定の公開鍵のハッシュもあらかじめアプリに登録しておくことで、一つのピンが使えなくなってももう一方で通信を維持できます。次節では、AndroidおよびiOSそれぞれのプラットフォームでSSLピンニングを実装する方法について、具体例を示します。

### Androidにおけるピンニング実装方法
AndroidアプリでSSLピンニングを実装する方法としては、大きく「Network Security Configurationによる設定」と「コード上でのピンニング実装」があります。

**1. Network Security Configurationを使用する方法**: Android 7.0以降では、アプリのリソースにXML形式でネットワークセキュリティポリシーを定義し、ドメインごとの証明書信頼ルールを設定できます。その中で`<pin-set>`を使って証明書（の公開鍵ハッシュ）をピン留めすることが可能です ([Network security configuration  |  Security  |  Android Developers](https://developer.android.com/privacy-and-security/security-config#:~:text=Certificate%20pinning%20is%20done%20by,of%20the%20pinned%20public%20keys))。この方法ではコードを書かずにピンニングを導入でき、テスト時と本番時の設定切り替えも容易なため推奨されています。以下にNetwork Security Configurationの例を示します（`res/xml/network_security_config.xml`に配置）。この例では`example.com`ドメインに対してピンニングを適用し、SHA-256ハッシュ値で指定した2つの公開鍵を信頼しています（1つはバックアップピン） ([Network security configuration  |  Security  |  Android Developers](https://developer.android.com/privacy-and-security/security-config#:~:text=%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22utf,256%22%3Efwza0LRMXouZHRC8Ei%2B4PyuldPDcf3UKgO%2F04cDM1oE%3D%3C%2Fpin))。

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config>
        <domain includeSubdomains="true">example.com</domain>
        <pin-set expiration="2025-01-01">
            <pin digest="SHA-256">7HIpactkIAq2Y49orFOOQKurWxmmSFZhBCoQYcRhJ3Y=</pin>
            <!-- backup pin -->
            <pin digest="SHA-256">fwza0LRMXouZHRC8Ei+4PyuldPDcf3UKgO/04cDM1oE=</pin>
        </pin-set>
    </domain-config>
</network-security-config>
```

上記では`example.com`およびそのサブドメインに対し、有効期限2025年1月1日までの間、指定したSHA-256ハッシュの公開鍵を持つ証明書以外は受け付けない設定です。ハッシュ値は証明書のSubject Public Key Info（公開鍵情報）から算出した値です ([Network security configuration  |  Security  |  Android Developers](https://developer.android.com/privacy-and-security/security-config#:~:text=Certificate%20pinning%20is%20done%20by,of%20the%20pinned%20public%20keys))。このようにXMLにピンを記述しておけば、Androidプラットフォームが自動的に証明書検証時にピンチェックを行ってくれます。ピンの有効期限（expiration）を設けることも可能で、これはアプリが長期間アップデートされなかった場合に通信遮断しっぱなしになるリスクを軽減します ([Network security configuration  |  Security  |  Android Developers](https://developer.android.com/privacy-and-security/security-config#:~:text=Additionally%2C%20it%20is%20possible%20to,to%20bypass%20your%20pinned%20certificates))（期限後は通常の証明書検証にフォールバック）が、攻撃者が期限切れを狙って待つ可能性もあるため設定は慎重に検討すべきです ([Network security configuration  |  Security  |  Android Developers](https://developer.android.com/privacy-and-security/security-config#:~:text=Additionally%2C%20it%20is%20possible%20to,to%20bypass%20your%20pinned%20certificates))。

Network Security Configurationを用いることで、テスト用ビルドではピンニングを無効化する・本番では有効にするといった柔軟な運用もできます ([Network security configuration  |  Security  |  Android Developers](https://developer.android.com/privacy-and-security/security-config#:~:text=When%20debugging%20an%20app%20that,release%20builds))。例えば上記設定を本番用とし、デバッグビルドでは`debug-overrides`セクションで独自CAを信頼するようにすれば、開発中はピンニングを気にせず作業しつつ、本番では自動的にピンニングが有効になります。コードに手を入れない分、実装ミスも減らせる利点があります。

**2. コード上でピンニングを実装する方法**: ライブラリや独自コードで通信処理を行っている場合、コード内でサーバー証明書を検証する際にピンニングを組み込むこともできます。例えばOkHttpクライアントライブラリ（Androidで広く利用されています）には`CertificatePinner`という機能が用意されており、数行のコードで特定ドメインのピンニングを設定可能です。

```java
CertificatePinner pinner = new CertificatePinner.Builder()
    .add("example.com", "sha256/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX=")
    .build();
OkHttpClient client = new OkHttpClient.Builder()
    .certificatePinner(pinner)
    .build();
```

上記のように、ビルダーにドメイン名と許可する公開鍵（SPKI）のSHA-256ハッシュ値を登録し、HTTPクライアントに設定します。以後、この`client`を使用した`example.com`へのHTTPS通信では、証明書チェーン内にピン留めした公開鍵が含まれていない場合に接続エラーとなります。OkHttp内部で証明書チェーン中の各証明書から公開鍵を抽出しハッシュ値と照合してくれるため、開発者はハッシュ値をコードに書くだけで済みます。

OkHttp以外でも、例えば独自に`X509TrustManager`を実装して`checkServerTrusted`内で証明書や公開鍵を比較する方法もあります。しかし前述の通り実装を誤るリスクが高いため、可能な限り標準のNetwork Security Configurationや実績のあるライブラリの機能を使う方が安全です。また、複数のピンを許容したい場合（バックアップピンの利用など）も上記のような方法で容易に実現できます ([Network security configuration  |  Security  |  Android Developers](https://developer.android.com/privacy-and-security/security-config#:~:text=%3Cpin%20digest%3D%22SHA,config))。

### iOSにおけるピンニング実装方法
iOSアプリでは、Androidのような専用設定ファイルはないため、コード上でピンニングを実装します。一般的な方法は**通信APIのデリゲートを利用する**ものです。iOSの`URLSession`を使った通信では、サーバーから証明書を受け取った際に`URLSessionDelegate`のメソッド`urlSession(_:didReceive:completionHandler:)`が呼ばれるので、ここでサーバー証明書を取得してアプリに埋め込んだピンと照合します。以下にSwiftでの実装例を示します。

```swift
class PinningURLSessionDelegate: NSObject, URLSessionDelegate {
    func urlSession(_ session: URLSession, 
                    didReceive challenge: URLAuthenticationChallenge, 
                    completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
        // サーバー証明書の検証要求に対処
        if challenge.protectionSpace.authenticationMethod == NSURLAuthenticationMethodServerTrust,
           let serverTrust = challenge.protectionSpace.serverTrust {
            // OS標準の証明書検証を実施（失敗したら以降進まない）
            if SecTrustEvaluateWithError(serverTrust, nil) {
                // チェーン中の一番目（サーバー証明書）を取得
                if let serverCert = SecTrustGetCertificateAtIndex(serverTrust, 0) {
                    let serverCertData = SecCertificateCopyData(serverCert) as Data
                    // アプリに埋め込んだサーバー証明書（例: server.cer）をロード
                    if let localCertPath = Bundle.main.path(forResource: "server", ofType: "cer"),
                       let localCertData = try? Data(contentsOf: URL(fileURLWithPath: localCertPath)) {
                        // 証明書ピンニングチェック: バイト列が一致すればOK
                        if serverCertData == localCertData {
                            completionHandler(.useCredential, URLCredential(trust: serverTrust))
                            return  // 検証成功、通信続行
                        }
                    }
                }
            }
        }
        // ピンに一致しない場合は接続拒否
        completionHandler(.cancelAuthenticationChallenge, nil)
    }
}
```

まず`SecTrustEvaluateWithError`によりAppleの標準的な証明書検証（チェーン検証や有効期限チェック）を行っています ([iOS certificate pinning with Swift and NSURLSession - Stack Overflow](https://stackoverflow.com/questions/34223291/ios-certificate-pinning-with-swift-and-nsurlsession#:~:text=if%20let%20serverTrust%20%3D%20challenge,serverTrust%2C%20nil))。この段階で不正な証明書であれば通常は失敗しますが、例えばユーザーが端末に独自CAをインストールしている場合などはここも通過してしまう可能性があります。しかしピンニング実装では次に進み、サーバー証明書データ`serverCertData`を取得して、予めアプリにバンドルされた正規証明書`localCertData`と比較します。ここがピンニングの核心部分で、一致した場合のみ`.useCredential`で信頼して通信を続行し、一致しなければチャレンジをキャンセルして接続を切断します。 ([iOS certificate pinning with Swift and NSURLSession - Stack Overflow](https://stackoverflow.com/questions/34223291/ios-certificate-pinning-with-swift-and-nsurlsession#:~:text=if%20let%20file%20%3D%20file_der,isEqual%28to%3A%20cert2%20as%20Data%29))

上記は**証明書ピンニング**の例ですが、公開鍵ピンニングをする場合も流れは同様です。違いは、ローカルに保存するピン情報として証明書ではなく公開鍵そのものやそのハッシュ値を保存し、サーバー証明書から`SecCertificateCopyKey`等で取得した`SecKey`（公開鍵）と比較する点です。例えば公開鍵のSHA-256ハッシュをハードコーディングしておき、`SecKey`から得たデータをハッシュ計算して比較する、といった実装になります。いずれにせよ、低レベルにはなりますがAppleのSecurityフレームワークで証明書や鍵を操作する機能を使って実現できます。

なお、Alamofireなどの高水準のネットワーキングライブラリも内部でピンニングに対応しており、サーバートラストポリシーを設定することで同様の効果が得られます ([SSL Pinning in iOS Swift Edition | Infinum](https://infinum.com/blog/ssl-pinning-revisited/#:~:text=let%20evaluators%3A%20,PublicKeysTrustEvaluator%28%29))。小規模なアプリであれば自前で実装しても良いですが、ライブラリの既存機能を利用すればコード量を減らせます。たとえばAlamofire 5では`ServerTrustManager`にドメインごとのピンningポリシー（証明書または公開鍵）を指定可能であり、ピンの追加や更新も集中管理できます ([SSL Pinning in iOS Swift Edition | Infinum](https://infinum.com/blog/ssl-pinning-revisited/#:~:text=let%20evaluators%3A%20,PublicKeysTrustEvaluator%28%29))。

**複数証明書・鍵へのピンニング**: iOSで複数のピン（バックアップピンなど）を扱う場合は、上記コードを拡張して**いずれか一つでも一致すればOK**とするロジックにします。例えばピン情報を配列で持ち、ループで比較して一つでもマッチしたら`useCredential`を返す、といった形です。公開鍵ハッシュ値を複数持つ場合は、TrustKitというOSSライブラリを使って簡単に設定することもできます ([
        Certificate Pinning iOS
      ](https://www.netguru.com/blog/certificate-pinning-in-ios#:~:text=kTSKPublicKeyHashes%3A%20%5B%20)) ([
        Certificate Pinning iOS
      ](https://www.netguru.com/blog/certificate-pinning-in-ios#:~:text=2,representation%20of%20the%20public%20key))。TrustKitではあらかじめ用意した辞書にホスト名と許容する公開鍵ハッシュ値（`kTSKPublicKeyHashes`）を登録しておくだけで、証明書検証時に自動的にピンニングチェックをしてくれます ([
        Certificate Pinning iOS
      ](https://www.netguru.com/blog/certificate-pinning-in-ios#:~:text=kTSKPublicKeyHashes%3A%20%5B%20))。社内向けアプリなどで独自に実装するコストが見合わない場合、このようなライブラリの利用も検討されます。

### ピンニング導入時の留意事項と発展的トピック
SSLピンニングは強力なセキュリティ強化手段ですが、その導入・運用にあたっていくつか留意点があります。

- **証明書更新への対応**: 繰り返しになりますが、ピン留めした証明書や鍵が変更になる際はタイミングに注意が必要です。サーバー証明書の更新前にアプリ側アップデートを配信し、新しいピンを含めておかなければ、一度でもピンと異なる証明書が提示された時点で通信が切断されてしまいます ([Certificate Pinning & Public Key Pinning](https://www.vaadata.com/blog/certificate-and-public-key-pinning/#:~:text=mobile%20app%2C%20as%20it%20is,to%20include%20the%20expected%20certificate))。最悪の場合、ユーザーがアプリをアップデートせず古いピンのままだと、新しい証明書を使ったサーバーに繋がらなくなります。この問題に対処するため、**バックアップピン**の実装（前述）や、ピンに有効期限を設ける運用が取られます ([Network security configuration  |  Security  |  Android Developers](https://developer.android.com/privacy-and-security/security-config#:~:text=Note%20that%2C%20when%20using%20certificate,the%20app%20to%20restore%20connectivity))。ただし有効期限を過ぎたらピンニングを無効化するというのは本末転倒になりかねないため、基本は事前にアプリを更新してもらうよう周知することが望ましいです。

- **動的ピンニング**: 一部の高度な手法として、アプリリリース後にピン情報を遠隔配信で更新できる**動的ピンニング**があります。これはアプリと別に安全なチャネルを用意し、新しいピン（証明書やハッシュ）をアプリにダウンロードさせて差し替える方式です ([3 Immediate Actions to Protect Mobile Apps from Man-in-the-Middle Attacks](https://approov.io/blog/three-actions-you-should-take-right-now-to-stop-mobile-mitm-attacks#:~:text=Dynamic%20pinning%20improves%20on%20this,change%2C%20which%20does%20unfortunately%20happen))。動的ピンニングを実装すれば証明書更新のたびにアプリ配布し直さなくても済み、サービス継続性の観点では有利です ([3 Immediate Actions to Protect Mobile Apps from Man-in-the-Middle Attacks](https://approov.io/blog/three-actions-you-should-take-right-now-to-stop-mobile-mitm-attacks#:~:text=Dynamic%20pinning%20improves%20on%20this,change%2C%20which%20does%20unfortunately%20happen))。しかしそのためにはピン配信自体の認証や安全性を確保する必要があり、実装も複雑になります。市販ソリューション（Approov等 ([3 Immediate Actions to Protect Mobile Apps from Man-in-the-Middle Attacks](https://approov.io/blog/three-actions-you-should-take-right-now-to-stop-mobile-mitm-attacks#:~:text=Dynamic%20pinning%20improves%20on%20this,change%2C%20which%20does%20unfortunately%20happen))）もありますが、大学院レベルでは概念だけ押さえておけば十分でしょう。

- **デバッグ・解析への対策**: SSLピンニングは攻撃者による中間者攻撃を防ぎますが、端末利用者（攻撃者）が**自分でアプリを改造できる場合**には回避される恐れがあります。例えば高度な攻撃者は、デバイスを脱獄して`SSLKillSwitch`（iOS向け）やFridaスクリプト（Android/iOS） ([Certificate Pinning & Public Key Pinning](https://www.vaadata.com/blog/certificate-and-public-key-pinning/#:~:text=The%20methods%20described%20above%20enable,possible%20to%20use%20Frida%20scripts))といったツールを使い、アプリのピンニングチェック部分を無効化してしまいます。これらのツールはアプリ内の証明書検証APIをフックして常に成功させるもので、ピンニング実装をも突破されてしまいます ([Certificate Pinning & Public Key Pinning](https://www.vaadata.com/blog/certificate-and-public-key-pinning/#:~:text=The%20methods%20described%20above%20enable,possible%20to%20use%20Frida%20scripts))。このような攻撃への対策として、アプリの改ざん検知やデバッグモード検知、root化検知などを組み合わせて不審な環境では動作を停止する、といった包括的なアプローチが必要になります。ピンニング自体も完全ではないことを念頭に置き、他のセキュリティ対策とも組み合わせて防御層を厚くすることが重要です。

以上、SSLピンニングの目的から実装方法、注意点までを解説しました。まとめると、**SSLピンニングとは「アプリが信頼するサーバーの証明書（または鍵）をあらかじめ固定しておくことで、想定外の証明書では通信しないようにする仕組み」**です ([
        Certificate Pinning iOS
      ](https://www.netguru.com/blog/certificate-pinning-in-ios#:~:text=More%20formal%20definition%3A))。適切に実装すれば、たとえデバイスの証明書ストアや認証局に異常が生じてもアプリ・サーバー間の通信を堅固に保護できます。一方で運用や実装に手間がかかるため、特に扱うデータの機密性が高いアプリで優先的に導入される傾向があります ([Certificate Pinning & Public Key Pinning](https://www.vaadata.com/blog/certificate-and-public-key-pinning/#:~:text=Implementation%20costs%20of%20these%20solutions,data%2C%20such%20as%20banking%20applications))。この解説資料が、モバイルアプリの安全な通信確立とSSLピンニングの理解に役立てば幸いです。

**参考文献・出典**: 本資料ではモバイルアプリの通信脆弱性に関する最新の調査結果 ([不正なSSL証明書で中間者攻撃の恐れ。モバイルアプリも注意が必要](https://product.sct.co.jp/blog/security/fear-of-man-in-the-middle-attacks-with-rogue-ssl-certificates#:~:text=%E5%AE%9F%E9%9A%9B%E3%80%81IO%20Active%E3%82%84%E5%AD%A6%E8%A1%93%E6%A9%9F%E9%96%A2%E3%81%8C%E8%A1%8C%E3%81%A3%E3%81%9F%E8%AA%BF%E6%9F%BB%E3%81%A7%E3%81%AF%E3%80%81iOS%E5%90%91%E3%81%91%E3%81%AE%E3%83%90%E3%83%B3%E3%82%AD%E3%83%B3%E3%82%B0%E3%82%A2%E3%83%97%E3%83%AA%E3%81%AE40%EF%BC%85%E3%80%81Android%E3%82%A2%E3%83%97%E3%83%AA%E3%81%AE41%EF%BC%85%E3%81%A7%E3%80%81SSL%E8%A8%BC%E6%98%8E%E6%9B%B8%E3%81%AE%E8%AA%8D%E8%A8%BC%E3%81%AB%E4%B8%8D%E5%82%99%E3%81%8C%E3%81%82%E3%82%8B%E3%81%A8%E3%81%84%E3%81%86%E7%B5%90%20%E6%9E%9C%E3%82%82%E5%87%BA%E3%81%A6%E3%81%84%E3%82%8B%E3%81%9D%E3%81%86%E3%81%A7%E3%81%99%E3%80%82)) ([SSL Vulnerabilities in Your Mobile Apps](https://cloudsecurityalliance.org/articles/ssl-vulnerabilities-in-your-mobile-apps-what-could-possibly-go-wrong#:~:text=number%20of%20the%20apps%20are,their%20servers%20to%20potential%20theft))、Android/iOSの公式ドキュメント ([安全でない X.509 TrustManager  |  Security  |  Android Developers](https://developer.android.com/privacy-and-security/risks/unsafe-trustmanager?hl=ja#:~:text=Android%20%E3%82%A2%E3%83%97%E3%83%AA%E3%81%AB%20)) ([Network security configuration  |  Security  |  Android Developers](https://developer.android.com/privacy-and-security/security-config#:~:text=Certificate%20pinning%20is%20done%20by,of%20the%20pinned%20public%20keys))、およびセキュリティベンダーによる解説記事 ([3 Immediate Actions to Protect Mobile Apps from Man-in-the-Middle Attacks](https://approov.io/blog/three-actions-you-should-take-right-now-to-stop-mobile-mitm-attacks#:~:text=Unfortunately%20%2C%20if%20an%20attacker,devices%2C%20this%20threat%20is%20real)) ([Certificate Pinning & Public Key Pinning](https://www.vaadata.com/blog/certificate-and-public-key-pinning/#:~:text=Certificate%20Pinning))などを参照しました。詳細は文中の各出典箇所をご参照ください。