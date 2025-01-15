# Travel Blog Project

## Overview
This is a travel blog project designed to share insights and experiences from various travel destinations. The project leverages Django for the backend and provides a clean interface for users to explore blog posts.

## Features
- **User Authentication**: Secure sign-up and login functionality.
- **Blog Post Creation**: Admins can create and manage blog posts.
- **Image Upload**: Supports image uploads for blog posts.
- **Responsive Design**: The website is mobile-friendly and adapts to various screen sizes.

## Technologies Used
- **Django**: The web framework used for building the project.
- **Cloudinary**: The cloud platform used for storing images.
- **HTML/CSS**: For frontend development.
- **JavaScript**: For interactive elements.

## Visit the Website
Check out the live site here: [Travel Blog Website](https://neptravelblog.pythonanywhere.com)

## Update (October 2, 2024)
Since this website is not used to write blogs by myself due to unrelated reasons, I am thinking of auto-generating blog by an AI model along with AI-generated image. Every day a new blog is going to be posted by AI automatically.
- **AI model**: Not sure, maybe Claude
- **Image Generation**: Pollinations.ai and stable-diffusion
- **Task Management**: Celery
- **Message Broker**: Redis as of now, might change to RabbitMQ later

## Update (October 19, 2024)
The project is now automated to generate and post travel blogs daily using AI. This allows consistent content posting without manual input.

- **AI Model**: Currently using Google Generative AI for blog generation.
- **Image Generation**: Using Pollinations.ai and Stable Diffusion to generate AI-powered images for each post.
- **Task Management**: Celery handles the periodic tasks of generating and posting blogs.
- **Message Broker**: Redis is being used to manage the task queues for Celery.

With this automation, the blog remains active and regularly updated with fresh content!

## Update (November 30, 2024)
Taking the blog project a step further, an AI avatar feature will be integrated to enhance user interaction. Users will be able to click on a blog post to have it recited by an AI avatar in either Nepali or English.

### AI Avatar Features
- **Recitation Option**: Users can choose to have the blog recited in Nepali or English.
- **Translation**: The blog content is translated from English to Nepali using a Generative AI model.
- **Voice Synthesis**: Google’s GTTS (Google Text-to-Speech) will be used to generate high-quality voice outputs.
- **Avatar Rendering**: The AI avatar is rendered using React Three Fiber.
- **Avatar Design**: The base design of the avatar will be created using Ready Player Me, with custom modifications made in Blender.
- **Avatar's Lipsync**: Although, I am still figuring out and testing options, at first I will be using ["rhubarb-lip-sync"](https://github.com/DanielSWolf/rhubarb-lip-sync) which is a really cool project.

With this feature, the travel blog will not only provide engaging content but also an immersive and interactive user experience.

## Update (January 15, 2025)
The project now has an AI avatar which recites the blog contents for you!

- **Recitation Option**: Users can choose to have the blog recited in Nepali or English.
- **In Avatar Options**: Users can select play/pause and reset option for respective performation of avatar.
- **In the html page**: A fully responsive sidebar is shown which includes the avatar when selected an language. Options to minimize and maximixe the avatar in mobile view..

### Future:
- A better translator will be used for translation of blog contents to nepali.
- Currently used Google's TTS is not perfect so, a better and flexible tts will be used.

**(Note: Only blogs written by the "automatic blog writer" has ability to show AI avatars but later it will be available for user written blogs as well.)**

## Explore Celery Integration
If you're interested in how Celery is set up separately for task management, check out the `celery_seperate` branch: [Separate Celery Branch](https://github.com/Roshan4004/NepalTravelBlog/tree/celery_seperate)

If you want to read about the AI integration, please have a look at my post on [medium](https://medium.com/@gautamroshan4004/how-i-automated-my-travel-blog-using-ai-and-celery-a-developers-journey-c8174d4a235a)

Thank you for reading!