import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from zhipuai_llm import ZhipuAILLM


def generate_response(input_text, api_key):
    llm = ZhipuAILLM(model="glm-4-0520", temperature=0.1, api_key=api_key)
    output = llm.invoke(input_text)
    output_parser = StrOutputParser()
    output = output_parser.invoke(output)
    return output


def main():
    st.title('科研GPT')
    zhipu_api_key = st.sidebar.text_input('ZhiPu API Key', type='password')
    if len(zhipu_api_key) == 0:
        st.warning('Please enter your ZhiPu API key!', icon='⚠')

    # 用于跟踪对话历史
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    messages = st.container(height=500)
    if prompt := st.chat_input("Say something"):
        # 将用户输入添加到对话历史中
        st.session_state.messages.append({"role": "user", "text": prompt})
        # 调用 respond 函数获取回答
        answer = generate_response(prompt, zhipu_api_key)
        # 检查回答是否为 None
        if answer is not None:
            # 将LLM的回答添加到对话历史中
            st.session_state.messages.append({
                "role": "assistant",
                "text": answer
            })

        # 显示整个对话历史
        for message in st.session_state.messages:
            if message["role"] == "user":
                messages.chat_message("user").write(message["text"])
            elif message["role"] == "assistant":
                messages.chat_message("assistant").write(message["text"])


if __name__ == "__main__":
    main()
