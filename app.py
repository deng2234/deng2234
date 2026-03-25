import streamlit as st

# 页面配置
st.set_page_config(page_title="忽左忽右·精密排版工具", layout="wide")

st.title("🎙️ 播客排版工具 (精密格式版)")

# 侧边栏设置
with st.sidebar:
    st.header("👤 角色定义")
    host_name = st.text_input("主持人姓名", value="程衍樑")
    guest_name = st.text_input("嘉宾姓名", value="刘愿")
    other_guests = st.text_input("其他角色 (用中文逗号隔开)", value="")
    
    st.header("🎨 颜色配置")
    color_host = st.color_picker("主持人标签颜色", "#79B9D9") # 蓝色
    color_guest = st.color_picker("嘉宾标签颜色", "#47B04B")  # 绿色
    
    st.markdown("---")
    st.write("📌 **当前规范：**")
    st.write("- 标题：16px / 居中 / 蓝")
    st.write("- 标题后：强制 3 条空行")
    st.write("- 人名：15px / 加粗 / 白字")
    st.write("- 正文：14px / 行距 2.0 / 字距 0.5 / 纯黑")

# 输入区域
col1, col2 = st.columns([1, 1])

with col1:
    main_title = st.text_input("文章标题内容", value="「边币」信用的建立三阶段")
    st.markdown("**文稿内容** (支持直接粘贴，名字识别后会自动加标签)")
    raw_script = st.text_area("粘贴文稿...", placeholder="刘愿\n这里是正文第一行\n这里是正文第二行\n\n程衍樑\n这里是追问...", height=500)

# 解析逻辑：极致兼容微信后台
def parse_to_wechat_html(text, host, guest, others):
    all_guests = [guest] + [x.strip() for x in others.split('，') if x.strip()]
    lines = text.split('\n')
    html_result = ""
    
    # 标题部分：16px, 居中, 蓝色, 后面跟三个空行
    title_html = f"""
    <p style="text-align: center; margin: 20px 0 0 0; line-height: 1.5;">
        <span style="color: #4a90e2; font-size: 16px; font-weight: bold; letter-spacing: 1px; font-family: sans-serif;">{main_title}</span>
    </p>
    <p style="min-height: 1em; margin: 0;"></p>
    <p style="min-height: 1em; margin: 0;"></p>
    <p style="min-height: 1em; margin: 0;"></p>
    """
    
    body_html = ""
    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            # 这里的空行设为 margin 0 保证“换行只换一行”
            body_html += '<p style="min-height: 1em; margin: 0;"></p>'
            continue
            
        # 判定是否为人名行
        is_host = clean_line == host or clean_line.startswith(f"{host}：") or clean_line.startswith(f"{host}:")
        is_guest = any(clean_line == g or clean_line.startswith(f"{g}：") or clean_line.startswith(f"{g}:") for g in all_guests)
        
        if is_host or is_guest:
            # 提取名字，去除可能的冒号
            display_name = clean_line.replace('：', '').replace(':', '').strip()
            bg_color = color_host if is_host else color_guest
            
            # 人名标签：15px，加粗，由于微信限制，margin 设置要保守
            body_html += f"""
            <p style="margin-top: 25px; margin-bottom: 8px; line-height: 1;">
                <span style="background-color: {bg_color}; color: #ffffff; padding: 4px 10px; font-size: 15px; font-weight: bold; border-radius: 2px; display: inline-block; font-family: sans-serif;">
                    {display_name}
                </span>
            </p>
            """
        else:
            # 正文内容：14px，行间距 2.0，字间距 0.5，颜色纯黑 #000000
            # margin: 0 保证换行时不会出现额外的段间距
            body_html += f"""
            <p style="font-size: 14px; line-height: 2.0; letter-spacing: 0.5px; color: #000000; text-align: justify; margin: 0; font-family: sans-serif;">
                {clean_line}
            </p>
            """
            
    return title_html + body_html

# 生成最终结果
final_html_content = parse_to_wechat_html(raw_script, host_name, guest_name, other_guests)

with col2:
    st.subheader("👁️ 预览与一键复制")
    
    # 包含复制功能的 HTML 组件
    # 使用 container-style 确保预览效果接近手机端
    copy_layout = f"""
    <div style="margin-bottom: 20px;">
        <button onclick="copyRichText()" style="padding: 12px 24px; background-color: #07c160; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            🟢 点击一键复制（格式已锁定）
        </button>
        <span id="msg" style="margin-left: 15px; color: #07c160; font-weight: bold; font-size: 13px;"></span>
    </div>

    <div style="border: 1px solid #eee; padding: 15px; background: white; min-height: 600px;">
        <div id="copy-target">
            {final_html_content}
        </div>
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
            document.getElementById('msg').innerText = "✅ 已复制！请前往后台粘贴";
            setTimeout(() => {{ document.getElementById('msg').innerText = ""; }}, 3000);
        }} catch (err) {{
            alert("复制失败，请尝试手动全选。");
        }}
        selection.removeAllRanges();
    }}
    </script>
    """
    st.components.v1.html(copy_layout, height=1200, scrolling=True)
