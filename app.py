import streamlit as st
from openai import OpenAI

# 页面配置
st.set_page_config(page_title="忽左忽右·AI全能排版", layout="wide")

# --- 1. 样式函数：保持你最满意的那个原生格式 ---
def render_block_html(main_title, raw_script, host, guest, others, h_color, g_color):
    if not raw_script.strip() and not main_title.strip(): return ""
    all_guests = [guest] + [x.strip() for x in others.split('，') if x.strip()]
    lines = raw_script.split('\n')
    
    # 标题：深蓝色 (#3E8AB8)，16px，居中，后空三行
    html = f'<p style="text-align: center; margin: 20px 0 0 0; line-height: 1.5;"><span style="color: #3E8AB8; font-size: 16px; font-weight: bold; letter-spacing: 1.5px;">{main_title}</span></p>'
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
            current_bg = h_color if is_host else g_color
            # 原生直角紧凑色块
            html += f'<p style="margin-top: 28px; margin-bottom: 10px; line-height: 1;"><span style="background-color: {current_bg}; color: #ffffff; font-size: 15px; font-weight: bold; padding: 1px 2px;">{name}</span></p>'
        else:
            # 正文：2.0倍行距，纯黑，0.5字距
            html += f'<p style="margin: 0; text-align: justify; line-height: 200%; letter-spacing: 0.5px;"><span style="font-size: 14px; color: #000000;">{clean_line}</span></p>'
    return html

# --- 2. AI 校对核心逻辑 ---
def ai_proofread(text, api_key):
    if not api_key:
        st.error("❌ 请先在左侧输入 DeepSeek API Key")
        return text
    
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    prompt = """你是一个专业的播客文稿校对员。要求：1.去掉冗余口语（嗯、那么、就是等）；2.修正错别字；3.严格保留原意和逻辑；4.直接输出修改后的文本。"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": text}],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"AI 调用失败: {e}")
        return text

# --- 3. 界面初始化 ---
st.title("🎙️ 播客排版工具 (AI 预览同步版)")

with st.sidebar:
    st.header("🤖 AI 配置")
    user_api_key = st.text_input("DeepSeek API Key", type="password")
    
    st.header("👤 角色定义")
    host_name = st.text_input("主持人姓名", value="程衍樑")
    guest_name = st.text_input("嘉宾姓名", value="刘愿")
    other_guests = st.text_input("其他角色", value="")
    
    st.header("🎨 颜色配置")
    c_host = st.color_picker("主持人颜色", "#79B9D9") 
    c_guest = st.color_picker("嘉宾颜色", "#47B04B")

# 初始化 session_state
for i in range(1, 4):
    if f"s_{i}" not in st.session_state: st.session_state[f"s_{i}"] = ""
    if f"t_{i}" not in st.session_state: st.session_state[f"t_{i}"] = f"示例标题 {i}"

# --- 4. 模块渲染 ---
all_blocks_html = []

for i in range(1, 4):
    st.markdown(f"### 📍 模块 {i}")
    col_in, col_pre = st.columns([1, 1])
    
    with col_in:
        # 标题输入
        st.session_state[f"t_{i}"] = st.text_input(f"标题 {i}", value=st.session_state[f"t_{i}"], key=f"title_input_{i}")
        
        # 文稿输入：绑定 session_state 确保 AI 修改后能显示
        txt = st.text_area(f"文稿内容 {i}", height=300, key=f"area_{i}", value=st.session_state[f"s_{i}"])
        st.session_
