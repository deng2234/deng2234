import streamlit as st

# 页面配置
st.set_page_config(page_title="忽左忽右·多模块排版工具", layout="wide")

st.title("🎙️ 播客排版工具 (三模块原生版)")

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
    st.write("📌 **样式说明：**")
    st.write("- 标题：16px / 深蓝 / 居中")
    st.write("- 人名：15px / 原生直角背景")
    st.write("- 正文：14px / 行距2.0 / 字距0.5 / 纯黑")

# 核心处理函数
def parse_content(main_title, raw_script, host, guest, others, h_color, g_color):
    if not raw_script.strip():
        return "<p style='color:gray;'>等待输入内容...</p>"
        
    all_guests = [guest] + [x.strip() for x in others.split('，') if x.strip()]
    lines = raw_script.split('\n')
    
    # 标题：深蓝色 (#3E8AB8)，16px，居中，后空三行
    html = f"""
    <p style="text-align: center; margin: 20px 0 0 0; line-height: 1.5;">
        <span style="color: #3E8AB8; font-size: 16px; font-weight: bold; letter-spacing: 1.5px;">{main_title}</span>
    </p>
    <p style="min-height: 1.5em; margin: 0;"></p>
    <p style="min-height: 1.5em; margin: 0;"></p>
    <p style="min-height: 1.5em; margin: 0;"></p>
    """
    
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
            # 极简 span，确保原生感
            html += f"""
            <p style="margin-top: 28px; margin-bottom: 10px; line-height: 1;">
                <span style="background-color: {bg_color}; color: #ffffff; font-size: 15px; font-weight: bold; padding: 1px 2px;">{name}</span>
            </p>
            """
        else:
            # 正文：2.0 倍行距，纯黑，0.5 字距
            html += f"""
            <p style="margin: 0; text-align: justify; line-height: 200%; letter-spacing: 0.5px;">
                <span style="font-size: 14px; color: #000000;">{clean_line}</span>
            </p>
            """
    return html

# 渲染三个模块
for i in range(1, 4):
    st.markdown(f"### --- 模块 {i} ---")
    c1, c2 = st.columns([1, 1])
    
    with c1:
        m_title = st.text_input(f"模块 {i} 标题", value=f"示例标题 {i}", key=f"title_{i}")
        m_script = st.text_area(f"模块 {i} 文稿内容", height=300, key=f"script_{i}")
        
    with c2:
        st.write("预览与复制")
        final_html = parse_content(m_title, m_script, host_name, guest_name, other_guests, color_host, color_guest)
        
        # 复制逻辑组件
        ui_id = f"copy_area_{i}"
        btn_id = f"btn_{i}"
        
        st.components.v1.html(f"""
            <div style="margin-bottom: 10px;">
                <button id="{btn_id}" onclick="copyToClipboard()" style="padding: 10px 20px; background-color: #07c160; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">
                    📋 点击复制模块 {i}
                </button>
                <span id="msg_{i}" style="margin-left: 10px; color: #07c160; font-size: 12px; font-weight: bold;"></span>
            </div>
            <div style="border: 1px solid #eee; padding: 15px; background: white; font-family: sans-serif;">
                <div id="{ui_id}">{final_html}</div>
            </div>
            <script>
            function copyToClipboard() {{
                const node = document.getElementById('{ui_id}');
                const range = document.createRange();
                range.selectNode(node);
                window.getSelection().removeAllRanges();
                window.getSelection().addRange(range);
                document.execCommand('copy');
                document.getElementById('msg_{i}').innerText = "✅ 已复制";
                setTimeout(() => {{ document.getElementById('msg_{i}').innerText = ""; }}, 2000);
                window.getSelection().removeAllRanges();
            }}
            </script>
        """, height=450, scrolling=True)
    st.markdown("---")
