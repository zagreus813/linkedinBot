import requests
import json

class LinkedInService:
    def __init__(self, access_token):
        self.access_token = access_token
        self.api_url = "https://api.linkedin.com/v2/ugcPosts"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        self.author_id = self._get_author_id()

    def _get_author_id(self):
        """آیدی پروفایل کاربر را می‌گیرد"""
        url = "https://api.linkedin.com/v2/userinfo" # یا me
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return f"urn:li:person:{response.json().get('sub')}"
        return None

    def post_text(self, text):
        if not self.author_id:
            return False, "Failed to get Author ID"

        post_data = {
            "author": self.author_id,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }

        response = requests.post(self.api_url, headers=self.headers, json=post_data)
        if response.status_code == 201:
            return True, "Published Successfully"
        else:
            return False, response.text