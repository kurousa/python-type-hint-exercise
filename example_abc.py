from abc import ABC, abstractmethod

type Headers = dict[str, str]
type JsonObject = dict[str, object]


class HttpResponse(ABC):
    """HTTP レスポンスの契約を定義する抽象基底クラス"""

    @property
    @abstractmethod
    def status_code(self) -> int:
        """ステータスコードを返す（サブクラスで実装必須）"""
        ...

    @abstractmethod
    # 戻り値がobjectの理由は、HTTPクライアント層の責務として、どのような型が変えるかは知らなくてよいため
    # どうあるべきかは、呼び出し側でキャストすることで対応する
    def json(self) -> object:
        """レスポンスボディを JSON としてパースする（サブクラスで実装必須）"""
        ...


class HttpClient(ABC):
    """HTTP クライアントの契約を定義する抽象基底クラス"""

    @abstractmethod
    def post(
        self, url: str, json: JsonObject, headers: Headers | None = None
    ) -> HttpResponse:
        """POST リクエストを送信する（サブクラスで実装必須）"""
        ...


class BrokenClient(HttpClient):
    pass  # post を実装していない


client = BrokenClient()
# TypeError: Can't instantiate abstract class BrokenClient with abstract method post
