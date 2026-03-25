import streamlit as st

# 页面配置
st.set_page_config(page_title="忽左忽右·像素级排版工具", layout="wide")

st.title("🎙️ 播客排版工具 (左侧原样还原版)")

# 侧边栏设置
with st.sidebar:
    st.header("👤 角色定义")
    host_name = st.text_input("主持人姓名", value="程衍樑")
    guest_name = st.text_input("嘉宾姓名", value="刘愿")
    other_guests = st.text_input("其他角色 (中文逗号隔开)", value="")
    
    st.header("🎨 颜色配置")
    color_host = st.color_picker("主持人颜色", "#79B9D9")
    color_guest = st.color_picker("嘉宾颜色", "#47B04B")
    
    st.markdown("---")
    st.write("✅ **样式已锁定：**")
    st.write("- 标题：16px / 居中 / 蓝 / 后空3行")
    st.write("- 人名：15px / 极简紧凑色块")
    st.write("- 正文：14px / 纯黑 / 2.0倍行距 / 0.5字距")

# 输入区域
col1, col2 = st.columns([1, 1])

with col1:
    main_title = st.text_input("文章标题内容", value="「边币」信用的建立三阶段：稳健发行、服务财政与配套改革")
    raw_script = st.text_area("粘贴文稿...", placeholder="刘愿\n这里是正文...\n\n程衍樑\n这里是追问...", height=500)

def parse_to_wechat_html(text, host, guest, others):
    all_guests = [guest] + [x.strip() for x in others.split('，') if x.strip()]
    lines = text.split('\n')
    
    # 标题部分：16px, 居中, 蓝色, 后面跟三个标准空行
    title_html = f"""
    <p style="text-align: center; margin: 20px 0 0 0; line-height: 1.5;">
        <span style="color: #4a90e2; font-size: 16px; font-weight: bold; letter-spacing: 1.5px; font-family: sans-serif;">{main_title}</span>
    </p>
    <p style="min-height: 1.5em; margin: 0;"></p>
    <p style="min-height: 1.5em; margin: 0;"></p>
    <p style="min-height: 1.5em; margin: 0;"></p>
    """
    
    body_html = ""
    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            # 换行只换一行的逻辑
            body_html += '<p style="min-height: 1.5em; margin: 0;"></p>'
            continue
            
        is_host = clean_line == host or clean_line.startswith(f"{host}：") or clean_line.startswith(f"{host}:")
        is_guest = any(clean_line == g or clean_line.startswith(f"{g}：") or clean_line.startswith(f"{g}:") for g in all_guests)
        
        if is_host or is_guest:
            name = host if is_host else (clean_line.replace('：','').replace(':',''))
            bg_color = color_host if is_host else color_guest
            
            # 使用 table 布局锁定人名标签宽度，防止过宽
            body_html += f"""
            <table style="margin-top: 35px; margin-bottom: 12px; border-collapse: collapse;">
                <tr>
                    <td style="background-color: {bg_color}; padding: 1px 4px; border-radius: 1px;">
                        <span style="color: #ffffff; font-size: 15px; font-weight: bold; line-height: 1.1; letter-spacing: 0px; font-family: sans-serif;">{name}</span>
                    </td>
                </tr>
            </table>
            """
        else:
            # 正文内容：14px, 纯黑, 2.0行距, 0.5字距
            # margin-bottom 增加一点，模拟左图的段落呼吸感
            body_html += f"""
            <p style="margin: 0 0 1.2em 0; text-align: justify; line-height: 2.0; letter-spacing: 0.5px;">
                <span style="font-size: 14px; color: #000000; font-family: sans-serif;">{clean_line}</span>
            </p>
            """
            
    return title_html + body_html

final_content = parse_to_wechat_html(raw_script, host_name, guest_name, other_guests)

with col2:
    st.subheader("👁️ 预览 (点击下方按钮复制)")
    
    copy_layout = f"""
    <div style="margin-bottom: 25px;">
        <button onclick="copyRichText()" style="padding: 12px 30px; background-color: #07c160; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; font-weight: bold; box-shadow: 0 2px 6px rgba(0,0,0,0.15);">
            📋 点击复制带格式文本
        </button>
        <span id="msg" style="margin-left: 15px; color: #07c160; font-weight: bold;"></span>
    </div>

    <div style="border: 1px solid #ddd; padding: 25px; background: #fff; min-height: 800px;">
        <div id="copy-target" style="word-wrap: break-word;">
            {final_content}
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
            document.getElementById('msg').innerText = "已成功复制，请直接粘贴";
            setTimeout(() => {{ document.getElementById('msg').innerText = ""; }}, 2500);
        }} catch (err) {{
            alert("请手动全选预览区内容进行复制");
        }}
        selection.removeAllRanges();
    }}
    </script>
    """
    st.components.v1.html(copy_layout, height=1200, scrolling=True)
