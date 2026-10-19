# ETA-Motion project page

ETA-Motion 논문을 위한 영문 정적 프로젝트 페이지입니다. HTML / CSS / JavaScript로 구성되어 있으며 별도의 빌드나 패키지 설치가 필요하지 않습니다.

## 미리보기

Node.js가 설치되어 있으면 프로젝트 폴더에서 실행합니다.

```sh
npm run dev
```

브라우저에서 <http://127.0.0.1:4173>을 엽니다. 종료는 터미널에서 `Ctrl+C`입니다. `site/index.html`을 직접 열어도 볼 수 있지만, 영상 탐색 및 클립보드 기능 확인에는 로컬 서버를 권장합니다.

## 논문 / 코드 링크 추가

`site/config.js`에서 다음 항목을 수정합니다. 값이 비어 있으면 해당 버튼이나 정보는 표시되지 않습니다.

```js
window.ETA_CONFIG = {
  paperUrl: "",       // arXiv URL 또는 assets/paper.pdf
  codeUrl: "",        // 공개 코드 저장소 URL
  supplementUrl: "", // supplementary PDF URL
  venue: "",          // 확정된 발표 학회·연도만 기입
  bibtex: "",         // 최종 BibTeX 전체 문자열 (여러 줄이면 백틱 사용)
  siteUrl: ""         // 최종 프로젝트 페이지 URL, 끝에 / 포함
};
```

PDF를 올리려면 `site/assets/paper.pdf`에 넣고 `paperUrl`을 `assets/paper.pdf`로 바꾸세요. arXiv와 Code 버튼은 URL이 비어 있으면 Coming soon으로 표시되며 클릭할 수 없습니다. URL을 입력하면 자동으로 활성화됩니다. 기본 BibTeX는 WACV 2027 학회 논문 형식이며, 페이지 상단에 WACV 2027을 표시합니다. 페이지 번호와 DOI는 추후 확정되면 추가하세요.

소셜 미디어 공유 이미지까지 설정하려면 배포 후 `index.html`의 `og:image`를 전체 URL로 바꾸고 `og:url` 및 canonical 태그를 추가하세요. 일부 공유 봇은 `config.js`를 실행하지 않습니다.

## GitHub Pages 배포

1. GitHub에서 빈 저장소를 만듭니다. 무료 개인 계정이라면 공개 저장소를 사용합니다.
2. 이 프로젝트의 웹사이트 파일을 `main` 브랜치에 올립니다. `.gitignore`가 원본 LaTeX, PPTX, 원본 동영상, ZIP, 작업용 폴더를 제외합니다.
3. 저장소의 **Settings → Pages → Build and deployment → Source**를 **GitHub Actions**로 선택합니다.
4. **Actions → Deploy project page → Run workflow**를 실행합니다. 이후 `main`에 push할 때마다 자동 배포됩니다.
5. 완료 후 Pages 설정에 표시된 주소로 접속합니다. 보통 `https://사용자명.github.io/저장소명/` 형태입니다.

터미널로 처음 올리는 경우, 저장소 주소를 실제 값으로 바꾸어 실행합니다. 아래 명령은 아직 실행하지 않았습니다.

```sh
git init -b main
git add .
git commit -m "Add ETA-Motion project page"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

워크플로는 **`site/` 폴더만** 게시합니다. `main` 대신 다른 브랜치를 사용하려면 `.github/workflows/pages.yml`의 브랜치 이름을 바꾸세요. 외부 패키지나 CDN 없이 동작하며 저장소 하위 경로에도 대응하도록 상대 경로를 사용합니다.

공식 안내: [GitHub Pages의 사용자 지정 워크플로](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## 파일 구성

| 경로 | 용도 |
| --- | --- |
| `site/index.html` | 제목, 저자, 초록, 방법, mesh 영상 갤러리, 인용 |
| `site/styles.css` | 데스크톱·모바일 스타일 |
| `site/config.js` | 논문 / 코드 / 학회 / 인용 정보 |
| `site/app.js` | 공개 링크 설정, 인용 복사 |
| `site/assets/images/` | 논문 그림의 웹용 WebP 버전 |
| `site/assets/video/mesh/` | 슬라이드별 mesh 결과 MP4 7개 |
| `.github/workflows/pages.yml` | GitHub Pages 자동 배포 |
| `scripts/serve.mjs` | 영상 탐색을 지원하는 로컬 서버 |
| `scripts/check.mjs` | 파일·링크·이미지 설명 검사 |

## 내용과 원본

제목·저자는 `main.tex`, 초록은 `sec/0_abstract.tex`, 방법과 실험 수치는 `sec/3_method.tex`와 `sec/4_experiments.tex`를 기준으로 작성했습니다. 실험 지표 표, 요약 수치, 정성 비교 그림, ablation 그래프는 페이지에서 제거하고 슬라이드별 mesh 영상으로 대체했습니다.

그림은 원본 PDF에서 렌더링 후 여백을 정리했습니다. `overview_v4.pdf`는 주 아키텍처 도식을 사용하고 하단의 별도 작업 도식은 제외했습니다. 원본 논문·그림·영상은 수정하지 않았습니다.

수정 후 `npm run check`를 실행하세요. 그림을 다시 생성할 때에만 Python의 Pillow와 Poppler가 필요합니다 (`python scripts/prepare_images.py`). 배포하거나 페이지를 보는 데는 필요하지 않습니다.

## Mesh 슬라이드별 MP4

`site/assets/video/mesh/`에 mesh 결과 7개 슬라이드를 각각 독립된 MP4로 저장했습니다. 원본 녹화의 1920×1080 해상도와 슬라이드 전체 화면을 유지했습니다. 각 영상은 페이지에서 별도로 재생·반복·전체화면 보기·다운로드할 수 있습니다. `preload="none"`으로 초기 페이지 로딩 시 모든 영상이 다운로드되는 것을 피합니다.

| PPT 슬라이드 | 영상 | 원본 시작 (초) | 원본 종료 (초, 미포함) |
| --- | --- | ---: | ---: |
| 12 | Quadrupeds: walk / run | 78.969 | 87.483 |
| 13 | Quadrupeds: attack | 87.483 | 97.218 |
| 14 | Quadrupeds: fall down / rise up | 97.218 | 102.663 |
| 15 | Bipeds | 102.663 | 109.824 |
| 16 | Flying | 109.824 | 115.698 |
| 17 | Reptiles / marine | 115.698 | 122.199 |
| 18 | Insects | 122.199 | 131.439 |

전환 시간을 포함한 실제 녹화 화면에서 경계를 확인했습니다. 마지막 곤충 영상은 마지막 인사 슬라이드로 넘어가는 전환 직전에 끝납니다. 편집 경계는 `scripts/mesh_clips.json`에 기록되어 있습니다.

다시 추출하려면 원본 `ETA-Motion_Video.mp4`, FFmpeg, Python의 Pillow가 필요합니다.

```sh
python scripts/export_mesh_clips.py --ffmpeg /path/to/ffmpeg
```

배포 및 재생에는 이 도구들이 필요하지 않습니다.

전체 보충 영상 섹션은 제거했고, 제목 아래 `View mesh results` 버튼은 mesh 영상 갤러리로 연결됩니다. 전체 영상 웹용 파일은 게시 폴더에서 제외했으며 원본 녹화는 그대로 보관합니다.
