import streamlit as st

# 页面配置
st.set_page_config(page_title="忽左忽右·专业排版工具", layout="wide")

st.title("🎙️ 播客排版工具 (格式增强版)")

# 侧边栏设置
with st.sidebar:
    st.header("👤 角色定义")
    host_name = st.text_input("主持人姓名", value="程衍樑")
    guest_name = st.text_input("嘉宾姓名", value="刘愿")
    other_guests = st.text_input("其他角色 (用中文逗号隔开)", value="")
    
    st.header("🎨 颜色配置")
    color_host = st.color_picker("主持人颜色", "#79B9D9") # 蓝色
    color_guest = st.color_picker("嘉宾颜色", "#47B04B")  # 绿色
    
    st.markdown("---")
    st.write("📌 **当前规范：**")
    st.write("- 标题：16px 居中")
    st.write("- 人名：15px 加粗")
    st.write("- 正文：14px 行距1.8")

# 输入区域
col1, col2 = st.columns([1, 1])

with col1:
    main_title = st.text_input("文章标题", value="「边币」信用的建立三阶段")
    st.markdown("**文稿内容** (一行名字，一行内容)")
    raw_script = st.text_area("粘贴文稿...", placeholder="刘愿\n这里是正文...\n\n程衍樑\n这里是追问...", height=500)

# 解析逻辑：强力注入内联样式
def parse_to_wechat_html(text, host, guest, others):
    # 构建角色列表
    all_guests = [guest] + [x.strip() for x in others.split('，') if x.strip()]
    lines = text.split('\n')
    html_result = ""
    
    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            # 微信对空 p 标签支持更好
            html_result += '<p style="min-height: 1em;"></p>'
            continue
            
        # 判定是否为人名行
        is_host = clean_line == host or clean_line.startswith(f"{host}：") or clean_line.startswith(f"{host}:")
        is_guest = any(clean_line == g or clean_line.startswith(f"{g}：") or clean_line.startswith(f"{g}:") for g in all_guests)
        
        if is_host or is_guest:
            name = host if is_host else (clean_line.split('：')[0].split(':')[0])
            bg_color = color_host if is_host else color_guest
            # 人名标签：15px
            html_result += f"""
            <p style="margin-top: 30px; margin-bottom: 10px; line-height: 1;">
                <span style="background-color: {bg_color}; color: #ffffff; padding: 3px 10px; font-size: 15px; font-weight: bold; border-radius: 2px; display: inline-block; font-family: sans-serif;">
                    {name}
                </span>
            </p>
            """
        else:
            # 正文内容：14px，行高1.8，必须写在 p 标签上
            html_result += f"""
            <p style="font-size: 14px; line-height: 1.8; color: #3f3f3f; text-align: justify; margin-bottom: 15px; font-family: sans-serif; letter-spacing: 0.5px;">
                {clean_line}
            </p>
            """
    return html_result

# 组装最终结果
formatted_body = parse_to_wechat_html(raw_script, host_name, guest_name, other_guests)

# 标题：16px 居中
final_html = f"""
<div id="copy-area" style="font-family: sans-serif; background-color: #ffffff; padding: 10px;">
    <p style="text-align: center; margin-top: 20px; margin-bottom: 40px; line-height: 1.5;">
        <span style="color: #4a90e2; font-size: 16px; font-weight: bold; letter-spacing: 1px;">{main_title}</span>
    </p>
    {formatted_body}
</div>
"""

with col2:
    st.subheader("👁️ 预览与一键复制")
    
    # 复制逻辑改进
    copy_script = f"""
    <div style="margin-bottom: 20px;">
        <button onclick="copyToClipboard()" style="padding: 12px 25px; background-color: #07c160; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold;">
            🟢 点击一键复制（格式增强版）
        </button>
        <p id="status" style="color: #07c160; font-size: 13px; margin-top: 10px; font-weight: bold;"></p>
    </div>

    <div style="border: 1px solid #eee; padding: 15px;">
        {final_html}
    </div>

    <script>
    function copyToClipboard() {{
        var container = document.getElementById('copy-area');
        var range = document.createRange();
        range.selectNode(container);
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(range);
        try {{
            document.execCommand('copy');
            document.getElementById('status').innerText = "✅ 复制成功！请直接在公众号后台粘贴。";
        }} catch (err) {{
            document.getElementById('status').innerText = "❌ 复制失败，请手动全选预览区。";
        }}
        window.getSelection().removeAllRanges();
    }}
    </script>
    """
    st.components.v1.html(copy_script, height=1000, scrolling=True)
