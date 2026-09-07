# Astra harness 감사 — 1차 migration 이후

감사일: 2026-09-07. 정책 변경 제안이며 새로운 governing policy가 아니다.

후속 작업은 아래 「Handoff 반영 및 보완 결과」에 기록했다. 원 감사의 SPOT findings는 추출 시 주의사항이며 SPOT migration을 승인하거나 요구하지 않는다.

대상 HEAD: operating-envelope `76be1df`, predictor_v3 `d305e74a`, oil_level_tracker `b64a7aa`, SPOT `5153c9e`.
사용자 확인에 따라 Predictor/Oil의 1차 migration은 완료된 것으로 평가했다. 이번 감사는 해당 checkout의 정책·스킬·checker·배포 파일과 SPOT의 추출 후보를 검토했으며 제품 전체 코드 감사는 아니다.

## 판단

방향은 적절하다. 작은 전역 행동 규칙, 조건부 재사용 스킬, 프로젝트 고유 계약, 지식/역사 분리는 유지할 가치가 있다. 추가 경량화는 전역 AGENTS의 글자 수보다 불필요하게 활성화되는 읽기·문서 작성·승인·검증 의무에 집중하는 편이 낫다.

공식 Astra 가이드는 instruction sensitivity, 불필요한 질문/중단, 과도한 검증을 직접 다룬다. 현재 전역 정책의 자율 실행·사용자 의도 우선·비례 검증은 이에 부합한다. 다만 six-layer 구조, recall temperatures, Soluna 역할/모델 제한은 OpenAI의 필수 규격이 아니라 이 저장소의 설계 선택이다.

공식 근거:

- [GPT-6 Astra model and prompting guidance](https://developers.openai.com/api/docs/guides/latest-model): 지시 충돌 감사, 자율 실행, 검증 범위 조정.
- [Codex custom instructions](https://developers.openai.com/codex/guides/agents-md): global/project instruction discovery와 override 순서.
- [Codex Skills](https://developers.openai.com/codex/skills): name/description 우선 노출 후 본문 로딩, 명확한 trigger, explicit invocation, prompt 기반 trigger 검증.

## 확인된 좋은 상태

| 표면 | 줄 수 | 비어 있지 않은 줄 | UTF-8 bytes |
| --- | ---: | ---: | ---: |
| global/AGENTS.md | 42 | 30 | 2,976 |
| Predictor AGENTS.md | 36 | 26 | 2,919 |
| Oil AGENTS.md | 24 | 16 | 1,377 |
| SPOT AGENTS.md | 84 | 62 | 3,538 |
| SPOT AGENT_TASK_ROUTER.md | 272 | 193 | 8,811 |
| SPOT PROJECT_RULES.md | 126 | 102 | 6,420 |

이 수치는 토큰 측정이 아니다. global은 자체 25–40 nonblank-line 목표 안에 있다. 길이만 줄이기 위한 재작성은 우선순위가 낮다.

- 전역 AGENTS와 canonical 5개 Skill의 모든 배포 대상 source 파일은 `~/.codex` 사본과 byte equality가 확인됐다. 전역 AGENTS.override.md는 없다.
- Predictor/Oil `core.hooksPath=.githooks` 설정을 확인했다.
- Predictor checker의 Result Record/memory-write 의무 제거와 LOC warning 전환은 코드에서도 확인됐다.
- Oil의 Windows qualification은 current owner를 통해 후보를 찾고, local PASS와 field PASS를 구분한다. 이 경계는 유지해야 한다.
- 일반 UI/portability Skills는 이미 짧고 제품 규칙과 분리되어 있다. 통합하여 하나의 거대한 desktop Skill로 만들 이유가 없다.
- Soluna는 의도적으로 무거운 explicit-only workflow다. 일반 작업에 적용하지 않는다면 그 크기 자체는 상시 비용 문제가 아니다. 이번 감사에서는 실행하지 않았다.

## Findings

### F1 · P2 · SPOT의 cross-project authority를 그대로 수입하면 새 구조와 충돌한다

근거: `SPOT/docs/ui_ux/00_UI_UX_SYSTEM.md:5–19`, `01_TOOLKIT_SELECTION_POLICY.md:5–24`, `03_SPREADSHEET_TABLE_UX_CONTRACT.md:5–28`.

SPOT 문서는 자신을 모든 desktop project의 SSOT로 선언하고 개별 프로젝트 UI 문서보다 우선한다고 한다. Toolkit policy는 새 table-heavy 앱에 PyQt5를 기본값으로 지정한다. 반면 현재 Predictor는 PySide6의 프로젝트 owner를 갖고 있고, operating-envelope는 toolkit/visual/domain 정책을 repo-local로 둔다.

SPOT이 아직 다른 프로젝트에 자동 적용된다는 뜻은 아니다. 추출·복사할 때 활성 정책으로 승격되면 충돌한다는 발견이다.

권고: SPOT 로컬 계약의 scope를 명시하고, 재사용 가능한 일부 행동만 기존 global Skill에 합친다. PyQt5 기본값, 색상·크기, 2–7 point 화면 목표, paste overflow/invalid 처리의 특정 선택은 global로 올리지 않는다.

### F2 · P2 · Oil checker는 작은 detector 수정에도 설계 문서 변경을 강제한다

근거: `oil_level_tracker/scripts/check_detector_governance.py:64–66,369–384`; `docs/30-validation/s11-detector-change-governance.md`.

checker는 path 기반으로 detector source 변경을 감지하고 companion design document + History Review block을 요구한다. 변경 내용이 주석인지, 동작 보존 수정인지, 새로운 mechanism인지 구별하지 않는다. validation 문서 변경에도 companion design을 요구한다. `check_changed_files()`에 vision `__init__.py` 경로만 전달하는 비변경 probe에서도 해당 오류를 재현했다.

이는 현재 의도된 safeguards이며 migration 미완료의 증거는 아니다. 다만 작은 수정을 반복할 때 문서 churn이 남는 가장 구체적인 비용이다.

권고: 계약/메커니즘/acceptance 변경의 hard gate는 유지한다. 동작 보존 변경에 한해서 기존 설계 owner와 연결하는 가벼운 경로가 필요한지 실제 사례로 평가한다. 자동 판별이 불확실한 경우 무조건 면제하거나 checker 전체를 warning으로 바꾸지 않는다. reviewed truth, provenance, generic detector 경계는 그대로 보존한다.

### F3 · P2 · Predictor hot memory에 현재 상태와 실행 지시가 다시 들어왔다

근거: `predictor_v3/result_reports/memory/project_memory_seed.md:71–94`.

seed는 113줄/12,700 bytes다. Phase closure, PR별 확인 상태, exact next gate, hold/defer 상태와 “다른 gate를 만들지 말라”는 문장을 담고 있다. 상단에는 evidence라고 선언하지만 상세 상태가 work plan과 이중 유지되며, Astra가 회상한 과거 실행 지시를 현재 작업 제약으로 읽을 여지가 있다. 이번 감사는 그 상태가 현재 틀렸다고 판정한 것은 아니다.

권고: topic + durable lesson 1–2문장 + current owner + 필요한 failure/decision 링크로 축약한다. acceptance 재실행 금지의 이유는 보존하되 현재 pending/closed 순서는 WORK_PLAN에서 읽도록 한다. Oil recall-index(34줄/2,255 bytes)는 더 가벼운 비교 사례다. memory 자체를 폐기할 이유는 없다.

### F4 · P2 · 사용자 Skill 경로 검증이 특정 host 배포 선택을 보편 규칙으로 다룬다

근거: `operating-envelope/scripts/validate_harness.py:77–78`, README 및 architecture의 deployment 설명.

validator는 active docs에 `~/.agents/skills`가 등장하면 retired 경로라며 실패한다. 그러나 감사 당일 가져온 공식 Skills 문서는 이 경로를 USER discovery location으로 기재한다. 현재 세션은 실제 `~/.codex/skills` 파일들을 노출하므로 현재 배포 장애로 판단하지 않는다. 문제는 공식 경로를 일률적으로 폐기했다고 단정하는 portability/maintenance 정책이다.

권고: 현재 desktop host에서 검증한 배포 위치와 다른 host/CLI의 공식 discovery contract를 구분한다. 문자열 금지 대신 선택한 host에서 discovery·중복 노출·원본 일치를 확인한다. 두 경로에 일괄 복제하면 같은 이름의 Skill이 중복 노출될 수 있으므로 자동 복제는 피한다.

### F5 · P2 · 구조 검증 PASS와 실제 Astra 행동 검증을 구분해야 한다

근거: `scripts/validate_harness.py`, `.github/workflows/harness-validation.yml`, architecture §14.

현재 CI는 요구 Skill의 name/description/implicit metadata, upstream pin, 일부 tracked-file 상태와 Soluna state-machine tests를 검사한다. 파일 구조에는 유용하지만 일반 수정에서 질문 없이 진행하는지, 잘못된 Skill이 켜지는지, 불필요한 history/전체 테스트를 읽는지는 증명하지 않는다. 필수 목록 밖의 추가 Skill은 같은 검사를 자동으로 받지도 않는다.

권고: 실사용 사례 6–8개를 작은 수동 회귀 세트로 둔다. trivial bug fix, table paste, unrelated calculator edit, past failure recall, ordinary ambiguity vs explicit grill-me, explicit Soluna, qualification vs local iteration을 포함한다. 불필요 질문 수·읽은 정책 파일·검증 재실행·완료 여부를 기록한다. 새 상시 승인 gate나 대규모 eval 시스템은 만들지 않는다. 신규 Skill은 directory discovery로 구조 검사 대상에 포함시키는 정도면 충분하다.

### F6 · P2 · SPOT 라우터/packaging에 불필요한 중단과 과검증 문구가 남아 있다

근거: `SPOT/AGENT_TASK_ROUTER.md:67,126,200`, `SPOT/PACKAGING_RULE.md:540`, `SPOT/AGENTS.md:24`.

- 모든 UI 작업에 toolkit selection 문서까지 필수 읽기.
- UI 변경 검증을 “no new imports”로 규정하여 새 외부 dependency와 정상적인 내부 import를 혼동.
- architecture 작업에 “broadest relevant local check” 요구.
- packaging 끝에는 “agent는 문서 업데이트만 수행”이라는 host와 무관한 실행 제한.
- 요구 충돌 시 일괄 중단 규칙은 우선순위로 해결 가능한 경우까지 질문을 유발할 수 있음.

권고: toolkit selection은 신규 선택/이전 때만 읽는다. imports 대신 승인되지 않은 dependency 및 DRM 경계 변화를 검사한다. 검증은 changed contract 기준으로 선택한다. packaging은 실제 Windows 환경/권한/도구가 있을 때 실행하고, 없으면 build/runtime evidence를 UNVERIFIED로 남기도록 쓴다. 기존 승인된 행동을 막는 보편적 문서-only 제한은 제거 후보이다.

## SPOT에서 가져올 가치가 있는 것

신규 global Skill은 우선 만들지 않고 기존 두 Skill을 작게 보강하는 것을 권고한다.

| 후보 | 근거 | 목적지 및 추출 범위 |
| --- | --- | --- |
| 한 번의 edit/paste/clear를 한 번에 undo | table contract §5,7; `ui/initial_values_table.py:517–608`의 snapshot/undo 구현 | `desktop-table-ui`: undo 지원 표면의 action 단위, data context 교체 시 history 수명 정의 |
| empty / zero / invalid / readonly / inactive 구분 | table contract §8–9 | `desktop-table-ui`: 상태 의미와 edit/paste/clear 경로의 일관성. empty가 유효한지는 domain validator가 판단 |
| 진행 UI, 성공/실패 시 정리 | UI system §5–6, Tk adapter §6 | `desktop-window-lifecycle`: progress 표시 시점, 실패/취소/종료 시 resource 및 UI 정리. 1초 임계치나 특정 scheduler는 일반화하지 않음 |
| Tkinter selection/editor/focus 기법 | Tk adapter §4–7 | 실제 반복 필요가 있을 때만 optional reference. toolkit 선택·SPOT helper 이름·Excel COM 정책은 로컬 유지 |
| EXE 외부 user-writable resources와 내부 bundle 분리, host log 미포함 | PACKAGING_RULE의 visible tools/layout 및 log 정책 | 우선 SPOT packaging owner에 유지. 다른 프로젝트에서 같은 배포 문제를 확인한 뒤 공통 reference 후보로 승격 |
| 표준화한 측정과 검증 수준 구분 | Windows export smoke 문서, PACKAGING_RULE preview vs Windows 구분 | 기존 Windows/local verification 원칙과 통합. 새 global qualification 절차로 복제할 필요 없음 |

그대로 복사하지 않을 내용: “어떤 표든 full spreadsheet 기능 필수”, invalid 값 무조건 저장, overflow 무조건 silent drop, Tkinter/PyQt5 선택 강제, 취소가 언제나 가능하다는 무조건 계약, Excel DRM API 제한, frozen result schema, packaging cleanup/배포 파일명. 제품·표면별 선택과 기술적 검증이 필요한 내용이다.

SPOT에서 추출 가능한 새 Git hook 또는 repo Skill 디렉터리는 이번 정책 inventory에서 발견하지 못했다. hook 설정도 없었다. 따라서 hook을 이식하기보다는 필요할 때 SPOT의 실제 domain/packaging invariant를 검사하는 작은 checker를 설계하는 편이 적절하다.

## 다음 적용 순서

1. 현재 global AGENTS와 기존 Skill 분할은 유지한다. Soluna allocation 승인 구조도 explicit workflow의 의도된 제약으로 유지한다.
2. SPOT의 전역 authority 문구와 F6 trigger를 정리하고, 기존 table/window Skill에 위 공통 행동만 추가한다.
3. Predictor seed의 current-state 중복을 줄인다. Oil governance는 실제 작은 변경 사례를 기준으로 제한적으로 조정한다.
4. host별 install/check 절차를 짧게 문서화하거나 작은 dry-run/check 도구로 만든다. 현재 canonical/runtime equality 검증을 재사용하고 거대한 installer framework는 만들지 않는다.
5. 새 프로젝트는 작은 repo AGENTS와 필요한 Skill만 사용한다. 여섯 layer는 논리적 분류이므로 빈 memory/decision/failure/router 파일을 미리 전부 생성할 필요가 없다. 첫 반복 실패/결정 또는 조건부 절차가 생겼을 때 해당 owner를 추가한다.
6. 대표 작업에서 행동 차이를 관찰한 뒤 추가 slimming을 결정한다. 공식 가이드 문장을 더 많이 복사하는 것을 개선 지표로 삼지 않는다.

## 검증 및 한계

- `python3 scripts/validate_harness.py`: PASS.
- `python3 -B skills/soluna/scripts/test_workflow_state.py`: 14 tests PASS.
- canonical global 및 5개 Skill source-to-runtime byte comparison: 모두 일치.
- Predictor/Oil hook config 확인, checker source inspection, Oil path-only API probe 완료.
- 모든 대상 checkout은 감사 시작 시 clean이었다. 감사 보고서 외 정책/source/runtime 변경, commit/push는 수행하지 않았다.
- 실제 fresh Astra 세션의 before/after 행동 평가, 제품 전체 테스트, UI 수동 검증, Windows packaging/field 실행은 수행하지 않았다. 따라서 latency/token 절감 수치나 전체 migration의 동작 완료를 새로 증명했다고 주장하지 않는다.

## Handoff 반영 및 보완 결과 — 2026-09-07

사용자가 제공한 이전 작업자의 handoff에 따르면 reserve 모델의 실행/trigger probes는 이미 통과했고, Astra 실제 실행만 quota로 막혀 있었다. F5는 기존 행동 검증 전체가 없었다는 의미로 해석하지 않는다. 기존 Soluna 14 tests 및 이전 migration regression 증거를 재사용하고, 이번 변경과 미검증 Astra 동작에 집중했다.

승인된 후속 범위: SPOT은 읽기/추출만, global Skill 소폭 보강, host deployment validation, Predictor memory slimming, 독립 read-only review. Oil checker/Graphify/브랜치 통합은 보류했다. 원격 확인 시 Oil은 main 대비 8 ahead였으며 handoff의 7 ahead 표기는 맞지 않았다.

완료된 변경:

- `desktop-table-ui`: dataset 경계의 undo 수명, 한 번의 동작 단위 undo, empty/zero/invalid/read-only/inactive 의미 분리. SPOT table contract §5/7/8에서 추출했으며 특정 toolkit·paste 정책은 수입하지 않았다.
- `desktop-window-lifecycle`: progress rendering과 작업 종료/실패/지원되는 취소의 UI 정리. SPOT UI system §5/6에서 추출했으며 무조건 취소 지원이나 1초 임계치는 수입하지 않았다.
- validator: 공식 사용자 경로 문자열 금지를 제거하고 신규 Skill도 발견하여 검사. 명시한 runtime root의 global/managed Skill source equality와 override를 선택적으로 검증한다. CI에 focused validator tests를 추가했다.
- [DEPLOYMENT.md](DEPLOYMENT.md): 현재 desktop 경로와 다른 host의 discovery를 구분하고 파일 일치와 행동 검증을 분리했다. 새 프로젝트에 빈 레이어 파일을 미리 만들 필요가 없음을 명시했다.
- Predictor hot seed: 12,700 → 9,216 bytes(약 27% 감소). 기존 evidence links를 보존하고 모든 source path 존재를 확인했다. 현재 상태/순서/holds는 WORK_PLAN에 남겼고, memory workflow owner도 그 경계를 명시했다.
- 변경한 두 Skill을 현재 desktop runtime에 배포했다. 전역 AGENTS 및 모든 5개 canonical Skill의 runtime equality가 통과했다.

### 실제 Astra probes

두 probe는 `codex exec --ephemeral -m gpt-6-astra -c model_reasoning_effort="low"`로 별도 임시 Git 저장소에서 수행했다. 모델 대체 없이 두 실행 모두 exit 0과 `turn.completed`를 확인했다.

1. **자율 수정 및 비례 검증:** 다른 cwd에서 `label.txt`를 읽는 작은 `reader.py`의 경로/UTF-8 수정을 요청했다. 기존 function signature와 label을 보존하고 focused unittest로 검증하도록 했다. Astra는 module-relative path와 explicit UTF-8로 수정하고 기존 테스트 1개만 실행하여 PASS했다. 승인 질문, 위임, broad test, memory scan은 없었다. `python-test-portability` 파일을 읽은 기록은 없으므로 해당 implicit trigger는 이 probe로 증명하지 않는다.
2. **변경한 UI Skill 호출 및 적용:** multi-cell paste 후 dataset switch 시 undo 오염, load 실패 후 progress dialog 잔류에 대한 짧은 repair advice를 요청했다. Skill 이름/경로는 prompt에 주지 않았다. Astra는 실제 runtime의 `desktop-table-ui/SKILL.md` 및 `desktop-window-lifecycle/SKILL.md`를 읽었고 dataset별 undo 수명, action 단위 undo, success/failure/cancel cleanup을 제안했다. toolkit migration이나 무조건 모든 표에 undo 추가를 요구하지 않았다. 이 결과는 advice/Skill invocation 검증이며 실제 GUI 구현 검증은 아니다.

로컬 원시 증거(임시 파일, durable owner가 아님):

- `/var/folders/s2/wbnr4dhn1z1bk7tcl342s8bw0000gn/T/astra-harness-probe-qzlmvyfh/`: fixture, `events.jsonl`, `final.txt`.
- `/var/folders/s2/wbnr4dhn1z1bk7tcl342s8bw0000gn/T/astra-ui-skill-probe-zryuw63s/`: `events.jsonl`, `final.txt`.

### 최종 검증

- Canonical validator 및 `--runtime-home ~/.codex`: PASS.
- 새 deployment validator regression: 4 tests PASS. 누락/변조/extra managed files, global override/drift, 대체 root/unmanaged Skill, 신규 Skill 검사 경로를 포함.
- 변경한 두 Skill: system skill-creator `quick_validate.py` PASS.
- 독립 read-only subagent: 두 repo diff, SPOT 추출 근거, Predictor WORK_PLAN 및 validator/tests를 직접 검토; material findings 없음.
- 두 repo whitespace checks 및 seed source-path 확인: PASS.
- SPOT/Oil checkout은 변경하지 않았다. commit/push/merge는 수행하지 않았다.

범위 한계: 이 작은 Astra 표본은 전체 작업에서 항상 동일하게 행동함을 증명하지 않는다. 이전 reserve trigger 증거는 별도로 유지하며, 실제 Windows/UI 실행, Graphify real-task pilot, Oil governance 완화, main integration은 이번 완료 범위가 아니다.

## 추가 승인된 Oil 조정 — 2026-09-07

이후 사용자가 Oil checker의 일부 경량화와 누적 변경 전체의 commit/merge/push를 승인했다. 같은 경로의 기존 Python 파일에서 AST, 파일 mode, encoding, shebang이 보존되는 cosmetic 수정은 companion design 의무에서 제외했다. 비교는 실제 merge base와 checked head/worktree를 사용하며 baseline이 없으면 면제하지 않는다.

상수/동작/docstring/type-comment 변경, 새 파일/삭제/이름 변경, 파싱 실패는 기존 gate를 유지한다. Markdown 오타나 링크는 acceptance/evidence 변경과 안전하게 구별할 수 없으므로 자동 면제하지 않았다. 삭제된 worktree 설계 문서가 HEAD 사본으로 대체되어 gate를 만족시키는 경우도 막았다.

Focused checker regression: 27 tests PASS. 기존 환경의 `qt_api` 미인식 warning은 동일하다. 독립 read-only 검토는 material findings가 없었으며, 마지막 merge-base divergence 회귀 추가 후 관련 suite를 통과했다. 제품 source와 R21 field disposition은 바꾸지 않았다. Integration은 기존 SHA를 보존하는 fast-forward 순서(R21 → harness)를 사용하며 별도 Windows field acceptance 완료로 간주하지 않는다.
