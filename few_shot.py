import json
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

class FewShotPosts:
    def __init__(self,file_path="data/processed_posts.json"):
        self.df = None
        self.uniqueTags = None
        self.load_posts(file_path)
        

    def load_posts(self,file_path):
        with open(file_path, encoding="utf-8") as f:
            post = json.load(f)
            self.df = pd.json_normalize(post)
            self.df["length"] = self.df["line_count"].apply(self.findLength)
            pd_column_of_all_tags = self.df["tags"].apply(lambda x: x).sum()
            self.uniqueTags = set(list(pd_column_of_all_tags))

    def getTags(self):
        return self.uniqueTags
    
    def findLength(self,count):
        if count<5:
            return "Short"
        elif count>=5 & count<=10:
            return "Medium"
        else:
            return "Long"

    def getFilteredPosts(self,len,tag,lang):
        filtered_df = self.df[
                            (self.df["length"] == len)
                            & (self.df["language"] == lang)
                            & (self.df["tags"].apply(lambda tags: tag in tags))
                            ]
        return filtered_df.to_dict(orient="records")
    

if __name__ == "__main__":
    fs = FewShotPosts()
    posts = fs.getFilteredPosts("Short","Job Search","English")
    print(posts)