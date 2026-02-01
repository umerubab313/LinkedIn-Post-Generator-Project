import streamlit as st
from few_shot import FewShotPosts
import postGenerator

def main():
    st.title("LinkedIn Post Generator")
    col1, col2, col3 = st.columns(3)
    fsObj = FewShotPosts()
    with col1:
        selected_tag = st.selectbox("Category", options=fsObj.getTags())
    with col2:
        selected_length = st.selectbox("Length", options=["Short","Medium","Long"])
    with col3:
        selected_lang = st.selectbox("Language", options=["English","Hinglish"])

    if st.button("Generate Post!"):
        st.write(f"Generated Post For {selected_tag},{selected_length},{selected_lang}:\n")
        st.write(postGenerator.generatePost(selected_length, selected_lang,selected_tag))


if __name__ == "__main__":
    main()
