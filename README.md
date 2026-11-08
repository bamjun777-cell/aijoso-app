# AI 좋소 (Android)

작은 회사의 큰 업무를 가볍게 — 중소기업 실무자를 위한 AI 업무 자동화 매뉴얼 앱.

## 현재 단계: 1단계 (기본 앱)
- 홈 · 찾기 · 프롬프트 · 보관함 4개 탭
- 매뉴얼 상세: 빈칸 채우기 프롬프트 복사, Claude 열기, 즐겨찾기, 공유
- 의견 남기기 (욕설·비속어·개인정보 차단) — 전송은 3단계에서 연결, 지금은 휴대폰에 저장
- 콘텐츠는 `app/src/main/assets/content.json` 하나로 관리 (화면 코드 수정 없이 추가)
- 서버 없음, 회원가입 없음, 인터넷 권한 없음

## 다음 단계
2. AdMob 테스트 배너 · A4 출력 미리보기 · 최신 콘텐츠 자동 받기(GitHub Pages)
3. Firebase(무료 플랜): 의견 전송 · 이용 분석

## 빌드
GitHub에 올리면 `.github/workflows/android.yml`이 자동으로
검사(콘텐츠·검색·비속어 필터) → 테스트 APK 빌드 → Releases의 `test-latest`에 APK를 올린다.

PC에서 직접: Android Studio로 폴더 열기 → ▶ Run.

- 기술: Kotlin · Jetpack Compose · Material 3 · kotlinx.serialization
- 대상: Android 8.0(API 26) 이상, targetSdk 36(Android 16)
- `app/debug.keystore`는 테스트 APK 덮어쓰기 설치용. 출시용 키는 별도 보관, 저장소에 올리지 않음.
