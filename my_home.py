from pyecharts import options as opts
import streamlit as st
import pandas as pd
from PIL import Image
import time
import base64
import streamlit as st

from streamlit.components.v1 import components
import jieba
def bar_bg(img):
    last = 'png'
    st.markdown(
        f"""
        <style>
        [data-testid='stSidebar'] > div:first-child {{
            background: url(data:img/{last};base64,{base64.b64encode(open(img, 'rb').read()).decode()});
            background-size:cover
        }}
        </style>
        """,
        unsafe_allow_html = True,
    )
def page_bg(img):
    last = 'png'
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:img/{last};base64,{base64.b64encode(open(img, 'rb').read()).decode()});
            background-size:cover
        }}
        </style>
        """,
        unsafe_allow_html = True,
    )
bar_bg("images/背景1.png")
page_bg("images/背景.png")
page = st.sidebar.radio("我的首页",["我的兴趣推荐","图片处理工具","智慧词典","留言区","老师demo","布局页","布局页1","布局页2","布局页3","进度条","词云图","网址导航",'滑动条'])
def img_change(img,rc,gc,bc):
    width,height = img.size
    img_array = img.load()
    for x in range(width):
        for y in range(height):
            r = img_array[x,y][rc]
            g = img_array[x,y][gc]
            b = img_array[x,y][bc]
            img_array[x,y] = (r,g,b)
    
    return img
def change_mode(img,L):
    return img
def ciyun(text):
    words_list = jieba.lcut(text)
    words_dict = {}
    drop = ['我们', '你们', '他们', '就是', '没有',"的"]
    for word in words_list:
        #去重判断
        if word in words_dict:
            words_dict[word] += 1
        else:
            #数据清洗过滤
            if len(word) > 1 and word not in drop:
                #创建键值
                words_dict[word] = 1
    wordcloud = WordCloud()
    name = ''  
    data = list(words_dict.items())  
    wordcloud.add(name, data)  
    wordcloud.set_global_opts(title_opts=opts.TitleOpts(title=name,subtitle="词云图", pos_left="center",title_textstyle_opts=opts.TextStyleOpts(font_size=20,color="red")))
    wordcloud.render("词云.html")
if page == "我的兴趣推荐":
    st.write("你好，很高兴认识你")
    st.image("images/4.gif")
    st.image("images/去海边游泳.png")
elif page == "图片处理工具":
    st.write("图片处理小程序")
    uploade_file = st.file_uploader("上传图片",type=['png','jpeg','jpg','gif'])
    if uploade_file:
        file_name = uploade_file.name #文件名字
        file_type = uploade_file.type #文件格式
        file_size = uploade_file.size #文件大小

        img = Image.open(uploade_file)
        tab1,tab2,tab3,tab4 = st.tabs(["原图","A","B","C"])
        with tab1:
            st.image(img)
        with tab2:
            st.image(img_change(img,0,2,1))
        with tab3:
            st.image(img_change(img,1,2,0))
        with tab4:
            st.image(img_change(img,2,1,0))

elif page == "智慧词典":
    pass
    st.write("智慧词典")
    with open("txt/words_space.txt",'r',encoding='utf-8') as f:
        words_list = f.read().split('\n')
    for i in range(len(words_list)):
        words_list[i] = words_list[i].split('#')
    words_dict = {}
    for i in words_list:
        words_dict[i[1]] = [int(i[0]),i[2]]

    with open("txt/check_out_times.txt",'r',encoding='utf-8') as f:
        times_list = f.read().split('\n')

    for i in range(len(times_list)):
        times_list[i] = times_list[i].split('#')
    print("zheshisha ",times_list)
    times_dict = {}
    for i in times_list:
        times_dict[int(i[0])] = int(i[1])
    # print(words_dict)
    word = st.text_input("输入要查询的单词")
    if word in words_dict:
        st.write(words_dict[word])
        n = words_dict[word][0]
        if n in times_dict:
            times_dict[n] +=1
        else:
            times_dict[n] = 1
        with open('txt/check_out_times.txt', 'w', encoding='utf-8') as f:
            message = ''
            for k, v in times_dict.items():
                message += str(k) + '#' + str(v) + '\n'
            message = message[:-1]
            print("这是",message)
            f.write(message)
        st.write('查询次数：',times_dict[n])
        
elif page == "留言区":
    st.write('我的留言区')
    # 从文件中加载内容，并处理成列表
    with open('txt/leave_messages.txt', 'r', encoding='utf-8') as f:
        messages_list = f.read().split('\n')
    for i in range(len(messages_list)):
        messages_list[i] = messages_list[i].split('#')
    num_page = 3
    if "page" not in st.session_state and "start" not in st.session_state:
        st.session_state.start =0
        st.session_state.page =st.session_state.start+num_page
    for i in messages_list[st.session_state.start:st.session_state.page]:
        if i[1] == "阿短":
            with st.chat_message("🌞"):
                st.write(i[1]+":"+i[2])
        elif i[1] == "编程猫":
            with st.chat_message("猫"):
                st.write(i[1]+":"+i[2])
    last,col1,col2,col3,col4,col5,col6,col7,col8,col9,next= st.columns([0.2,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.2])
    with last:
        last_page= st.button("上一页")    
        if last_page:
            if st.session_state.start >=num_page and st.session_state.page>=st.session_state.start+num_page:
                st.session_state.start  -=num_page
                st.session_state.page -=num_page
                st.experimental_rerun()
    with col1:
        one_page = st.button("1")
        if one_page:    
            st.session_state.start = 0*num_page
            st.session_state.page =st.session_state.start+num_page
            st.experimental_rerun()
    with col2:
        two_page = st.button("2")
        if two_page:    
            st.session_state.start = 1*num_page
            st.session_state.page =st.session_state.start+num_page
            st.experimental_rerun()
    with col3:
        three_page = st.button("3")
        if three_page:    
            st.session_state.start = 2*num_page
            st.session_state.page =st.session_state.start+num_page
            st.experimental_rerun()
    with col4:
        four_page = st.button("4")
        if four_page:    
            st.session_state.start = 3*num_page
            st.session_state.page =st.session_state.start+num_page
            st.experimental_rerun()
    with col5:
        five_page = st.button("5")
        if five_page:
            st.session_state.start = 4*num_page
            st.session_state.page =st.session_state.start+num_page
            st.experimental_rerun()
    with col6:
        six_page = st.button("6")
        if six_page:
            st.session_state.start = 5*num_page
            st.session_state.page =st.session_state.start+num_page
            st.experimental_rerun()
    with col7:
        seven_page = st.button("7")
        if seven_page:
            st.session_state.start = 6*num_page
            st.session_state.page =st.session_state.start+num_page
            st.experimental_rerun()
    with col8:
        eight_page = st.button("8")
        if eight_page:
            st.session_state.start = 7*num_page
            st.session_state.page =st.session_state.start+num_page
            st.experimental_rerun()
    with col9:
        nine_page = st.button("9")
        if nine_page:
            st.session_state.start = 8*num_page
            st.session_state.page =st.session_state.start+num_page
            st.experimental_rerun()
    with next:
        next_page = st.button("下一页")
        if next_page:
            st.session_state.start +=num_page
            st.session_state.page +=num_page
            st.experimental_rerun()

    name = st.selectbox("我是...",["阿短","编程猫"])
    new_message = st.text_input("想要说的话")
    if st.button("留言"):
        messages_list.append([str(int(messages_list[-1][0])+1),name,new_message])
        with open('txt/leave_messages.txt', 'w', encoding='utf-8') as f:
            message = ''
            for i in messages_list:
                message += i[0] + '#' + i[1] + '#' + i[2] + '\n'
            message = message[:-1]
            f.write(message)
    
            
elif page == "老师demo":
    st.write(":red[这是红色的哈]")
    data = {
        '姓名':['阿短','编程猫','小可'],
        "学号":[1,2,3]
        }
    d = pd.DataFrame(data)
    st.write(d)
    st.write(123341241)
    with open("music/把酒叹平生.m4a",'rb') as f:
        bjtps = f.read()
    st.audio(bjtps,format = "audio/m4a",start_time = 0)
    st.write("把酒叹平生歌曲背景介绍:......")
elif page == "布局页":
    st.write("下面哪些可以")
    #columns中的参数可以是一个整数，代表创建n列，然后每一列宽度相等，也可以是一个迭代对象，
    #例如[0.7,0.3]第一列占70%，也可以是[1,2,3]创建三列，其中第二列的宽度是第一列的两倍，第三列的宽度也是第一列的三倍。
    col1,col2= st.columns([2,2])
    col3,col4 = st.columns([2,2])
    with col1:
        cb1 = st.checkbox("A.aaaaaa")
    with col2:
        cb2 = st.checkbox("B.bbbbbb")
    with col3:
        cb3 = st.checkbox("C.cccccc")
    with col4:
        cb4 = st.checkbox("D.dddddd")
    b1 = st.button("第一题答案")
    if b1:
        if cb1==False and cb2==True and cb3==True and cb4==False:
            st.write("对")
        else:
            st.write("错")
elif page == "布局页1":
    a1,a2 = st.columns([2,2])
    with a1:
        st.write('a1'*5) 
        st.write('a1'*5)  
    with a2:
        st.write('a2'*5)
        st.write('a2'*5)  

    st.write('a3'*28)

    a3,a4,a5 = st.columns([1,1,1])
    with a3:
        st.write('a3'*5)  
    with a4:
        st.write('a4'*5)
    with a5:
        st.write('a5'*5)  
    a6,a7 = st.columns([1,5])
    with a6:
        st.write('a6'*3)
    with a7:
        st.write('a7'*17)
    a8,a9 = st.columns([1,5])
    with a8:
        st.write('a8'*3)
    with a9:
        st.write('a9'*17)
    a10,a11 = st.columns([1,5])
    with a10:
        st.write('a10'*3)
    with a11:
        st.write('a11'*14)

elif page == "布局页2":
    a1,a2 = st.columns([2,2])
    with a1:
        st.write('a1'*5)
        st.write('a1'*5)  
    with a2:
        st.write('a2'*5)
        st.write('a2'*5)  
    a3,a4 = st.columns([2,2])
    with a3:
        st.write('a3'*17)
        a3_1,a3_2 = st.columns([1,1])
        with a3_1:
            st.write('a3_1'*3)
        with a3_2:
            st.write('a3_2'*3)
    with a4:
        st.write('a4'*5) 
        st.write('a4'*5) 
    a5,a6 = st.columns([1,5])
    with a5:
        st.write('a5'*3)
    with a6:
        st.write('a6'*17)
    a7,a8 = st.columns([1,5])
    with a7:
        st.write('a7'*3)
    with a8:
        st.write('a8'*17)
    a9,a10 = st.columns([1,5])
    with a9:
        st.write('a9'*3)
    with a10:
        st.write('a10'*14)
    
elif page == "布局页3":
    a1,a2 = st.columns([2,2])
    with a1:
        st.write('a1'*5)
 
    with a2:
        st.write('a2'*5)

    a3,a4,a5,a6 = st.columns([1,1,1,1])
    with a3:
 
        st.write('a3'*2)
    with a4:
        st.write('a4'*2) 
    with a5:
        st.write('a5'*2)
    with a6:
        st.write('a6'*2)
    st.write('aa'*26)
    a7,a8 = st.columns([1,5])
    with a7:
        st.write('a7'*3)
    with a8:
        st.write('a8'*17)
    a9,a10 = st.columns([1,5])
    with a9:
        st.write('a9'*3)
    with a10:
        st.write('a10'*14)
    a10,a11 = st.columns([1,5])
    with a10:
        st.write('a10'*3)
    with a11:
        st.write('a11'*14)
    

elif page =="进度条":
    now = 0
    keep = True
    images = ["images/武汉1.jpg", "images/武汉2.jpg", "images/武汉3.jpg","images/武汉4.jpg"]
    current_index = 0
    # 创建一个空的容器
    image_container = st.empty()
    image_container.image(images[current_index], use_column_width=True)
    roading = st.progress(0, '开始加载')
    my_open = st.toggle('暂停')
    if my_open:
        keep = False
        image_container.image(images[current_index], use_column_width=True)
    else:
        keep = True
    while keep:   
        time.sleep(1)
        current_index = (current_index ) % len(images)
        image_container.image(images[current_index], use_column_width=True)
        current_index+=1
        roading.progress(current_index*int(100/len(images)), '正在加载第{}张'.format(current_index))
        if current_index == len(images):
            roading.progress(100, '加载完毕！')
            current_index=0
    
elif page == "词云图":
    
    uploaded_file = st.file_uploader("上传txt文件")
    if uploaded_file is not None:
        pass
        # str_data = uploaded_file.read().decode("utf-8")
        # ciyun(str_data)
        # html_file = open('词云.html', 'r',encoding = 'utf-8')
        # html_content = html_file.read()
        # # 使用components.v1.html来显示HTML内容
        # st.components.v1.html(html_content, width = 1300,height=st.session_state.get("height", 800)) # 你可以根据需要调整height
        # #关闭文件
        # html_file.close()
    else:
        pass
elif page == "网址导航":
    st.write('除了本主站之外，我还将我的有趣内容分享在了其他网站中')
    go = st.selectbox('你的支持是我最大的动力，去支持一下up吧！', ['我的贴吧', '我的bilibili'])
    if go == '我的贴吧':
        st.link_button('帮我盖楼', 'https://www.baidu.com/')
    elif go == '我的bilibili':
        st.link_button('帮我一键三连', 'https://www.bilibili.com/')
elif page == '滑动条':
    # 滑动条st.slider()
    # number1 = st.slider('数据1：', 1, 100, 50)
    # number2, number3 = st.slider('数据2和3：', 1, 10, (4, 6))
    # st.write('数据1：', number1)
    # st.write('数据2-3：', number2, '-', number3)
    
    # # 如何创建滑动条？
    # # 滑动条中可以有几个数据点？
    
    # # 应用：留言_显示范围控制
    # st.write('----')
    # msg_lst = ['留言1', '留言2', '留言3', '留言4', '留言5', '留言6', '留言7', '留言8']
    # begin, end = st.slider('选择显示的留言信息：', 1, len(msg_lst), (1, len(msg_lst)))
    # for i in range(begin-1, end):
    #     st.write(msg_lst[i])
    # 应用：宣传_互联网知识
    st.write('----')
    st.write('你知道吗：为什么要设置公网和私网？为什么不让每一个设备都直接连接到公网上？')
    cb1 = st.checkbox('易于管理')
    cb2 = st.checkbox('效率高')
    cb3 = st.checkbox('网速快')
    cb4 = st.checkbox('安全性好')
    l = [cb1, cb2, cb3, cb4]
    if st.button('确认答案'):
        if True in l:
            st.write('其实都不对，答案是“历史问题，不得已而为之”')
        else:
            st.write('好厉害！确实都不对，真实答案是“历史问题，不得已而为之”，下面就让我来讲讲吧！')
