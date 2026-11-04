# fstack 使用指南

fstack 把 pstack 的任務路由、角色分工、獨立審查、驗證和決策紀錄改造成投資研究流程。第一階段涵蓋美股、港股、ETF、組合分析，以及日線或更長週期的策略研究。

## 安裝

需要 Python 3.11 或以上。在套件根目錄執行：

```sh
python -m pip install -e .
python scripts/check_package.py
python scripts/install.py /你的研究專案絕對路徑
python scripts/install.py /你的研究專案絕對路徑 --apply
```

沒有 `--apply` 時只顯示安裝預覽。正式安裝將完整套件放在專案的 `.agents/fstack/`，並在 `.agents/skills/` 建立技能入口。Windows 不需要符號連結權限。相同版本重跑不會重寫；若目標檔案已有不同內容，會先停止且不寫入任何檔案。其他既有技能保持原狀。

在 Codex 開啟該專案，使用 `$fstack`。若技能清單未更新，重新啟動客戶端。設定技能會檢查當前工具及模型能力；不會自行替你申請資料服務或建立券商權限。

## 開始研究

提供一間公司、一個可觀察的看法和時間範圍。例如：

```text
$fstack 我認為這間公司未來兩季的毛利率改善會超出預期。請核實資料、找反證，並說明目前是否建立了預期差。
$fstack 用這些資料建立可重現的日線策略研究。先固定規則、成本和評估方法，再執行。
$fstack-interrogate 檢查這份研究的論點、資料及計算。把可重現錯誤與仍待觀察的經濟疑慮分開報告。
```

主代理依任務選擇 playbook，列明步驟並負責最後結論。複雜研究保留不同工作代理的獨立產出。作者與驗證者分開，資料缺口及模型多樣性不足會如實記錄。簡單問題使用適合的較短流程。

## 驗算範例

在套件根目錄執行：

```sh
python -m fstack_tools check-data examples/daily_research/us.csv examples/daily_research/us.metadata.json
python -m fstack_tools check-data examples/daily_research/hk.csv examples/daily_research/hk.metadata.json
python -m fstack_tools verify examples/daily_research/manifest.json examples/daily_research/.fstack/receipt.json --verifier reviewer
python -m fstack_tools check-receipt examples/daily_research/.fstack/receipt.json
```

範例公司、價格和策略都是假資料，用來檢查發布時間、交易時段、拆股、股息、成本和重現能力。它不是即時行情或回報承諾。

`verify` 會執行 manifest 列明的程式。執行他人提供的 manifest 前，先檢查其中的指令。驗證要求新輸出，不能以舊檔案冒充新證據；每次研究使用新的輸出目錄。憑證建立後不覆寫。重要輸入改變，舊憑證就不再對應目前研究。驗證者姓名是操作者聲明，並不是經認證的身分或獨立性證明。

## 理解結果

資料／計算完整性、投資論點支持度及績效證據會各自報告。計算正確不等於存在持續的交易優勢。市場共識查不到就標示未知，不能以 AI 的猜測補齊。

策略研究先固定規則、資訊截止時間、成本及評估設計。用過來調整策略的資料不再是未受影響的評估資料。原始預測、失敗嘗試和修正理由保留在追加式紀錄。

真實 API key、持倉、交易資料及研究輸出應放在被忽略的本地位置。公開範例只使用假資料。`.gitignore` 不會移除已經進入 Git 歷史的秘密。

## 來源與範圍

原版固定為 pstack v0.15.36、commit `c742dd61706fbacc1b95f1a20b7b988cf096ce6c`。請參閱[原版改造對照](upstream-map.md)和[架構說明](architecture.md)。套件保留原作者署名與 MIT 授權。

fstack 交付研究與模擬成果。實盤下單、轉帳、付費資料訂閱及公開發布研究，需要各自明確的使用者指示。
