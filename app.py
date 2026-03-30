import streamlit as st

# 页面配置
st.set_page_config(page_title="忽左忽右公众号排版工具", layout="wide")

st.title("🎙️ 忽左忽右公众号排版工具")

# 侧边栏：全局设置
with st.sidebar:
    st.header("👤 全局角色定义")
    host_name = st.text_input("主持人姓名", value="程衍樑")
    guest_name = st.text_input("嘉宾姓名", value="刘愿")
    other_guests = st.text_input("其他角色 (中文逗号隔开)", value="")
    
    st.header("🎨 全局颜色配置")
    color_host = st.color_picker("主持人背景色", "#79B9D9") 
    color_guest = st.color_picker("嘉宾背景色", "#47B04B")
    
    st.markdown("---")
    st.write("📌 **样式标准（已更新标题）：**")
    st.write("- 标题：16px / Optima+萍方 / 2px 间距")
    st.write("- 人名：15px 原生直角色块")
    st.write("- 正文：14px / 行距2.0 / 纯黑")

# 核心渲染逻辑
def render_block_html(main_title, raw_script, host, guest, others, h_color, g_color):
    if not raw_script.strip() and not main_title.strip():
        return ""
        
    all_guests = [guest] + [x.strip() for x in others.split('，') if x.strip()]
    lines = raw_script.split('\n')
    
    # --- 标题部分：采用你最满意的 Optima + 2px 间距风格 ---
    title_style = "color: #3E8AB8; font-size: 16px; font-weight: bold; letter-spacing: 2px; font-family: Optima, 'PingFang SC', sans-serif;"
    html = f'<p style="text-align: center; margin: 20px 0 0 0; line-height: 1.6;"><span style="{title_style}">{main_title}</span></p>'
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
            bg_color = h_color if is_host else g_color
            html += f'<p style="margin-top: 28px; margin-bottom: 10px; line-height: 1;"><span style="background-color: {bg_color}; color: #ffffff; font-size: 15px; font-weight: bold; padding: 1px 2px;">{name}</span></p>'
        else:
            html += f'<p style="margin: 0; text-align: justify; line-height: 200%; letter-spacing: 0.5px;"><span style="font-size: 14px; color: #000000;">{clean_line}</span></p>'
            
    html += '<p style="min-height: 2em; margin: 0;"></p>'
    return html

# 存储 HTML
all_blocks_html = []

for i in range(1, 4):
    st.subheader(f"📍 模块 {i}")
    col_in, col_pre = st.columns([1, 1])
    
    with col_in:
        m_title = st.text_input(f"标题 {i}", value=f"标题内容 {i}", key=f"t_{i}")
        m_script = st.text_area(f"文稿 {i}", height=250, key=f"s_{i}")
    
    current_html = render_block_html(m_title, m_script, host_name, guest_name, other_guests, color_host, color_guest)
    all_blocks_html.append(current_html)
    
    with col_pre:
        st.caption("分模块预览")
        st.components.v1.html(f'<div style="border:1px solid #eee; padding:10px; background:white;">{current_html if current_html else "等待输入..."}</div>', height=350, scrolling=True)
    st.markdown("---")

# --- 底部：全文合并一键导出 ---
st.header("🚀 全文合并一键导出")
full_combined_html = "".join(all_blocks_html)

if full_combined_html.strip():
    # 这里的 JS 代码块使用了分段构建，避免三引号导致的语法错误
    copy_button_html = f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <button onclick="copyFull()" style="padding: 15px 40px; background-color: #07c160; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 18px; font-weight: bold; box-shadow: 0 4px 10px rgba(7,193,96,0.3);">
            🔥 点击一键复制“全文”
        </button>
        <p id="full_msg" style="color: #07c160; font-weight: bold; margin-top: 10px;"></p>
    </div>
    <div style="border: 2px solid #07c160; padding: 20px; background: white;">
        <div id="full_area">{full_combined_html}</div>
    </div>
    <script>
    function copyFull() {{
        var node = document.getElementById('full_area');
        var range = document.createRange();
        range.selectNode(node);
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(range);
        document.execCommand('copy');
        document.getElementById('full_msg').innerText = "✅ 全文已成功复制！";
        setTimeout(function(){{ document.getElementById('full_msg').innerText = ""; }}, 3000);
        window.getSelection().removeAllRanges();
    }}
    </script>
    """
    st.components.v1.html(copy_button_html, height=1000, scrolling=True)
else:
    st.info("在上方输入内容后，此处将自动汇总。")
