import streamlit as st
from openai import OpenAI

# 页面配置
st.set_config = st.set_page_config(page_title="忽左忽右·AI排版工具", layout="wide")

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
    
    # 兼容 OpenAI 格式的调用
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
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
            temperature=0.3
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
    
    html = f'<p style="text-align: center; margin: 20px 0 0 0;"><span style="color: #3E8AB8; font-size: 16px; font-weight: bold; letter-spacing: 1.5px;">{main_title}</span></p>'
    html += '<p style="min-height: 1.5em; margin: 0;"></p>' * 3
    
    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            html += '<p style="min-height: 1.5em; margin: 0;"></p>'
