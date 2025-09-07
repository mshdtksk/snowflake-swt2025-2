import streamlit as st
import math
import random

# ページ設定
st.set_page_config(
    page_title="Snowflake 知識の呼吸 - クロスワードの型",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# カスタムCSS - 鬼滅の刃風デザイン
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&display=swap');
    
    .main {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    h1, h2, h3 {
        font-family: 'Noto Serif JP', serif !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .crossword-container {
        display: flex;
        justify-content: center;
        margin: 20px 0;
        filter: drop-shadow(0 0 20px rgba(138, 43, 226, 0.3));
    }
    
    .crossword-table {
        border-collapse: collapse;
        border: 3px solid #8a2be2;
        background: rgba(255, 255, 255, 0.95);
        box-shadow: 0 0 30px rgba(138, 43, 226, 0.5);
    }
    
    .crossword-cell {
        width: 45px;
        height: 45px;
        border: 1px solid #666;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        position: relative;
        background-color: white;
        transition: all 0.3s ease;
    }
    
    .crossword-cell:hover {
        background-color: rgba(138, 43, 226, 0.1);
        transform: scale(1.05);
    }
    
    .black-cell {
        background: linear-gradient(135deg, #2c003e 0%, #1a0033 100%) !important;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
    }
    
    .special-cell {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%) !important;
        color: white !important;
        box-shadow: 0 0 15px rgba(231, 76, 60, 0.7);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 15px rgba(231, 76, 60, 0.7); }
        50% { box-shadow: 0 0 25px rgba(231, 76, 60, 1); }
        100% { box-shadow: 0 0 15px rgba(231, 76, 60, 0.7); }
    }
    
    .number-label {
        font-size: 10px;
        position: absolute;
        top: 2px;
        left: 3px;
        color: #8a2be2;
        font-weight: bold;
        text-shadow: 1px 1px 1px rgba(255,255,255,0.8);
    }
    
    .special-cell .number-label {
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    
    .correct {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
        animation: correctFlash 0.5s ease;
    }
    
    @keyframes correctFlash {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .red-cell-display {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(231, 76, 60, 0.4);
        font-family: 'Noto Serif JP', serif;
        position: relative;
        overflow: hidden;
    }
    
    .red-cell-display::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .stats-container {
        background: linear-gradient(135deg, rgba(138, 43, 226, 0.1) 0%, rgba(138, 43, 226, 0.2) 100%);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        border: 2px solid rgba(138, 43, 226, 0.3);
        box-shadow: 0 5px 20px rgba(138, 43, 226, 0.2);
    }
    
    .hint-display {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: 2px solid #8a2be2;
        border-radius: 8px;
        padding: 10px;
        margin: 10px 0;
        font-family: monospace;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        box-shadow: 0 5px 15px rgba(138, 43, 226, 0.3);
        letter-spacing: 3px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        font-weight: bold;
        transition: all 0.3s ease;
        font-family: 'Noto Serif JP', serif;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(138, 43, 226, 0.4);
    }
    
    .breath-title {
        background: linear-gradient(90deg, #e74c3c, #8a2be2, #3498db, #e74c3c);
        background-size: 300% 100%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 5s ease infinite;
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
        font-family: 'Noto Serif JP', serif;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .invisible-button {
        position: fixed;
        bottom: 5px;
        right: 5px;
        width: 20px;
        height: 20px;
        opacity: 0;
        cursor: default;
        z-index: -9999;
        pointer-events: none;
    }
    
    /* 特殊な条件でのみボタンを有効化（開発者用） */
    .invisible-button:focus {
        pointer-events: auto;
        opacity: 0.01;
    }
    
    .problem-statement {
        background: rgba(0, 0, 0, 0.3);
        border-left: 4px solid #e74c3c;
        padding: 20px;
        margin: 20px 0;
        border-radius: 10px;
        color: white;
        font-style: italic;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

def initialize_hint_system():
    """ヒントシステムの初期化"""
    if 'hint_uses' not in st.session_state:
        st.session_state.hint_uses = 0
    
    if 'total_mistakes' not in st.session_state:
        st.session_state.total_mistakes = 0
    
    if 'hint_enabled' not in st.session_state:
        st.session_state.hint_enabled = False
    
    if 'used_hints' not in st.session_state:
        st.session_state.used_hints = {}

class SnowflakeCrossword:
    def __init__(self):
        # グリッドサイズ
        self.rows = 9
        self.cols = 13
        
        # 黒マスの位置
        self.black_cells = [
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1],
        ]
        
        # 特別なセル
        self.special_cells = {
            (1, 8): '1', (0, 3): '2', (7, 6): '3', (1, 11): '4',
            (5, 6): '5', (6, 1): '6', (8, 4): '7', (2, 6): '8',
            (3, 4): '9', (5, 9): '10'
        }
        
        # 答えの定義
        self.answers = {
            'across': {
                '水': {
                    'row': 0, 'col': 0, 'answer': 'HORIZON', 
                    'hint': 'Snowflakeのセマンティックカタログやガバナンス機能をまとめた名称',
                    'label': '水'
                },
                '蟲': {
                    'row': 2, 'col': 0, 'answer': 'INTELLIGENCE', 
                    'hint': '洞察を提供する安全なAIエージェント',
                    'label': '蟲'
                },
                '炎': {
                    'row': 8, 'col': 0, 'answer': 'SEARCH', 
                    'hint': 'Snowfoldの隠れた意識された用語ページ内・AI統合検索の補完機能',
                    'label': '炎'
                },
                '音': {
                    'row': 7, 'col': 4, 'answer': 'SUMMIT', 
                    'hint': 'Snowflake が年に一度開催している、グローバルイベントの名称',
                    'label': '音'
                },
                '恋': {
                    'row': 3, 'col': 2, 'answer': 'DBT', 
                    'hint': 'Snowsightから直接操作できる、データモデルパイプライン構築の統合環境',
                    'label': '恋'
                },
            },
            'down': {
                '蛇': {
                    'row': 0, 'col': 3, 'answer': 'ICEBERG', 
                    'hint': 'Snowflakeがサポートを強化しているオープンテーブルフォーマット',
                    'label': '蛇'
                },
                '風': {
                    'row': 1, 'col': 8, 'answer': 'SEMANTIC', 
                    'hint': '「ビジネス定義を含むビュー」を指すもの',
                    'label': '風'
                },
                '霞': {
                    'row': 1, 'col': 6, 'answer': 'AISQL', 
                    'hint': '自然言語を活用しながらSQLクエリを発行できる機能',
                    'label': '霞'
                },
                '岩': {
                    'row': 1, 'col': 9, 'answer': 'ANALYST', 
                    'hint': 'Snowflake が提供する生成 AI を活用した自然言語分析のためのツール',
                    'label': '岩'
                },
                '雷': {
                    'row': 1, 'col': 1, 'answer': 'SNOWPIPE', 
                    'hint': 'Snowflakeのリアルタイムデータ取り込みを担うサービス',
                    'label': '雷'
                },
                '火': {
                    'row': 0, 'col': 11, 'answer': 'OPENFLOW', 
                    'hint': '構造化・非構造化データやバッチ・ストリームの統合を簡素化する機能',
                    'label': '火'
                },
            }
        }
        
        # セッション状態の初期化
        if 'grid' not in st.session_state:
            st.session_state.grid = [['' for _ in range(self.cols)] for _ in range(self.rows)]
        
        if 'revealed' not in st.session_state:
            st.session_state.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        
        if 'completed' not in st.session_state:
            st.session_state.completed = False
        
        initialize_hint_system()

    def check_answer(self, direction, key):
        """答えをチェック"""
        if key not in self.answers[direction]:
            return False
            
        answer_info = self.answers[direction][key]
        user_answer = ""
        
        try:
            if direction == 'across':
                for i in range(len(answer_info['answer'])):
                    if answer_info['col'] + i < self.cols:
                        cell_value = st.session_state.grid[answer_info['row']][answer_info['col'] + i]
                        user_answer += cell_value if cell_value else ' '
            else:
                for i in range(len(answer_info['answer'])):
                    if answer_info['row'] + i < self.rows:
                        cell_value = st.session_state.grid[answer_info['row'] + i][answer_info['col']]
                        user_answer += cell_value if cell_value else ' '
        except IndexError:
            return False
        
        return user_answer.upper().strip() == answer_info['answer']

    def set_answer(self, direction, key, user_input):
        """ユーザーの入力をグリッドに設定"""
        if key not in self.answers[direction]:
            return
            
        answer_info = self.answers[direction][key]
        
        try:
            if direction == 'across':
                for i, char in enumerate(user_input.upper()):
                    if i < len(answer_info['answer']) and answer_info['col'] + i < self.cols:
                        if not self.black_cells[answer_info['row']][answer_info['col'] + i]:
                            st.session_state.grid[answer_info['row']][answer_info['col'] + i] = char
            else:
                for i, char in enumerate(user_input.upper()):
                    if i < len(answer_info['answer']) and answer_info['row'] + i < self.rows:
                        if not self.black_cells[answer_info['row'] + i][answer_info['col']]:
                            st.session_state.grid[answer_info['row'] + i][answer_info['col']] = char
        except IndexError:
            pass

    def reveal_answer(self, direction, key):
        """答えを表示"""
        if key not in self.answers[direction]:
            return
            
        answer_info = self.answers[direction][key]
        
        try:
            if direction == 'across':
                for i, char in enumerate(answer_info['answer']):
                    if answer_info['col'] + i < self.cols:
                        st.session_state.grid[answer_info['row']][answer_info['col'] + i] = char
                        st.session_state.revealed[answer_info['row']][answer_info['col'] + i] = True
            else:
                for i, char in enumerate(answer_info['answer']):
                    if answer_info['row'] + i < self.rows:
                        st.session_state.grid[answer_info['row'] + i][answer_info['col']] = char
                        st.session_state.revealed[answer_info['row'] + i][answer_info['col']] = True
        except IndexError:
            pass
    
    def reveal_all_answers(self):
        """すべての答えを表示"""
        for direction in ['across', 'down']:
            for key in self.answers[direction]:
                self.reveal_answer(direction, key)

    def check_completion(self):
        """すべての答えが正解かチェック"""
        for direction in ['across', 'down']:
            for key in self.answers[direction]:
                if not self.check_answer(direction, key):
                    return False
        return True
    
    def get_red_cells_content(self):
        """赤セルの内容を番号順に取得"""
        sorted_cells = sorted(self.special_cells.items(), key=lambda x: int(x[1]))
        result = []
        all_filled = True
        
        for (row, col), num in sorted_cells:
            content = st.session_state.grid[row][col]
            if content:
                result.append(content)
            else:
                result.append("_")
                all_filled = False
        
        display_text = "".join(result)
        
        if all_filled:
            return f"✨ {display_text} ✨"
        else:
            return display_text
    
    def generate_hint_for_answer(self, answer, reveal_ratio=0.3):
        """答えに対してヒントを生成"""
        if not answer:
            return ""
        
        answer_length = len(answer)
        reveal_count = max(1, math.ceil(answer_length * reveal_ratio))
        
        reveal_indices = [0]
        
        if reveal_count > 1 and answer_length > 1:
            remaining_indices = list(range(1, answer_length))
            random.shuffle(remaining_indices)
            reveal_indices.extend(remaining_indices[:reveal_count-1])
        
        reveal_indices.sort()
        
        masked_answer = []
        for i in range(answer_length):
            if i in reveal_indices:
                masked_answer.append(answer[i])
            else:
                masked_answer.append("_")
        
        return "".join(masked_answer)

def header_animation():
    """ヘッダーアニメーション"""
    st.markdown("""
        <div class="breath-title">
            ⚔️ Snowflake 最終問題-氷に閉ざされしワードを炎で解放せよ！-⚔️
        </div>
    """, unsafe_allow_html=True)

def display_problem_statement():
    """問題文の表示"""
    st.markdown("""
        <div class="problem-statement">
            <i>"雪の結晶に秘められた知識の刃を研ぎ澄ませ。<br/>
            データの呼吸を極めし者のみが、真の答えに辿り着く。"</i><br/><br/>
            
            【試練】
            Snowflakeの知識を試すクロスワードの型。
            横と縦に隠された言葉を解き明かし、
            赤き炎のマスに宿る文字を集めよ。
            
            【奥義】
            八度の過ちを重ねし時、秘められし力が解放される。
            されど、その力は四度までしか使えぬ諸刃の剣。
        </div>
    """, unsafe_allow_html=True)

def main():
    header_animation()
    st.header(":red[氷晶の鬼] 〜Snowflakeの呼吸・最終ノ型〜", divider="red")
    
    display_problem_statement()
    
    # パズルインスタンス作成
    puzzle = SnowflakeCrossword()
    
    # 8回以上間違えた場合にヒント機能を有効化
    if st.session_state.total_mistakes >= 8 and not st.session_state.hint_enabled:
        st.session_state.hint_enabled = True
    
    # 統計情報の表示
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    col_stats = st.columns(4)
    with col_stats[0]:
        st.metric("⚔️ 討伐失敗", st.session_state.total_mistakes)
    with col_stats[1]:
        if st.session_state.hint_enabled:
            st.metric("🔥 奥義使用", f"{st.session_state.hint_uses}/4")
        else:
            st.metric("🔥 奥義", "未解放")
    with col_stats[2]:
        correct_count = sum(1 for d in ['across', 'down'] for k in puzzle.answers[d] if puzzle.check_answer(d, k))
        total_count = sum(len(puzzle.answers[d]) for d in ['across', 'down'])
        st.metric("✨ 討伐成功", f"{correct_count}/{total_count}")
    #with col_stats[3]:
    #    if st.button("🔄 再挑戦", type="secondary"):
    #        for key in list(st.session_state.keys()):
    #            del st.session_state[key]
    #        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.hint_enabled and st.session_state.total_mistakes == 8:
        st.success("🔥 **奥義解放！** ヒントの呼吸が使用可能になった！（全体で四度まで）")
    
    # メインコンテンツ
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("⚔️ 試練の盤面")
        
        # 赤セルの内容を表示
        red_cells_content = puzzle.get_red_cells_content()
        st.markdown(f'<div class="red-cell-display">🔥 封印の文字: {red_cells_content}</div>', unsafe_allow_html=True)
        
        # グリッドのHTML生成
        grid_html = '<div class="crossword-container"><table class="crossword-table">'
        
        labels = {}
        for direction in ['across', 'down']:
            for key, info in puzzle.answers[direction].items():
                pos = (info['row'], info['col'])
                if pos not in labels:
                    labels[pos] = info['label']
        
        for pos, label in puzzle.special_cells.items():
            if pos in labels:
                labels[pos] = labels[pos] + '/' + label
            else:
                labels[pos] = label
        
        for row in range(puzzle.rows):
            grid_html += '<tr>'
            for col in range(puzzle.cols):
                if puzzle.black_cells[row][col] == 1:
                    cell_class = "crossword-cell black-cell"
                    cell_content = ""
                else:
                    if (row, col) in puzzle.special_cells:
                        cell_class = "crossword-cell special-cell"
                    else:
                        cell_class = "crossword-cell"
                        if st.session_state.revealed[row][col]:
                            cell_class += " correct"
                    
                    label = labels.get((row, col), "")
                    cell_content = st.session_state.grid[row][col]
                    if label:
                        if (row, col) in puzzle.special_cells:
                            cell_content = f'<span class="number-label" style="color: white !important;">{label}</span>' + cell_content
                        else:
                            cell_content = f'<span class="number-label">{label}</span>' + cell_content
                
                grid_html += f'<td class="{cell_class}">{cell_content}</td>'
            grid_html += '</tr>'
        
        grid_html += '</table></div>'
        st.markdown(grid_html, unsafe_allow_html=True)
        
        if puzzle.check_completion() and not st.session_state.completed:
            st.session_state.completed = True
            st.balloons()
            st.success("🎊 **完全討伐！** すべての試練を突破した！")
            st.info("🏆 Snowflakeの極意を会得せり！")
    
    with col2:
        st.subheader("📜 知識の巻物")
        
        tab1, tab2 = st.tabs(["横の型", "縦の型"])
        
        with tab1:
            direction = 'across'
            for key, info in puzzle.answers[direction].items():
                with st.expander(f"【{info['label']}】の試練", expanded=False):
                    st.write(f"**謎かけ:** {info['hint']}")
                    st.info(f"文字数: {len(info['answer'])}文字")
                    
                    hint_key = f"{direction}_{key}"
                    if hint_key in st.session_state.get('used_hints', {}):
                        st.markdown(f'<div class="hint-display">🔥 {st.session_state.used_hints[hint_key]}</div>', 
                                  unsafe_allow_html=True)
                    
                    col_input, col_check, col_hint = st.columns([5, 2, 2])
                    
                    with col_input:
                        user_input = st.text_input("答え", key=f"input_across_{key}", 
                                                  label_visibility="collapsed", placeholder="答えを入力")
                    
                    with col_check:
                        if st.button("⚔️ 討伐", key=f"check_across_{key}", use_container_width=True):
                            if user_input:
                                puzzle.set_answer(direction, key, user_input)
                                if puzzle.check_answer(direction, key):
                                    st.success("討伐成功！")
                                    puzzle.reveal_answer(direction, key)
                                    st.rerun()
                                else:
                                    st.error("討伐失敗！")
                                    st.session_state.total_mistakes += 1
                                    st.rerun()
                    
                    with col_hint:
                        if st.session_state.hint_enabled and st.session_state.hint_uses < 4:
                            if hint_key not in st.session_state.used_hints:
                                if st.button("🔥 奥義", key=f"hint_across_{key}", use_container_width=True):
                                    correct_answer = info['answer']
                                    masked_answer = puzzle.generate_hint_for_answer(correct_answer, reveal_ratio=0.3)
                                    st.session_state.used_hints[hint_key] = masked_answer
                                    st.session_state.hint_uses += 1
                                    st.rerun()
        
        with tab2:
            direction = 'down'
            for key, info in puzzle.answers[direction].items():
                with st.expander(f"【{info['label']}】の試練", expanded=False):
                    st.write(f"**謎かけ:** {info['hint']}")
                    st.info(f"文字数: {len(info['answer'])}文字")
                    
                    hint_key = f"{direction}_{key}"
                    if hint_key in st.session_state.get('used_hints', {}):
                        st.markdown(f'<div class="hint-display">🔥 {st.session_state.used_hints[hint_key]}</div>', 
                                  unsafe_allow_html=True)
                    
                    col_input, col_check, col_hint = st.columns([5, 2, 2])
                    
                    with col_input:
                        user_input = st.text_input("答え", key=f"input_down_{key}", 
                                                  label_visibility="collapsed", placeholder="答えを入力")
                    
                    with col_check:
                        if st.button("⚔️ 討伐", key=f"check_down_{key}", use_container_width=True):
                            if user_input:
                                puzzle.set_answer(direction, key, user_input)
                                if puzzle.check_answer(direction, key):
                                    st.success("討伐成功！")
                                    puzzle.reveal_answer(direction, key)
                                    st.rerun()
                                else:
                                    st.error("討伐失敗！")
                                    st.session_state.total_mistakes += 1
                                    st.rerun()
                    
                    with col_hint:
                        if st.session_state.hint_enabled and st.session_state.hint_uses < 4:
                            if hint_key not in st.session_state.used_hints:
                                if st.button("🔥 奥義", key=f"hint_down_{key}", use_container_width=True):
                                    correct_answer = info['answer']
                                    masked_answer = puzzle.generate_hint_for_answer(correct_answer, reveal_ratio=0.3)
                                    st.session_state.used_hints[hint_key] = masked_answer
                                    st.session_state.hint_uses += 1
                                    st.rerun()
    
    # 完全に見えない全答えボタン（キーボードショートカット Ctrl+Shift+Zで実行）
    if st.text_input("", key="secret_key", label_visibility="collapsed", 
                     placeholder="", max_chars=1, 
                     help=None) == "Z":
        puzzle.reveal_all_answers()
        st.rerun()

if __name__ == "__main__":
    main()