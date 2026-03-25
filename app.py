import streamlit as st
from openai import OpenAI

# 页面配置
st.set_page_config(page_title="忽左忽右·AI排版工具", layout="wide")

st.title("🎙️ 播客排版工具 (AI 智能纠错版)")

# --- 1. 侧边栏配置 ---
with st.sidebar:
    st.header("🤖 AI 校对配置")
    api_key = st.text_input("DeepSeek API Key", type="password", help="在此输入 Key 以启用 AI 纠错")
    
    st.header("👤 角色定义")
    host_name = st.text_input("主持人姓名", value="程衍樑")
    guest_name = st.text_input("嘉宾姓名", value="刘愿")
    other_guests = st.text_input("其他角色", value="")
    
    st.header("🎨 颜色配置")
    color_host = st.color_picker("主持人颜色", "#79B9D9") 
    color_guest = st.color_picker("嘉宾颜色", "#47B04B")

# --- 2. AI 逻辑函数 ---
def ai_proofread(text, api_key):
    if not api_key:
        st.warning("请在左侧侧边栏输入 API Key 以进行 AI 校对。")
        return text
    
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    # 你的核心指令：保留原意，去口语化，改错别字
    prompt = """你是一个专业的播客文稿校对员。
任务：请帮我优化这段播客转录稿。
要求：
1. 去掉冗余的口语（如：嗯、那么、这个、就是、对不对、那样一个）。
2. 合并重复表达，修正明显的错别字和同音字错误。
3. 严格保留原有的观点和逻辑，不要增加或删除原意。
4. 保持段落和对话角色的完整性，直接输出修改后的文本，不要带有任何解释或评价。"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.3 # 保持较低的随机性
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"AI 调用出错: {str(e)}")
        return text

# --- 3. 渲染逻辑函数 ---
def render_block_html(main_title, raw_script, host, guest, others, h_color, g_color):
    if not raw_script.strip() and not main_title.strip(): return ""
    all_guests = [guest] + [x.strip() for x in others.split('，') if x.strip()]
    lines = raw_script.split('\n')
    
    html = f"""<p style="text-align: center; margin: 20px 0 0 0;"><span style="color: #3E8AB8; font-size: 16px; font-weight: bold; letter-spacing: 1.5px;">{main_title}</span></p>"""
    html += '<p style="min-height: 1.5em; margin: 0;"></p>' * 3
    
    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            html += '<p style="min-height: 1.5em; margin: 0;"></p>'
            continue
            
        is_host = clean_line == host or clean_line.startswith(f"{host}：") or clean_line.startswith(f"{host}:")
        is_guest = any(clean_line == g or clean_line.startswith(f"{g}：") or clean_line.startswith(f"{g}:") for g in all_guests)
        
        if is_host or is_guest:
            name = host if is_host else (clean_line.replace('：','').replace(':',''))
            html += f"""<p style="margin-top: 28px; margin-bottom: 10px; line-height: 1;"><span style="background-color: {'#79B9D9' if is_host else '#47B04B'}; color: #ffffff; font-size: 15px; font-weight: bold; padding: 1px 2px;">{name}</span></p>"""
        else:
            html += f"""<p style="margin: 0; text-align: justify; line-height: 200%; letter-spacing: 0.5px;"><span style="font-size: 14px; color: #000000;">{clean_line}</span></p>"""
    return html

# --- 4. 模块循环渲染 ---
all_blocks_html = []

# 初始化 session_state 存储文本
for i in range(1, 4):
    if f"script_{i}" not in st.session_state:
        st.session_state[f"script_{i}"] = ""

for i in range(1, 4):
    st.subheader(f"📍 模块 {i}")
    col_in, col_pre = st.columns([1, 1])
    
    with col_in:
        m_title = st.text_input(f"标题 {i}", value=f"标题内容 {i}", key=f"t_{i}")
        
        # 使用 session_state 绑定 text_area
        m_script = st.text_area(f"文稿 {i}", height=250, key=f"s_{i}", value=st.session_state[f"script_{i}"])
        st.session_state[f"script_{i}"] = m_script # 同步
        
        # AI 纠错按钮
        if st.button(f"✨ AI 轻量校对（模块 {i}）", key=f"ai_btn_{i}"):
            with st.spinner("AI 正在优化口语并修正错别字..."):
                optimized_text = ai_proofread(m_script, api_key)
                st.session_state[f"script_{i}"] = optimized_text
                st.rerun() # 强制刷新页面显示新文本

    current_html = render_block_html(m_title, st.session_state[f"script_{i}"], host_name, guest_name, other_guests, color_host, color_guest)
    all_blocks_html.append(current_html)
    
    with col_pre:
        st.caption("分模块预览")
        st.components.v1.html(f"""<div style="border:1px solid #eee; padding:10px; background:white;">{current_html if current_html else '等待输入...'}</div>""", height=350, scrolling=True)
    st.markdown("---")

# --- 5. 底部合并 ---
st.header("🚀 全文合并导出")
full_combined_html = "".join(all_blocks_html)

if full_combined_html.strip():
    st.components.v1.html(f"""
        <div style="margin-bottom: 20px; text-align: center;">
            <button onclick="copyFull()" style="padding: 15px 40px; background-color: #07c160; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 18px; font-weight: bold;">
                🔥 点击一键复制“全文”
            </button>
            <p id="full_msg" style="color: #07c160; font-weight: bold; margin-top: 10px;"></p>
        </div>
        <div style="border: 2px solid #07c160; padding: 20px; background: white;">
            <div id="full_area">{full_combined_html}</div>
        </div>
        <script>
        function copyFull() {{
            const node = document.getElementById('full_area');
            const range = document.createRange();
            range.selectNode(node);
            window.getSelection().removeAllRanges();
            window.getSelection().addRange(range);
            document.execCommand('copy');
            document.getElementById('full_msg').innerText = "✅ 全文已成功复制！";
            setTimeout(() => {{ document.getElementById('full_msg
