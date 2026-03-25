import streamlit as st

# 页面配置
st.set_page_config(page_title="忽左忽右·精密排版工具", layout="wide")

st.title("🎙️ 播客排版工具 (色块紧凑版)")

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
    st.write("📌 **已修复：**")
    st.write("- 人名背景：左右极窄间距")
    st.write("- 标题：深蓝色 + 3个空行")
    st.write("- 正文：2.0倍行距 / 纯黑")

# 输入区域
col1, col2 = st.columns([1, 1])

with col1:
    main_title = st.text_input("文章标题内容", value="「边币」信用的建立三阶段：稳健发行、服务财政与配套改革")
    raw_script = st.text_area("粘贴文稿...", placeholder="刘愿\n这里是正文...\n\n程衍樑\n这里是追问...", height=500)

def parse_to_wechat_html(text, host, guest, others):
    all_guests = [guest] + [x.strip() for x in others.split('，') if x.strip()]
    lines = text.split('\n')
    
    # 标题部分：16px, 居中, 修正后的深蓝色, 后面跟三个标准空行
    title_html = f"""
    <p style="text-align: center; margin: 20px 0 0 0; line-height: 1.5;">
        <span style="color: #3E8AB8; font-size: 16px; font-weight: bold; letter-spacing: 1px; font-family: sans-serif;">{main_title}</span>
    </p>
    <p style="min-height: 1.5em; margin: 0;"></p>
    <p style="min-height: 1.5em; margin: 0;"></p>
    <p style="min-height: 1.5em; margin: 0;"></p>
    """
    
    body_html = ""
    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            body_html += '<p style="min-height: 1.5em; margin: 0; line-height: 200%;"></p>'
            continue
            
        # 判定人名
        is_host = clean_line == host or clean_line.startswith(f"{host}：") or clean_line.startswith(f"{host}:")
        is_guest = any(clean_line == g or clean_line.startswith(f"{g}：") or clean_line.startswith(f"{g}:") for g in all_guests)
        
        if is_host or is_guest:
            name = host if is_host else (clean_line.replace('：','').replace(':',''))
            bg_color = color_host if is_host else color_guest
            
            # 人名标签：核心改动！去掉 inline-block，使用极小 padding 确保色块紧凑
            body_html += f"""
            <p style="margin-top: 30px; margin-bottom: 8px; line-height: 1.2;">
                <span style="background-color: {bg_color}; color: #ffffff; padding: 2px 3px; font-size: 15px; font-weight: bold; border-radius: 1px; font-family: sans-serif; letter-spacing: 0px;">{name}</span>
            </p>
            """
