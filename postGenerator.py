from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from few_shot import FewShotPosts

def getLength(length):
    if length == "Short":
        return "1 to 4 lines" 
    if length == "Medium":
        return "5 to 9 lines" 
    if length == "Long":
        return "10 or more then 15 lines" 
def generatePost(length,lang,topic):
    len_in_num = getLength(length)
    prompt = f'''
    Generate a post for linked without any preamble.It should be according to following specifications:
    1. Topic = {topic}
    2. Length of Post = {len_in_num}
    3. Language of Post = {lang}
    If language is Hinglish then it means it is mix of hindi and english
    The script for generated post should alwasy be English. 

    '''
    fs = FewShotPosts()
    examplePost = fs.getFilteredPosts(length,topic,lang)
    
    if len(examplePost) > 0:
        prompt += "Also i am giving you examples, make sure the Posts writing style is exactly according to the style adopted in given examples: \nExamples:"
    
    for i, post in enumerate(examplePost):
        postText = post["text"]
        num = i + 1
        prompt += f"\n\n({num}) {postText} "


    response = llm.invoke(prompt)

    return response.content