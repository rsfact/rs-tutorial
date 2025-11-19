from pydantic import BaseModel

class ShortenRequest(BaseModel):
    """
    リクエスト: URL登録
    """
    from_name: str
    to_url: str

class ShortenResponse(BaseModel):
    """
    レスポンス: URL登録
    """
    uuid: str
    from_name: str
    to_url: str
    count: int
