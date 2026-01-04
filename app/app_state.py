"""애플리케이션 전역에서 공유할 객체들을 모아둡니다.

FastAPI는 스프링처럼 컨테이너가 싱글톤을 자동 관리해주진 않기 때문에,
현재 단계에서는 '간단한 전역 싱글톤' 방식으로 Service/Repository를 공유합니다.

나중에 DB/테스트를 붙이면서 Depends 기반 DI로 옮겨가도 됩니다.
"""

from app.repositories.post_repo import InMemoryPostRepository
from app.services.post_service import PostService


post_repo = InMemoryPostRepository()
post_service = PostService(repository=post_repo)
