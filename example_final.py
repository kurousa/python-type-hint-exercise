from typing import Final


class ExampleFinalClass:
    # クラスのトップレベルで Final が宣言された場合、それを暗黙的にクラス変数（ClassVar 相当）として処理
    COLLECT_FINAL_CLASS_VAR: Final[str] = "Class Variable Value"

    # 違反理由: Final は一番外側に記述しなければならないから
    # BAD_FINAL_CLASS_VAR: ClassVar[Final[str]] = "Class Variable Value"
    # 違反理由：ClassVar と Fianl は重複禁止(PEP591)
    # BAD_FINAL_CLASS_VAR2: Final[ClassVar[str]] = "Class Variable Value2"

    def __init__(self) -> None:
        # mypyで定数変更しようとしていることを検出できる
        # self.COLLECT_FINAL_CLASS_VAR = "some change"
        pass
