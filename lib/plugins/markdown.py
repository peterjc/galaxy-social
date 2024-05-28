import os
import time


class markdown_client:
    def __init__(self, **kwargs):
        self.save_path = kwargs.get("save_path") and (
            kwargs["save_path"]
            if os.path.isabs(kwargs["save_path"])
            else os.path.join(os.getcwd(), kwargs["save_path"])
        )

    def create_post(self, content, mentions, hashtags, images, **kwargs):
        try:
            _images = (
                "\n"
                + "\n".join(
                    [
                        f'![{image.get("alt_text", "")}]({image["url"]})'
                        for image in images
                    ]
                )
                if images
                else ""
            )
            mentions = "\n" + " ".join([f"@{v}" for v in mentions]) if mentions else ""
            hashtags = "\n" + " ".join([f"#{v}" for v in hashtags]) if hashtags else ""
            text = f"{content}{mentions}{hashtags}{_images}"
            if self.save_path:
                os.makedirs(self.save_path, exist_ok=True)
                prefix = kwargs.get("file_path", "").replace(".md", "")
                file_name = (
                    f"{self.save_path}/{prefix.replace('/', '-')}_{time.strftime('%Y%m%d-%H%M%S')}.md"
                )
                with open(file_name, "w") as f:
                    f.write(text)
            if kwargs.get("preview"):
                social_media = ", ".join(kwargs.get("media", []))
                pre_comment_text = ""
                if len(images) > 4 and (
                    "mastodon" in social_media or "bluesky" in social_media
                ):
                    pre_comment_text = f"Please note that Mastodon and Bluesky only support up to 4 images in a single post. The first 4 images will be included in the post, and the rest will be ignored.\n"
                comment_text = f"{pre_comment_text}This is a preview from {prefix.split('/')[-1]} that will be posted to {social_media}:\n\n{text}"
                return True, None, comment_text
            return True, None
        except Exception as e:
            if kwargs.get("preview", False):
                print(e)
                return False, None, e
            return False, None
