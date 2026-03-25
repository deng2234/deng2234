import streamlit as st
import re

# 页面配置
st.set_page_config(page_title="忽左忽右·对话排版助手", layout="wide")

st.title("🎙️ 播客内容排版助手 (V2.0)")
st.caption("修复了识别逻辑，支持 14px 字号及【带格式一键复制】")

# 侧边栏配置
with st.sidebar:
    st.header("🎨 样式配置")
    color_guest = st.color_picker("嘉宾标签颜色", "#47B04B") # 绿色
    color_host = st.color_picker("主持标签颜色", "#79B9D9")  # 蓝色
    st.info("提示：正文字体已设为 14px")

# 输入区域
col1, col2 = st.columns([1, 1])

with col1:
    main_title = st.text_input("文章标题", value="「边币」信用的建立三阶段")
    st.markdown("---")
    st.markdown("**文稿输入区** (格式：`名字：内容`)")
    raw_script = st.text_area("在此粘贴对话...", placeholder="刘愿：这里是内容...\n\n程衍樑：这里是追问...", height=500)

# 解析函数
def parse_script_to_html(text):
    lines = text.split('\n')
    html_result = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            # 处理空行，增加垂直间距
            html_result += '<p style="height: 15px; margin: 0;"></p>'
            continue
            
        # 使用正则表达式识别： 名字 + 冒号（全角或半角）+ 内容
        match = re.match(r'^([^：:]+)[：:](.*)$', line)
        
        if match:
            name = match.group(1).strip()
            content = match.group(2).strip()
            # 颜色逻辑：包含“程”用蓝色，否则用绿色
            bg_color = color_host if "程" in name or "主" in name else color_guest
            
            html_result += f"""
            <div style="margin-top: 25px; margin-bottom: 8px;">
                <span style="background-color: {bg_color}; color: white; padding: 2px 8px; font-size: 13px; font-weight: bold; border-radius: 2px; display: inline-block;">
                    {name}
                </span>
            </div>
            <div style="font-size: 14px; line-height: 1.8; color: #3F3F3F; text-align: justify; margin-bottom: 15px;">
                {content}
            </div>
            """
        else:
            # 没有冒号的行，视为上一段的延续
            html_result += f"""
            <div style="font-size: 14px; line-height: 1.8; color: #3F3F3F; text-align: justify; margin-bottom: 15px;">
                {line}
            </div>
            """
    return html_result

# 构建完整的 HTML 片段
content_html = parse_script_to_html(raw_script)
final_rendered_html = f"""
<div id="copy-target" style="font-family: -apple-system, system-ui, sans-serif; padding: 20px; background-color: white;">
    <div style="text-align: center; margin: 30px 0 50px 0;">
        <h3 style="color: #4A90E2; font-size: 18px; font-weight: bold; letter-spacing: 1px;">{main_title}</h3>
    </div>
    {content_html}
</div>
"""

with col2:
    st.subheader("👁️ 预览与操作")
    
    # 注入“一键复制带格式文本”的 JavaScript 脚本
    # 注意：由于浏览器安全限制，Streamlit 的按钮无法直接复制富文本，我们通过 HTML 组件实现
    copy_js = f"""
    <div style="margin-bottom: 20px;">
        <button onclick="copyRichText()" style="padding: 10px 20px; background-color: #07c160; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">
            📋 点击一键复制（带格式）
        </button>
        <span id="msg" style="margin-left: 10px; color: #07c160; font-size: 12px;"></span>
    </div>
    
    <div style="border: 1px solid #eee; padding: 10px; background: white;">
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
            document.getElementById('msg').innerText = "已成功复制到剪贴板！请去公众号后台粘贴。";
        }} catch (err) {{
            document.getElementById('msg').innerText = "复制失败，请手动全选预览区。";
        }}
        selection.removeAllRanges();
    }}
    </script>
    """
    
    # 渲染预览和复制按钮
    st.components.v1.html(copy_js, height=800, scrolling=True)
