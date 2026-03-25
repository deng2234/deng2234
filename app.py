import streamlit as st

# 页面配置
st.set_page_config(page_title="忽左忽右·对话排版助手", layout="wide")

st.title("🎙️ 播客内容排版助手 (无冒号识别版)")

# 侧边栏：定义识别关键词
with st.sidebar:
    st.header("👤 角色定义")
    host_name = st.text_input("主持人姓名", value="程衍樑")
    guest_name = st.text_input("嘉宾姓名", value="刘愿")
    
    st.header("🎨 样式配置")
    color_host = st.color_picker("主持人标签颜色", "#79B9D9") # 蓝色
    color_guest = st.color_picker("嘉宾标签颜色", "#47B04B")  # 绿色
    st.info("正文字体：14px | 行高：1.8")

# 输入区域
col1, col2 = st.columns([1, 1])

with col1:
    main_title = st.text_input("文章标题", value="「边币」信用的建立三阶段")
    st.markdown("---")
    st.markdown("**文稿输入区** (名字需单独占一行，或名字后带空格/冒号均可识别)")
    raw_script = st.text_area("在此粘贴对话...", placeholder=f"{guest_name}\n这里是内容...\n\n{host_name}\n这里是追问...", height=500)

# 解析逻辑
def parse_script_smart(text, host, guest):
    lines = text.split('\n')
    html_result = ""
    
    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            html_result += '<p style="height: 12px; margin: 0;"></p>' # 空行处理
            continue
            
        # 识别逻辑：如果整行内容就是人名，或者是以人名开头后面带了冒号
        is_host = clean_line == host or clean_line.startswith(f"{host}:") or clean_line.startswith(f"{host}：")
        is_guest = clean_line == guest or clean_line.startswith(f"{guest}:") or clean_line.startswith(f"{guest}：")
        
        if is_host or is_guest:
            name = host if is_host else guest
            bg_color = color_host if is_host else color_guest
            
            html_result += f"""
            <div style="margin-top: 28px; margin-bottom: 12px;">
                <span style="background-color: {bg_color}; color: white; padding: 2px 8px; font-size: 13px; font-weight: bold; border-radius: 2px; display: inline-block;">
                    {name}
                </span>
            </div>
            """
        else:
            # 正文内容：14px
            html_result += f"""
            <div style="font-size: 14px; line-height: 1.8; color: #3F3F3F; text-align: justify; margin-bottom: 16px;">
                {clean_line}
            </div>
            """
    return html_result

# 最终 HTML 构建
content_html = parse_script_smart(raw_script, host_name, guest_name)
final_rendered_html = f"""
<div id="copy-target" style="font-family: -apple-system, system-ui, sans-serif; padding: 20px; background-color: white;">
    <div style="text-align: center; margin: 20px 0 50px 0;">
        <p style="color: #4A90E2; font-size: 18px; font-weight: bold; letter-spacing: 1px;">{main_title}</p>
    </div>
    {content_html}
</div>
"""

with col2:
    st.subheader("👁️ 预览与一键复制")
    
    # 一键复制组件
    copy_component = f"""
    <div style="margin-bottom: 20px;">
        <button onclick="copyRichText()" style="padding: 12px 24px; background-color: #07c160; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            🟢 点击一键复制（带格式）
        </button>
        <span id="msg" style="margin-left: 15px; color: #07c160; font-weight: bold;"></span>
    </div>
    
    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; background: #fff; box-shadow: inset 0 0 10px rgba(0,0,0,0.05);">
        {final_rendered_html}
    </div>

    <script>
    function copyRichText() {{
        const target = document.getElementById('copy-target');
        const range = document.createRange();
        range.selectNode(target);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        try {{
            document.execCommand('copy');
            const msg = document.getElementById('msg');
            msg.innerText = "✅ 已成功复制！请去公众号后台粘贴";
            setTimeout(() => {{ msg.innerText = ""; }}, 3000);
        }} catch (err) {{
            alert("复制失败，请手动全选预览区。");
        }}
        selection.removeAllRanges();
    }}
    </script>
    """
    st.components.v1.html(copy_component, height=900, scrolling=True)
