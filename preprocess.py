# now in this gen ai proj we will be having three steps:
# step 1: pre processing the data/the raw posts to :
#              i) categorized data of posts 
#              ii) using Llama to further process it and extract out main features from it 
# step 2: using the final data to generate a promppt
# step 3: sending pprompt to our gen ai model that generates a post accordingly 
# -----------------------------------------------------------------------------------------     
import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm

def process_posts(raw_file_path, processed_file_path="data/processed_posts.json"):
    with open(raw_file_path, encoding='utf-8') as file:
        data_raw = json.load(file)
        newDataList = []
        #print(data_raw)
        for post in data_raw:
            extra_data = process_raw_data(post)
            new_data = post | extra_data  # union
            newDataList.append(new_data)

        unique_tags = getUniqueTags(newDataList)
        
        for post in newDataList:
            current_tags = post["tags"]
            
            new_tags = {
                unique_tags.get(tag, tag)  # fallback to original tag
                for tag in current_tags
            }

            post['tags'] = list(new_tags)

        with open(processed_file_path,encoding="utf-8",mode="w") as outfile:
            json.dump(newDataList, outfile, indent=4)



        for posts in newDataList:
            print(posts)
        
        
def getUniqueTags(processedPost):
    # we are taking a set so that repetitve tags in all posts are removed
    # and we only get unique tags
    uniqueTagsSet = set()
    for post in processedPost:
        uniqueTagsSet.update(post["tags"])
    
    # now after getting unique set of tags we again process the data by using 
    # llm to give a single tag for all similar tags like for : job search, job hunt, job hunting ---> Job Search
    uniqueTagsList = ', '.join(uniqueTagsSet)   # converting to list
    template = '''
    I will give you a list of tags. You need to unify tags with the following requirements,
    1. Tags are unified and merged to create a shorter list.
       Example 1: "Jobseekers", "Job Hunting" can all ne merged into a single tag "Job Search".
       Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation".
       Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement"
       Example 4: "Scam Alert", "Job Scam" etc can be mapped to "Scams"
    2. Each tag should follow title case concention i.e for example "Motivation", "Web Development"
    3. Output should be a JSON object and there should be No preamble
    4. Output should have following format i.e mapping original tag and unified tag. 
       for example: {{"Jobseekers": "Job Search", "Job hunting":"Job Search","Motivation":"Motivation"}}

       Here is the list of tags on which you have to perform all the working: {tags}

    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke({"tags": uniqueTagsList})
    try:
        json_parse = JsonOutputParser()
        res = json_parse.parse(response.content)
    except OutputParserException as e:
        print("LLM Output:", response.content)
        raise e
    return res


def process_raw_data(raw_form):

    template = '''
    You are given a linkedin post. you need to extract number of lines, language of the post and
    1. Return a valid JSON. no preamble.
    2. JSON object should have exactly three keys: line_count, language and tags.
    3. tags is an array of text tags. Extract maximum two tags.
    4. Language should be English or Hinglish(Hinglish means hindi + english)

    Here is the actual post on which you need to perform this task:
    {post}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke({"post": raw_form})
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("context too big!")
    return res





if __name__ == "__main__":
    process_posts("data/raw_posts.json","data/processed_posts.json")

 