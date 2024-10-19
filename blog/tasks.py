from celery import shared_task
import requests, os, re
from blogg.settings import GEMINI_KEY, POST_AI, GET_TITLES
import google.generativeai as genai, base64

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_blog_titles():
    url = GET_TITLES
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to get blog titles: {str(e)}")
        return None
    
def parse_ai_response(response):
    title = re.search(r'### Blog Title:\n(.+?)(?=\n###)', response, re.DOTALL).group(1).strip()
    address = re.search(r'### Blog Address:\n(.+?)(?=\n###)', response, re.DOTALL).group(1).strip()
    content = re.search(r'### Blog Content:\n(.+?)(?=\n###)', response, re.DOTALL).group(1).strip()
    image_prompt = re.search(r'### Image Generation Prompt:\n(.+?)(?=\n\n|$)', response, re.DOTALL).group(1).strip()

    return {
        "title": title,
        "address": address,
        "content": content,
        "image_prompt": image_prompt,
    }

def generate_blog_content_and_image_prompt(blog_titles):
    prompt = f"""
Write a blog post about any specific location in Nepal, focusing on a detailed, lesser-known aspect or experience of the place, not just general information. For example, instead of "Visit to Pokhara," focus on a specific experience like "Pokhara's Lakeside Cafes during Sunrise."

Do NOT write about the following topics, as blogs on these have already been written:
- {blog_titles}

Make sure to follow these guidelines:
- Write the blog in a descriptive, engaging, and informative style.
- Provide a **unique title** for the blog.
- Specify the **exact address or location** of the place being described, so readers know where it is.
- Avoid general descriptions and focus on unique experiences, hidden gems, or specific local attractions within Nepal.
- Include relevant historical, cultural, or natural information that adds depth to the description.
-For bolding and spacing in content section, write in HTML. Don not use markdown

In addition to the blog content, also generate a **prompt for an AI image generator** that will capture the essence of the place you’re writing about. This prompt should help the AI generate a realistic and context-appropriate image. 

Output Format:
### Blog Title:
[Title of the blog]

### Blog Address:
[Location/address details of the place being described]

### Blog Content:
[The actual blog content. Write in HTML for bold and paragraph change.]

### Image Generation Prompt:
[Provide a highly specific, vivid, and detailed image prompt that describes the scene, ambiance, or key features of the place.]

#### Example Output:

### Blog Title:
Sunrise at Pokhara's Hidden Lakeside Cafes

### Blog Address:
Lakeside Road, Sedi Heights, Pokhara, Nepal

### Blog Content:
Nestled along the quieter stretches of Pokhara’s lakeside, far from the bustling tourist spots, are a series of charming cafes that offer a serene, picturesque view of Phewa Lake during the early morning hours. These hidden gems allow visitors to soak in the tranquility of the lake, with the Annapurna range reflecting on the still waters as the sun slowly rises. The experience is made richer by the crisp morning air and the distant sound of prayer flags fluttering in the breeze...

### Image Generation Prompt:
A serene lakeside café in Pokhara at sunrise, with still waters of Phewa Lake reflecting the distant Annapurna mountains, a few locals sipping tea in outdoor seating, with prayer flags fluttering in the cool morning breeze.

"""

    try:
        ai_response = model.generate_content(prompt)
        final_resp=parse_ai_response(ai_response.text)
        return final_resp
    except Exception as e:
        print(f"AI call failed: {str(e)}")
        return None, None

def generate_image(image_prompt):
    url = f"https://image.pollinations.ai/prompt/{image_prompt}?width=768&height=800&model=FLUX&seed=1"
    response = requests.get(url)

    if response.status_code == 200:
        image_base64 = base64.b64encode(response.content).decode('utf-8')
        return image_base64
    else:
        print(f"Image generation failed")
        return None

def post_blog(title, content, address, image_base64):
    url = POST_AI
    payload = {
        "title": title,
        "content": content,
        "local_body": address,
        "main_img": image_base64
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Blog post failed: {str(e)}")
        return None

@shared_task
def cron_blog_writer():
    blog_titles = get_blog_titles()['data']
    if blog_titles or blog_titles==[]:
        final_resp = generate_blog_content_and_image_prompt(blog_titles)
        if final_resp:
            image_base64 = generate_image(final_resp['image_prompt'])
            if image_base64:
                post_response = post_blog(
                    title=final_resp['title'],
                    content=final_resp['content'],
                    address=final_resp['address'], 
                    image_base64=image_base64
                )
                print(f"Blog posted: {post_response}")
                return(post_response)
            else:
                print("Image generation failed.")
        else:
            print("Failed to generate blog content or image prompt.")
    else:
        print("No blog titles available.")
