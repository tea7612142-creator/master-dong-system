import streamlit as st
import re
from lunar_python import Solar, Lunar

# -------------------------------------------------------------
# 1. 頁面配置 (設定標題，限制最大寬度)
# -------------------------------------------------------------
st.set_page_config(
    page_title="董大師 數字易經排盤系統",
    page_icon="📜",
    layout="wide"
)

# -------------------------------------------------------------
# 2. 自訂 CSS 樣式 (日系 MUJI 質感風格 + 強制淺色保護 + 介面修正)
# -------------------------------------------------------------
st.markdown("""
<style>
    /* 全局背景：溫暖的日系米白紙感 */
    .stApp, body {
        background-color: #FBF9F5 !important;
        color: #333333 !important;
        font-family: "PingFang TC", "Noto Sans TC", "Microsoft JhengHei", sans-serif;
    }
    
    /* 限制整體內容最大寬度與留白 */
    .block-container {
        max-width: 900px !important;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
    }

    /* 隱藏輸入框內的 "Press Enter to submit form" 提示文字 */
    [data-testid="stInputInstruction"],
    [data-testid="InputInstructions"] {
        display: none !important;
    }

    /* ----------------------------------------------------
       Tabs 頁籤切換（特別強化：解決手機深色模式字體隱藏問題）
       ---------------------------------------------------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: #EFEAE1 !important;
        padding: 6px !important;
        border-radius: 8px !important;
    }

    .stTabs [data-baseweb="tab"] {
        height: 42px !important;
        background-color: transparent !important;
        border-radius: 6px !important;
        border: none !important;
        flex: 1 !important;
        text-align: center !important;
    }

    /* 強制未選中的標籤文字為清晰深茶色 */
    .stTabs [data-baseweb="tab"] *,
    .stTabs button *,
    .stTabs p {
        color: #5C4A3E !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        opacity: 1 !important;
    }

    /* 選中的標籤：朱紅字白底 */
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.06) !important;
        border-radius: 6px !important;
    }

    .stTabs [aria-selected="true"] * {
        color: #A84438 !important;
        font-weight: 700 !important;
    }

    /* ----------------------------------------------------
       輸入框與按鈕（淺色模式保護與排版優化）
       ---------------------------------------------------- */
    label, [data-testid="stWidgetLabel"] p {
        color: #4A3B32 !important;
        font-weight: 600 !important;
        font-size: 15px !important;
    }

    div[data-baseweb="input"],
    div[data-baseweb="base-input"],
    .stNumberInput div {
        background-color: #FAF8F5 !important;
        color: #333333 !important;
        border-color: #DCD5C9 !important;
        border-radius: 6px !important;
    }

    .stNumberInput input {
        background-color: #FAF8F5 !important;
        color: #333333 !important;
        font-weight: 600 !important;
    }

    .stNumberInput button {
        background-color: #EFEAE1 !important;
        color: #4A3B32 !important;
        border: none !important;
    }

    .stButton > button,
    [data-testid="stFormSubmitButton"] > button,
    [data-testid="stFormSubmitButton"] button {
        background-color: #A84438 !important;
        color: #FFFFFF !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 10px 20px !important;
        width: 100% !important;
        box-shadow: 0 2px 6px rgba(168, 68, 56, 0.2) !important;
    }
    
    .stButton > button *,
    [data-testid="stFormSubmitButton"] button p {
        color: #FFFFFF !important;
    }

    /* 主標題 */
    .main-title {
        text-align: center;
        color: #4A3B32;
        font-size: 26px !important;
        font-weight: 600;
        letter-spacing: 2px;
        padding: 5px 0;
        margin-bottom: 20px;
        border-bottom: 2px solid #E2DACD;
        display: inline-block;
    }
    .title-wrapper { text-align: center; }

    /* 表單外層 */
    [data-testid="stForm"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E8E2D5 !important;
        border-radius: 8px !important;
        padding: 18px 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02) !important;
    }

    .panel-header {
        color: #4A3B32 !important;
        font-size: 18px;
        font-weight: 600;
        letter-spacing: 1px;
        margin-top: 10px;
        margin-bottom: 12px;
        padding-bottom: 6px;
        border-bottom: 1px solid #F0EAE1;
    }

    .section-subcaption {
        color: #7A6B5D !important;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 8px;
        margin-top: 12px;
        letter-spacing: 0.5px;
    }

    /* 矩陣容器 */
    .matrix-container {
        background-color: #FAF8F5 !important;
        border: 1px solid #EFEAE1 !important;
        border-radius: 6px;
        padding: 15px;
        margin-bottom: 15px;
    }

    .matrix-row {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 12px;
        margin: 4px 0;
    }
    
    /* 神煞卡片 */
    .star-box {
        border: 1px solid #DCD5C9 !important;
        background-color: #FFFFFF !important;
        border-radius: 4px;
        width: 64px;
        height: 64px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
        flex-shrink: 0;
    }
    
    /* 核心格局星 (朱紅框標示) */
    .star-box-core {
        border: 1.5px solid #A84438 !important;
        background-color: #FFFBFB !important;
        border-radius: 4px;
        width: 64px;
        height: 64px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
        flex-shrink: 0;
    }
    
    .star-top, .star-bottom { 
        font-size: 16px; 
        font-weight: 600; 
        color: #333333 !important; 
        line-height: 1.15;
    }
    
    .star-mark { 
        position: absolute;
        top: 2px;
        right: 4px;
        font-size: 10px; 
        font-weight: bold; 
        color: #A84438 !important; 
    }

    .matrix-divider {
        width: 75%;
        margin: 8px auto;
        border: 0;
        border-top: 1px dashed #DCD5C9;
    }

    .layout-box {
        background-color: #FAF8F5 !important;
        border: 1px solid #EFEAE1 !important;
        border-radius: 6px;
        padding: 12px 18px;
        margin-bottom: 15px;
        min-height: 48px;
    }

    .tk-fieldset {
        border: 1px solid #C4C4C4 !important;
        padding: 8px 12px 12px 12px;
        margin-top: 15px;
        margin-bottom: 5px;
        border-radius: 2px;
        background-color: #F7F5F0 !important; 
    }
    .tk-legend {
        font-size: 13px;
        font-weight: 600;
        color: #333333 !important;
        padding: 0 6px;
        width: auto;
        margin-bottom: 0;
        line-height: 1;
    }
    .tk-text-area {
        background-color: #FFFFFF !important;
        border: 1px solid #A9A9A9 !important; 
        padding: 10px;
        font-family: monospace;
        font-size: 13px;
        color: #111111 !important;
        white-space: pre-wrap;
        height: 180px;
        overflow-y: auto;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 3. 八星對照表與算盤邏輯
# -------------------------------------------------------------
STAR_MAP = {
    '11': ('比肩', '最強'), '22': ('比肩', '最強'),
    '88': ('比肩', '強'),   '99': ('比肩', '強'),
    '66': ('比肩', '次強'), '77': ('比肩', '次強'),
    '33': ('比肩', '弱'),   '44': ('比肩', '弱'),
    
    '14': ('正印', '最強'), '41': ('正印', '最強'),
    '67': ('正印', '強'),   '76': ('正印', '強'),
    '39': ('正印', '次強'), '93': ('正印', '次強'),
    '28': ('正印', '弱'),   '82': ('正印', '弱'),

    '13': ('食神', '最強'), '31': ('食神', '最強'),
    '68': ('食神', '強'),   '86': ('食神', '強'),
    '49': ('食神', '次強'), '94': ('食神', '次強'),
    '27': ('食神', '弱'),   '72': ('食神', '弱'),

    '19': ('正官', '最強'), '91': ('正官', '最強'),
    '78': ('正官', '強'),   '87': ('正官', '強'),
    '34': ('正官', '次強'), '43': ('正官', '次強'),
    '26': ('正官', '弱'),   '62': ('正官', '弱'),

    '17': ('七煞', '最強'), '71': ('七煞', '最強'),
    '89': ('七煞', '強'),   '98': ('七煞', '強'),
    '46': ('七煞', '次強'), '64': ('七煞', '次強'),
    '23': ('七煞', '弱'),   '32': ('七煞', '弱'),

    '16': ('偏印', '最強'), '61': ('偏印', '最強'),
    '47': ('偏印', '強'),   '74': ('偏印', '強'),
    '38': ('偏印', '次強'), '83': ('偏印', '次強'),
    '29': ('偏印', '弱'),   '92': ('偏印', '弱'),

    '12': ('傷官', '最強'), '21': ('傷官', '最強'),
    '69': ('傷官', '強'),   '96': ('傷官', '強'),
    '48': ('傷官', '次強'), '84': ('傷官', '次強'),
    '37': ('傷官', '弱'),   '73': ('傷官', '弱'),

    '18': ('劫財', '最強'), '81': ('劫財', '最強'),
    '97': ('劫財', '強'),   '79': ('劫財', '強'),
    '36': ('劫財', '次強'), '63': ('劫財', '次強'),
    '24': ('劫財', '弱'),   '42': ('劫財', '弱'),
}

COMPOUND_PATTERN_MAP = {
    19: "正官格", 28: "比肩格", 29: "比肩格",
    37: "傷官格", 38: "比肩格", 39: "傷官格",
    46: "七煞格", 47: "比肩格", 48: "傷官格"
}

TOP_ROW_STARS = {"比肩", "正印", "食神", "正官"}
BOTTOM_ROW_STARS = {"七煞", "偏印", "傷官", "劫財"}

HIDDEN_ENERGY_MAP = {
    "正官": "七煞", "正印": "偏印", "比肩": "劫財", "食神": "劫財",
    "七煞": "正官", "偏印": "正印", "劫財": "比肩", "傷官": "食神"
}

def process_digits_and_pairs(year: int, month: int, day: int):
    year_s, month_s, day_s = str(abs(year)), str(abs(month)), str(abs(day))
    raw_seq = f"{year_s}{month_s}{day_s}"
    pairs_info = []

    has_day_five = '5' in day_s

    i = 0
    n = len(raw_seq)
    
    while i < n - 1:
        current_char = raw_seq[i]
        
        if current_char == '5':
            i += 1
            continue

        if raw_seq[i+1] == '5':
            j = i + 1
            while j < n and raw_seq[j] == '5':
                j += 1
            
            if j < n:
                prev_d, next_d = raw_seq[i], raw_seq[j]
                pair = prev_d + next_d
                star_name, strength = ("比肩", "強") if '0' in pair else STAR_MAP.get(pair, (None, None))
                fives = raw_seq[i+1:j]
                if star_name:
                    pairs_info.append({
                        "pair": f"{prev_d}{fives}{next_d}➔{pair}", 
                        "star": star_name, 
                        "strength": strength, 
                        "is_infinite": True
                    })
                i = j - 1
            else:
                pair = current_char + '5'
                pairs_info.append({
                    "pair": f"{current_char}5➔比肩", 
                    "star": "比肩", 
                    "strength": "強", 
                    "is_infinite": False
                })
                i = j
        else:
            pair = raw_seq[i:i+2]
            star_name, strength = ("比肩", "強") if '0' in pair else STAR_MAP.get(pair, (None, None))
            if star_name:
                pairs_info.append({
                    "pair": pair, 
                    "star": star_name, 
                    "strength": strength, 
                    "is_infinite": False
                })
            i += 1

    if has_day_five:
        pairs_info.append({
            "pair": f"{day_s}➔日期含5視為比肩", 
            "star": "比肩", 
            "strength": "強", 
            "is_infinite": False
        })

    return raw_seq, pairs_info

def calculate_destiny_chart(year: int, month: int, day: int):
    raw_seq, pairs_info = process_digits_and_pairs(year, month, day)
    
    full_digits = [int(ch) for ch in raw_seq if ch.isdigit()]
    pattern_num = sum(full_digits)
    
    goal_num = pattern_num
    while goal_num >= 10:
        goal_num = sum(int(c) for c in str(goal_num))
        
    if pattern_num in COMPOUND_PATTERN_MAP:
        pattern_name = COMPOUND_PATTERN_MAP[pattern_num]
    else:
        p_pair = str(pattern_num)
        star = STAR_MAP.get(p_pair, ("比肩", "普通"))[0]
        pattern_name = f"{star}格"

    core_pattern_star = pattern_name.replace("格", "")

    star_counts = {}
    star_has_infinite = {}
    for p in pairs_info:
        s_name = p['star']
        star_counts[s_name] = star_counts.get(s_name, 0) + 1
        if p['is_infinite']:
            star_has_infinite[s_name] = True

    processed_stars = []
    visited = set()
    for p in pairs_info:
        s_name = p['star']
        if s_name in visited: continue
        visited.add(s_name)
        count = star_counts[s_name]
        mark = "∞" if star_has_infinite.get(s_name, False) else (str(count) if count > 1 else "")
        processed_stars.append({
            "name": s_name,
            "top_char": s_name[0] if len(s_name) > 0 else "",
            "bottom_char": s_name[1] if len(s_name) > 1 else "",
            "mark": mark,
            "is_hidden": False
        })

    top_stars = [s for s in processed_stars if s['name'] in TOP_ROW_STARS]
    bottom_stars = [s for s in processed_stars if s['name'] in BOTTOM_ROW_STARS]
    
    num_cols = max(len(top_stars), len(bottom_stars))
    if num_cols == 0: num_cols = 1
    
    matrix_top = [None] * num_cols
    matrix_bottom = [None] * num_cols

    for t_idx, star in enumerate(top_stars):
        if t_idx < num_cols: matrix_top[t_idx] = star
    for b_idx, star in enumerate(bottom_stars):
        if b_idx < num_cols: matrix_bottom[b_idx] = star

    for c in range(num_cols):
        if matrix_top[c] is not None and matrix_bottom[c] is None:
            hidden_name = HIDDEN_ENERGY_MAP.get(matrix_top[c]['name'], "")
            if hidden_name:
                matrix_bottom[c] = {"name": hidden_name, "top_char": hidden_name[0], "bottom_char": hidden_name[1], "mark": "x", "is_hidden": True}
        elif matrix_bottom[c] is not None and matrix_top[c] is None:
            hidden_name = HIDDEN_ENERGY_MAP.get(matrix_bottom[c]['name'], "")
            if hidden_name:
                matrix_top[c] = {"name": hidden_name, "top_char": hidden_name[0], "bottom_char": hidden_name[1], "mark": "x", "is_hidden": True}

    grid_2d = [matrix_top, matrix_bottom]
    core_r, core_c = -1, -1
    core_item = None
    has_exact_pattern_star = False

    # 1. 優先尋找原格局星
    for r in range(2):
        for c in range(num_cols):
            item = grid_2d[r][c]
            if item and item['name'] == core_pattern_star and not item.get('is_hidden', False):
                core_r, core_c, core_item, has_exact_pattern_star = r, c, item, True
                break
        if core_r != -1: break

    # 2. 未入格修正：取最後一個拆解組合（末位星）做為核心星
    if not has_exact_pattern_star:
        pattern_name = f"{pattern_name}-未入格"
        fallback_star_name = None
        # 倒序尋找最後一個有星號的組合（避開非星號標記）
        for p in reversed(pairs_info):
            if p.get('star'):
                fallback_star_name = p['star']
                break
        
        if fallback_star_name:
            for r in range(2):
                for c in range(num_cols):
                    item = grid_2d[r][c]
                    if item and item['name'] == fallback_star_name and not item.get('is_hidden', False):
                        core_r, core_c, core_item = r, c, item
                        break
                if core_r != -1: break

    pattern_layout_tuples = []
    # 十字格局能量排列計算 (有原格局星或末位備用星皆可計算)
    if core_item:
        opp_r = 1 if core_r == 0 else 0
        pattern_layout_tuples.append(("+", f"{core_item['name']}{core_item['mark']}"))

        opp_side_items = [grid_2d[opp_r][c]['name'] + grid_2d[opp_r][c]['mark'] for c in (core_c - 1, core_c + 1) if 0 <= c < num_cols and grid_2d[opp_r][c]]
        if opp_side_items: pattern_layout_tuples.append(("-", " ".join(opp_side_items)))

        opp_item = grid_2d[opp_r][core_c]
        if opp_item: pattern_layout_tuples.append(("+", f"{opp_item['name']}{opp_item['mark']}"))

        same_side_items = [grid_2d[core_r][c]['name'] + grid_2d[core_r][c]['mark'] for c in (core_c - 1, core_c + 1) if 0 <= c < num_cols and grid_2d[core_r][c]]
        if same_side_items: pattern_layout_tuples.append(("-", " ".join(same_side_items)))

    clean_top = [item for item in matrix_top if item is not None]
    clean_bottom = [item for item in matrix_bottom if item is not None]

    return {
        "raw_seq": raw_seq,
        "pattern_num": pattern_num,
        "goal_num": f"{goal_num}號人",
        "pattern_name": pattern_name,
        "core_item": core_item,
        "matrix_top": clean_top,
        "matrix_bottom": clean_bottom,
        "pairs_info": pairs_info,
        "pattern_layout_tuples": pattern_layout_tuples
    }

# -------------------------------------------------------------
# 4. Web UI 渲染模組
# -------------------------------------------------------------
def build_star_box_html(item, core_item):
    if not item: return ''
    is_core = (core_item is not None and item == core_item)
    box_class = "star-box-core" if is_core else "star-box"
    mark_html = f'<div class="star-mark">{item["mark"]}</div>' if item["mark"] else ''
    return f'<div class="{box_class}">{mark_html}<div class="star-top">{item["top_char"]}</div><div class="star-bottom">{item["bottom_char"]}</div></div>'

def render_panel(res, title_prefix, date_desc):
    core_item = res['core_item']
    top_boxes_html = "".join([build_star_box_html(item, core_item) for item in res['matrix_top']])
    bottom_boxes_html = "".join([build_star_box_html(item, core_item) for item in res['matrix_bottom']])

    st.markdown(f"<div class='panel-header'>〔 {title_prefix}排盤結果 〕</div>", unsafe_allow_html=True)
    
    st.markdown(f"<div class='section-subcaption'>{title_prefix} ‧ 神煞排盤矩陣</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="matrix-container">
        <div class="matrix-row">{top_boxes_html}</div>
        <hr class="matrix-divider">
        <div class="matrix-row">{bottom_boxes_html}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div class='section-subcaption'>{title_prefix} ‧ 格局能量排列</div>", unsafe_allow_html=True)
    
    layout_html = "<div class='layout-box'>"
    if res['pattern_layout_tuples']:
        for sign, content in res['pattern_layout_tuples']:
            layout_html += f"<div style='margin: 4px 0;'><span style='color:#A84438; font-size: 16px; font-weight:600;'>{sign} &nbsp; {content}</span></div>"
    else:
        layout_html += "<div style='color:#888888; font-size:14px;'>無能量排列組合（未入格）</div>"
    layout_html += "</div>"
    st.markdown(layout_html, unsafe_allow_html=True)

    detail_text = f"{date_desc}\n"
    detail_text += f"【處理後數字串】: {res['raw_seq']}\n"
    detail_text += f"【格局數】: {res['pattern_num']}  |  【目標數】: {res['goal_num']}  |  【格局】: {res['pattern_name']}\n"
    detail_text += "--------------------------------------------------\n"
    detail_text += "【兩兩拆解與歸類詳情】:\n"
    for p in res['pairs_info']:
        inf_tag = " [無限大 ∞]" if p['is_infinite'] else ""
        detail_text += f"  • 組合 [{p['pair']}] ➔ {p['star']} ({p['strength']}){inf_tag}\n"
    
    st.markdown(f"""
    <fieldset class="tk-fieldset">
        <legend class="tk-legend">{title_prefix} - 詳細計算過程</legend>
        <div class="tk-text-area">{detail_text}</div>
    </fieldset>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 5. 主畫面介面
# -------------------------------------------------------------
st.markdown("<div class='title-wrapper'><div class='main-title'>董大師 數字易經排盤系統</div></div>", unsafe_allow_html=True)

with st.form("birth_form"):
    col_y, col_m, col_d = st.columns(3)
    with col_y:
        year = st.number_input("國曆西元年", min_value=1900, max_value=2100, value=1976, step=1)
    with col_m:
        month = st.number_input("月", min_value=1, max_value=12, value=7, step=1)
    with col_d:
        day = st.number_input("日", min_value=1, max_value=31, value=17, step=1)
    
    st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
    submit_btn = st.form_submit_button("一 鍵 自 動 排 盤")

# 執行計算
solar_res = calculate_destiny_chart(year, month, day)
solar_obj = Solar.fromYmd(year, month, day)
lunar_obj = solar_obj.getLunar()
ly, lm, ld = lunar_obj.getYear(), lunar_obj.getMonth(), lunar_obj.getDay()

# 閏月判定與顯示優化
is_leap = "閏" if lm < 0 else ""
lunar_res = calculate_destiny_chart(ly, abs(lm), ld)

# 切換頁籤 (國曆/農曆)
tab1, tab2 = st.tabs(["國曆排盤結果", "農曆排盤結果"])

with tab1:
    render_panel(solar_res, "國曆", f"【國曆生日】: {year}年{month}月{day}日")

with tab2:
    render_panel(lunar_res, "農曆", f"【自動轉換農曆】: {ly}年{is_leap}{abs(lm)}月{ld}日 (對應國曆 {year}/{month}/{day})")
