# AI 업무 레시피 (Android) · 옛 이름 AI 좋소

작은 회사의 큰 업무를 가볍게 — 중소기업 실무자를 위한 AI 업무 자동화 매뉴얼 앱.

## 현재 단계: 1단계 (기본 앱)
- 홈 · 찾기 · 프롬프트 · 보관함 4개 탭
- 매뉴얼 상세: 빈칸 채우기 프롬프트 복사, Claude 열기, 즐겨찾기, 공유
- 의견 남기기 (욕설·비속어·개인정보 차단) — 전송은 3단계에서 연결, 지금은 휴대폰에 저장
- 콘텐츠는 `app/src/main/assets/content.json` 하나로 관리 (화면 코드 수정 없이 추가)
- 서버 없음, 회원가입 없음, 인터넷 권한 없음

## 웹 버전
같은 `content.json`으로 `web/build.py`가 정적 웹사이트(`site/`)를 만들고, `.github/workflows/pages.yml`이 GitHub Pages(무료)에 배포한다.
- 매뉴얼마다 별도 페이지 → 검색엔진 노출, 사이트맵 자동 생성
- PC 2단 레이아웃, A4 미리보기·실제 인쇄, 예시 결과 파일 내려받기
- 로컬 확인: `python3 web/build.py && cd site && python3 -m http.server`

## 다국어 (한국어 · English · 日本語 · 简体中文 · 繁體中文)
- 원본은 한국어 `app/src/main/assets/content.json`. 번역·나라별 법령은 `content/i18n/<언어>.py`
- `python3 content/build_i18n.py` → `content.<언어>.json`, `ui.json`(앱·웹 공통 화면 문구) 생성 + 검사(빈칸·한국어 남음·대만 용어)
- 법령 기준 나라: 한국어=대한민국, 영어=미국 연방, 일본어=일본, 간체=싱가포르, 번체=대만
- 번체는 간체를 대만식 표현으로 자동 변환(OpenCC s2twp + 엑셀 행/열 용어)한 뒤 `zh_Hant.py`의 대만 법령 매뉴얼로 덮어씀
- 앱: 휴대폰 언어를 따르고 설정에서 바꿀 수 있음. 웹: `/en/` `/ja/` `/zh-hans/` `/zh-hant/`
- 매뉴얼을 고칠 때: 한국어 원본 수정 → 각 언어 파일 수정 → `build_i18n.py` 실행

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
