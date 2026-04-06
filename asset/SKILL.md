---
name: Frontend Design
description: 設計並實作美觀的日系風格前端網頁畫面。以和色配色、侘寂美學與精緻工藝感為核心，產出高品質的 HTML/CSS/JS 程式碼。
---

# Frontend Design Skill

## 設計流程

當使用者要求設計前端畫面時，請依照以下步驟進行：

### Step 1：需求確認
- 確認頁面用途（landing page、dashboard、form、portfolio 等）
- 確認色系偏好（若未指定，使用日系和色配色）
- 確認是否需要 RWD（預設啟用）
- 確認技術限制（純 HTML/CSS/JS 或使用框架）

### Step 2：先產出設計稿圖片
- 使用 `generate_image` 工具產出 UI mockup
- 讓使用者確認設計方向後再實作
- 設計稿應呈現完整的介面佈局，不包含裝置外框

### Step 3：實作程式碼
請遵循以下設計原則：

#### 色彩系統（和色 — 日本傳統色）
- 不使用原始顏色（純紅、純藍、純綠），使用日本傳統和色搭配的 HSL 色彩
- 色彩靈感來自自然與四季：桜（櫻花）、藍（靛藍）、抹茶、墨、和紙
- 建立 CSS 變數管理色彩：

**淡色主題（推薦預設）— 和紙風**
```css
:root {
  /* 主色：藍鼠 — 沉穩的靛藍灰 */
  --color-primary: hsl(215, 35%, 45%);
  --color-primary-light: hsl(215, 40%, 62%);

  /* 背景：和紙色 — 溫暖的米白 */
  --color-bg: hsl(40, 30%, 96%);
  --color-surface: hsl(40, 25%, 92%);

  /* 文字：墨色系 */
  --color-text: hsl(220, 15%, 18%);
  --color-text-muted: hsl(220, 10%, 50%);

  /* 邊框：薄墨 */
  --color-border: hsl(30, 15%, 82%);

  /* 點綴色：桜色（櫻花粉） */
  --color-accent: hsl(350, 60%, 72%);

  /* 擴充和色 */
  --color-sakura: hsl(350, 60%, 82%);       /* 桜色 */
  --color-fuji: hsl(270, 30%, 72%);          /* 藤色（紫藤） */
  --color-matcha: hsl(120, 25%, 55%);        /* 抹茶色 */
  --color-kohaku: hsl(35, 70%, 55%);         /* 琥珀色 */
  --color-asagi: hsl(190, 45%, 55%);         /* 浅葱色（淺蔥藍） */
  --color-sumi: hsl(220, 10%, 25%);          /* 墨色 */
}
```

**深色主題 — 墨夜風**
```css
[data-theme="dark"] {
  --color-primary: hsl(215, 45%, 60%);
  --color-primary-light: hsl(215, 50%, 72%);
  --color-bg: hsl(220, 15%, 12%);
  --color-surface: hsl(220, 12%, 18%);
  --color-text: hsl(40, 20%, 88%);
  --color-text-muted: hsl(40, 10%, 55%);
  --color-border: hsl(220, 10%, 25%);
  --color-accent: hsl(350, 55%, 68%);
}
```

#### 字體
- 使用 Google Fonts，推薦日系風格字體：
  - 標題：`Zen Maru Gothic`（圓體，柔和感）、`Noto Serif JP`（明朝體，典雅感）
  - 內文：`Noto Sans JP`、`Zen Kaku Gothic New`
  - 中文搭配：`Noto Sans TC`
  - 英文輔助：`Inter`（簡潔配搭）
- 在 `<head>` 中引入：
```html
<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@400;500;700&family=Noto+Serif+JP:wght@400;600;700&family=Noto+Sans+JP:wght@300;400;500;700&family=Inter:wght@300;400;500;600&family=Noto+Sans+TC:wght@300;400;500;700&display=swap" rel="stylesheet">
```
- 字體使用建議：
```css
body {
  font-family: 'Noto Sans JP', 'Noto Sans TC', 'Inter', sans-serif;
  letter-spacing: 0.02em; /* 日文排版微調字距 */
}
h1, h2, h3 {
  font-family: 'Zen Maru Gothic', 'Noto Sans JP', sans-serif;
  /* 或使用明朝體獲得更正式的感覺：*/
  /* font-family: 'Noto Serif JP', serif; */
}
```

#### 佈局
- 使用 CSS Grid 或 Flexbox 進行排版
- 設定合理的 max-width 和 margin auto 置中
- 使用 `clamp()` 做流體排版
```css
h1 { font-size: clamp(1.8rem, 4vw, 3rem); }
```

#### 動畫與互動
必須加入以下效果提升使用體驗，風格以「含蓄、優雅、自然」為主：
- **Hover 效果**：柔和的浮起與淡色變化（避免過度跳動）
- **入場動畫**：使用 `@keyframes` + `animation`，偏好 `fade-in` + 輕微 `translateY`，模擬自然飄落感
- **平滑過渡**：所有互動元素加上 `transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1)`
- **和紙質感卡片**（替代 Glassmorphism）：
```css
.washi-card {
  background: linear-gradient(
    135deg,
    hsl(40, 30%, 96%) 0%,
    hsl(40, 25%, 92%) 100%
  );
  border: 1px solid hsl(30, 20%, 85%);
  border-radius: 12px;
  box-shadow:
    0 1px 3px rgba(0, 0, 0, 0.04),
    0 4px 12px rgba(0, 0, 0, 0.03);
}

/* 深色模式下的障子風格（半透明和紙感） */
[data-theme="dark"] .washi-card {
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.08);
}
```
- **櫻花飄落微動畫**（適時使用於裝飾）：
```css
@keyframes sakura-fall {
  0% { transform: translateY(-10%) rotate(0deg); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
}
```

#### 響應式設計
```css
/* Mobile first */
@media (min-width: 768px) { /* Tablet */ }
@media (min-width: 1024px) { /* Desktop */ }
```

#### 必須包含的 HTML 元素
- `<meta charset="UTF-8">`
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- 描述性的 `<title>`
- 語義化標籤：`<header>`, `<main>`, `<section>`, `<nav>`, `<footer>`
- 所有互動元素必須有唯一的 `id`

### Step 4：預覽與迭代
- 使用 browser 工具開啟畫面預覽
- 截圖讓使用者確認
- 根據回饋調整

## 設計參考模板

### 和風 Dashboard 風格
適用於：後台管理、數據面板、監控頁面
- 和紙色背景 + 藍鼠 / 桜色 accent
- 和紙質感卡片佈局 + 柔和圓角（12px）
- 留白充足，呼應「間」的美學
- 資料表格使用細緻的墨色邊線
- 圖表色彩使用和色系列（藤、浅葱、抹茶、琥珀）

### 和風 Landing Page 風格
適用於：產品介紹、活動頁面、個人網站
- Hero section：大面積留白 + 優雅字體 + 淡色漸層背景
- 裝飾元素：可加入幾何和柄（麻の葉、青海波）作為背景紋樣
- Features section：icon 使用線條風格（stroke-based），配色和色
- 自然意象的分隔：使用波浪線或山形 SVG divider
- Footer 簡潔典雅，使用墨色背景 + 和紙色文字

### 和風 Form 風格
適用於：登入頁、註冊頁、問卷表單
- 置中的和紙質感表單卡片
- 輸入框使用底線式（underline style）設計，呼應書道感
- Label 使用柔和的墨色，placeholder 使用薄墨色
- 聚焦時邊框使用浅葱色或藤色
- Submit 按鈕：圓角 + 藍鼠色背景 + hover 時微微浮起

### 侘寂（Wabi-Sabi）極簡風格
適用於：作品集、部落格、藝術展示
- 大量留白，最小化視覺元素
- 使用不對稱佈局，模擬自然的不完美感
- 配色僅 2-3 色：墨色 + 和紙色 + 一個點綴色
- 字體使用明朝體（Noto Serif JP）增添文化質感
- 圖片搭配柔和陰影，避免銳利邊框

## 日系設計原則提醒
- 🎋 **間（Ma）**：善用留白，讓畫面呼吸
- 🌸 **侘寂（Wabi-Sabi）**：接受不完美，追求自然質樸之美
- 🏯 **整（Sei）**：整齊有序，元素對齊精確
- 🍵 **渋い（Shibui）**：含蓄優雅，避免過度裝飾

## 禁止事項
- ❌ 不使用 TailwindCSS（除非使用者明確要求）
- ❌ 不使用預設瀏覽器字體
- ❌ 不使用 placeholder 圖片（使用 generate_image 產生）
- ❌ 不產出看起來簡陋的 MVP
- ❌ 不在互動元素上省略 hover 效果
- ❌ 不使用高飽和度螢光色（違反日系含蓄美學）
- ❌ 不使用粗重的陰影（shadow 應柔和、自然）
- ❌ 避免過度動畫（動畫應如微風般輕柔）