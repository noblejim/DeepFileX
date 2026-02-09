# 🤝 DeepFileX 기여 가이드

DeepFileX 프로젝트에 관심을 가져주셔서 감사합니다! 이 문서는 프로젝트에 기여하는 방법을 안내합니다.

---

## 📋 목차

- [행동 강령](#행동-강령)
- [기여 방법](#기여-방법)
- [개발 환경 설정](#개발-환경-설정)
- [코딩 규칙](#코딩-규칙)
- [커밋 메시지 규칙](#커밋-메시지-규칙)
- [Pull Request 프로세스](#pull-request-프로세스)
- [이슈 리포트](#이슈-리포트)

---

## 행동 강령

### 우리의 약속

포용적이고 환영받는 환경을 조성하기 위해, 우리는 다음을 약속합니다:
- 🤝 모든 기여자를 존중합니다
- 💬 건설적인 피드백을 제공합니다
- 🌍 다양성을 존중합니다
- 📚 배움에 열려있습니다

---

## 기여 방법

DeepFileX에 기여할 수 있는 여러 방법:

### 1. 🐛 버그 리포트
- 버그를 발견하셨나요? [이슈를 생성](https://github.com/noblejim/DeepFileX/issues/new)해주세요
- 재현 가능한 단계를 포함해주세요
- 예상 동작과 실제 동작을 명시해주세요

### 2. ✨ 기능 제안
- 새로운 기능 아이디어가 있으신가요?
- [Discussion](https://github.com/noblejim/DeepFileX/discussions)에서 먼저 논의해주세요
- 기능의 필요성과 사용 사례를 설명해주세요

### 3. 💻 코드 기여
- 버그 수정
- 새로운 기능 구현
- 성능 개선
- 코드 리팩토링

### 4. 📖 문서 개선
- README 개선
- 코드 주석 추가
- 사용 가이드 작성
- 번역 (영어, 일본어 등)

### 5. 🧪 테스트
- 테스트 케이스 추가
- 버그 재현 확인
- 베타 테스트 참여

---

## 개발 환경 설정

### 필수 요구사항

- **Python**: 3.8 이상
- **OS**: Windows 10/11 (64bit)
- **Git**: 최신 버전
- **IDE**: VS Code, PyCharm 등 (선택)

### 설정 단계

1. **저장소 Fork & Clone**
   ```bash
   # GitHub에서 Fork 후
   git clone https://github.com/YOUR_USERNAME/deepfilex.git
   cd deepfilex
   ```

2. **upstream 리모트 추가**
   ```bash
   git remote add upstream https://github.com/noblejim/DeepFileX.git
   ```

3. **가상환경 생성**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

4. **의존성 설치**
   ```bash
   # 기본 의존성
   pip install -r requirements.txt

   # 개발 의존성 (선택)
   pip install pyinstaller pytest black flake8
   ```

5. **개발 모드로 실행**
   ```bash
   python src\filemri.py
   ```

---

## 코딩 규칙

### Python 스타일 가이드

DeepFileX는 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 스타일 가이드를 따릅니다.

#### 주요 규칙

```python
# ✅ Good
def analyze_file(file_path: str) -> dict:
    """파일을 분석하고 메타데이터를 반환합니다.

    Args:
        file_path: 분석할 파일 경로

    Returns:
        파일 메타데이터 딕셔너리
    """
    result = {}
    # 구현...
    return result


# ❌ Bad
def analyzeFile(filePath):
    result={}
    #구현
    return result
```

#### 인코딩
- **UTF-8 사용 필수** (이모지 지원)
- 파일 상단에 `# -*- coding: utf-8 -*-` 명시

#### 네이밍 컨벤션
- **함수/변수**: `snake_case`
- **클래스**: `PascalCase`
- **상수**: `UPPER_CASE`
- **Private**: `_leading_underscore`

#### 코드 포맷팅 도구

```bash
# Black (자동 포맷팅)
black src/

# Flake8 (린트)
flake8 src/

# isort (import 정리)
isort src/
```

---

## 커밋 메시지 규칙

### 형식

```
🎯 타입: 간단한 설명 (50자 이내)

상세 설명 (선택, 72자로 줄바꿈)

관련 이슈: #123
```

### 타입 이모지

| 타입 | 이모지 | 설명 |
|------|--------|------|
| feat | ✨ | 새로운 기능 |
| fix | 🐛 | 버그 수정 |
| docs | 📝 | 문서 변경 |
| style | 💄 | 코드 스타일 (포맷팅, 세미콜론 등) |
| refactor | ♻️ | 코드 리팩토링 |
| perf | ⚡ | 성능 개선 |
| test | ✅ | 테스트 추가/수정 |
| build | 🔧 | 빌드 시스템, 의존성 변경 |
| ci | 👷 | CI 설정 변경 |
| chore | 🔨 | 기타 변경사항 |

### 예시

```bash
✨ feat: Add dark mode toggle button

사용자가 UI에서 다크모드를 쉽게 전환할 수 있도록
토글 버튼을 추가했습니다.

관련 이슈: #42
```

---

## Pull Request 프로세스

### 1. 브랜치 생성

```bash
# upstream에서 최신 변경사항 가져오기
git fetch upstream
git checkout master
git merge upstream/master

# 새 브랜치 생성
git checkout -b feature/amazing-feature
# 또는
git checkout -b bugfix/fix-something
```

### 2. 코드 작성 및 테스트

- 변경사항 구현
- 로컬에서 충분히 테스트
- 코드 스타일 확인

```bash
# 프로그램 실행 테스트
python src\filemri.py

# 코드 포맷팅
black src/

# 린트 체크
flake8 src/
```

### 3. 커밋

```bash
git add .
git commit -m "✨ feat: Add amazing feature"
```

### 4. 푸시

```bash
git push origin feature/amazing-feature
```

### 5. Pull Request 생성

1. GitHub에서 본인의 Fork로 이동
2. "Compare & pull request" 버튼 클릭
3. PR 템플릿 작성:
   - **제목**: 명확하고 간결하게
   - **설명**: 변경사항 상세히 설명
   - **관련 이슈**: `Closes #123` 형식으로 명시
   - **테스트**: 테스트 방법 설명
   - **스크린샷**: UI 변경 시 포함

4. "Create pull request" 클릭

### 6. 리뷰 대응

- 리뷰어의 피드백에 성실히 대응
- 요청된 변경사항 수정
- 추가 커밋으로 업데이트

```bash
# 수정 후
git add .
git commit -m "🐛 fix: Address review comments"
git push origin feature/amazing-feature
```

---

## 이슈 리포트

### 버그 리포트 템플릿

```markdown
## 🐛 버그 설명
간단한 버그 설명

## 📋 재현 단계
1. '...'로 이동
2. '...' 클릭
3. '...' 스크롤
4. 오류 발생

## ✅ 예상 동작
예상했던 동작 설명

## ❌ 실제 동작
실제로 발생한 동작 설명

## 📸 스크린샷
(해당되는 경우 추가)

## 💻 환경
- OS: Windows 11
- Python: 3.11.0
- DeepFileX: 1.3.0

## 📝 추가 정보
기타 관련 정보
```

### 기능 제안 템플릿

```markdown
## ✨ 기능 설명
간단한 기능 설명

## 🎯 해결하려는 문제
이 기능이 해결하려는 문제

## 💡 제안하는 해결책
구체적인 구현 방안

## 🔄 대안
고려해본 다른 방법들

## 📝 추가 정보
기타 관련 정보, 스크린샷 등
```

---

## 질문이 있으신가요?

- 💬 [Discussions](https://github.com/noblejim/DeepFileX/discussions)에서 질문해주세요
- 📧 이메일: contact@quantumlayer.com
- 🐛 버그는 [Issues](https://github.com/noblejim/DeepFileX/issues)에 리포트해주세요

---

**감사합니다!** 🎉

DeepFileX 프로젝트에 기여해주셔서 감사합니다. 여러분의 기여가 DeepFileX를 더 나은 도구로 만들어갑니다!

🔷 **DeepFileX by QuantumLayer** - Advanced File Analysis System
