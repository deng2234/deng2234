import streamlit as st

st.set_page_config(page_title="忽左忽右·原生排版工具", layout="wide")

st.title("🎙️ 播客排版工具 (公众号原生背景色版)")

with st.sidebar:
    st.header("👤 角色定义")
    host_name = st.text_input("主持人姓名", value="程衍樑")
    guest_name = st.text_input("嘉宾姓名", value="刘愿")
    other_guests = st.text_input("其他角色 (中文逗号隔开)", value="")
    
    st.header("🎨 颜色配置")
    # 这里默认改为你截图中的深蓝色和绿色
    color_host = st.color_picker("主持人背景色", "#79B9D9") 
    color_guest = st.color_picker("嘉宾背景色", "#47B04B")
    
    st.markdown("---")
    st.write("📌 **原生规范已锁定：**")
    st.write("- **人名：** 15px / 无圆角 / 无多余边距")
    st.write("- **正文：** 14px / 纯黑 / 行距 2.0 / 字距 0.5")

col1, col2 = st.columns([1, 1])

with col1:
    main_title = st.text_input("文章标题内容", value="「边币」信用的建立三阶段")
    raw_script = st.text_area("粘贴文稿...", height=500)

def parse_to_native_wechat(text, host, guest, others):
    all_guests = [guest] + [x.strip() for x in others.split('，') if x.strip()]
    lines = text.split('\n')
    
    # 标题：深蓝色 (#3E8AB8)，16px，居中，后空三行
    title_html = f"""
    <p style="text-align: center; margin-bottom: 0px;">
        <span style="color: #3E8AB8; font-size: 16px; font-weight: bold; letter-spacing: 1.5px;">{main_title}</span>
    </p>
    <p style="min-height: 1.5em;"></p>
    <p style="min-height: 1.5em;"></p>
    <p style="min-height: 1.5em;"></p>
    """
    
    body_html = ""
    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            body_html += '<p style="min-height: 1.5em; margin: 0;"></p>'
            continue
            
        is_host = clean_line == host or clean_line.startswith(f"{host}：") or clean_line.startswith(f"{host}:")
        is_guest = any(clean_line == g or clean_line.startswith(f"{g}：") or clean_line.startswith(f"{g}:") for g in all_guests)
        
        if is_host or is_guest:
            name = host if is_host else (clean_line.replace('：','').replace(':',''))
            bg_color = color_host if is_host else color_guest
            
            # 使用最简单的 span 背景，去掉 border-radius 和 padding 补丁
            # 这样粘贴过去就是公众号原生的“直角紧凑色块”
            body_html += f"""
            <p style="margin-top: 28px; margin-bottom: 10px; line-height: 1;">
                <span style="background-color: {bg_color}; color: #ffffff; font-size: 15px; font-weight: bold; padding: 1px 2px;">{name}</span>
            </p>
            """
        else:
            # 正文：2.0 倍行距 (200%)，纯黑，0.5 字距
            body_html += f"""
            <p style="margin: 0; text-align: justify; line-height: 200%; letter-spacing: 0.5px;">
                <span style="font-size: 14px; color: #000000;">{clean_line}</span>
            </p>
            """
            
    return title_html + body_html

final_html = parse_to_native_wechat(raw_script, host_name, guest_name, other_guests)

with col2:
    st.subheader("👁️ 预览与一键复制")
    
    copy_layout = f"""
    <div style="margin-bottom: 20px;">
        <button onclick="copyToClipboard()" style="padding: 12px 24px; background-color: #07c160; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">
            🟢 点击一键复制（原生背景色版）
        </button>
        <span id="status" style="margin-left: 10px; color: #07c160;"></span>
    </div>
    <div style="border: 1px solid #eee; padding: 20px; background: white;">
        <div id="copy-area">{final_html}</div>
    </div>
    <script>
    function copyToClipboard() {{
        const node = document.getElementById('copy-area');
        const range = document.createRange();
        range.selectNode(node);
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(range);
        document.execCommand('copy');
        document.getElementById('status').innerText = "✅ 复制成功";
        setTimeout(() => {{ document.getElementById('status').innerText = ""; }}, 2000);
        window.getSelection().removeAllRanges();
    }}
    </script>
    """
    st.components.v1.html(copy_layout, height=1000, scrolling=True)
