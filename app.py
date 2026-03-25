import streamlit as st

# 页面配置
st.set_page_config(page_title="忽左忽右·最终版排版工具", layout="wide")

st.title("🎙️ 播客排版工具 (精密修正版)")

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
    st.write("📌 **当前规格：**")
    st.write("- 标题：16px / 居中 / 蓝")
    st.write("- 标题后：3 条标准空行")
    st.write("- 人名：15px / 紧凑色块")
    st.write("- 正文：14px / 行距 2.0 / 纯黑")

# 输入区域
col1, col2 = st.columns([1, 1])

with col1:
    main_title = st.text_input("文章标题内容", value="「边币」信用的建立三阶段")
    st.markdown("**文稿内容**")
    raw_script = st.text_area("粘贴文稿...", placeholder="刘愿\n这里是正文...\n\n程衍樑\n这里是追问...", height=500)

def parse_to_wechat_html(text, host, guest, others):
    all_guests = [guest] + [x.strip() for x in others.split('，') if x.strip()]
    lines = text.split('\n')
    html_result = ""
    
    # 标题部分：16px, 居中, 蓝色, 后面跟三个空行
    title_html = f"""
    <p style="text-align: center; margin: 20px 0 0 0; line-height: 1.5;">
        <span style="color: #4a90e2; font-size: 16px; font-weight: bold; letter-spacing: 1px;">{main_title}</span>
    </p>
    <p style="min-height: 1em; margin: 0;"></p>
    <p style="min-height: 1em; margin: 0;"></p>
    <p style="min-height: 1em; margin: 0;"></p>
    """
    
    body_html = ""
    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            # 换行只换一行的逻辑
            body_html += '<p style="min-height: 1em; margin: 0; line-height: 200%;"></p>'
            continue
            
        # 判定人名（精准匹配或带冒号匹配）
        is_host = clean_line == host or clean_line.startswith(f"{host}：") or clean_line.startswith(f"{host}:")
        is_guest = any(clean_line == g or clean_line.startswith(f"{g}：") or clean_line.startswith(f"{g}:") for g in all_guests)
        
        if is_host or is_guest:
            # 提取名字
            display_name = clean_line.replace('：', '').replace(':', '').strip()
            bg_color = color_host if is_host else color_guest
            
            # 人名标签：瘦身版，padding 减小，去掉 inline-block 以缩窄背景
            body_html += f"""
            <p style="margin-top: 25px; margin-bottom: 5px; line-height: 1.2;">
                <span style="background-color: {bg_color}; color: #ffffff; padding: 2px 5px; font-size: 15px; font-weight: bold; border-radius: 2px; font-family: sans-serif;">
                    {display_name}
                </span>
            </p>
            """
        else:
            # 正文内容：行间距使用 200% 强制加固，颜色 #000000
            body_html += f"""
            <p style="margin: 0; text-align: justify; line-height: 200%;">
                <span style="font-size: 14px; letter-spacing: 0.5px; color: #000000; font-family: sans-serif;">
                    {clean_line}
                </span>
            </p>
            """
            
    return title_html + body_html

final_html_content = parse_to_wechat_html(raw_script, host_name, guest_name, other_guests)

with col2:
    st.subheader("👁️ 预览与一键复制")
    
    # 复制组件
    copy_layout = f"""
    <div style="margin-bottom: 20px;">
        <button onclick="copyRichText()" style="padding: 12px 24px; background-color: #07c160; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold;">
            🟢 点击一键复制（精密版）
        </button>
        <span id="msg" style="margin-left: 15px; color: #07c160; font-weight: bold;"></span>
    </div>

    <div style="border: 1px solid #eee; padding: 20px; background: white;">
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
            document.getElementById('msg').innerText = "✅ 复制成功";
            setTimeout(() => {{ document.getElementById('msg').innerText = ""; }}, 2000);
        }} catch (err) {{
            alert("请手动全选复制预览区内容");
        }}
        selection.removeAllRanges();
    }}
    </script>
    """
    st.components.v1.html(copy_layout, height=1200, scrolling=True)
