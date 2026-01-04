from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass
class AppError(Exception):
    """
    서비스/도메인에서 던지는 '비즈니스 예외'의 기본 형태.
    Router는 이걸 잡아서 공통 포맷으로 변환한다.
    """
    code: str
    message: str
    status_code: int = 400
    details: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "details": self.detail or {},
        }
    

def not_found(resource: str, resource_id: Any) -> AppError:
    return AppError(
        code=f"{resource.upper()}_NOT_FOUND",
        message=f"{resource}({resource_id}) not found",
        status_code=404,
        details={"id": resource_id},
    )

def bad_request(code: str, message: str, **details: Any) -> AppError:
    return AppError(
        code=code,
        message=message,
        status_code=400,
        details=details or {},
    )