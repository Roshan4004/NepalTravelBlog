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
(Replace with your actual website URL)

## Current Update (October 2, 2024)
Since this website is not used to write blogs by myself due to unrelated reasons, I am thinking of auto-generating blog by an AI model along with AI generated image. Every day a new blog is going to be posted by AI automatically.
- **AI model** : Not sure, maybe claude
- **Image Generation** : Pollinations.ai and stable-diffusion
- **Task Management** : Celery
- **Message Broker**: Redis as of now, might change to RabbitMQ later

## Updates (October 19, 2024)
The project is now automated to generate and post travel blogs daily using AI. This allows consistent content posting without manual input.

- **AI Model**: Currently using Google Generative AI for blog generation.
- **Image Generation**: Using Pollinations.ai and Stable Diffusion to generate AI-powered images for each post.
- **Task Management**: Celery handles the periodic tasks of generating and posting blogs.
- **Message Broker**: Redis is being used to manage the task queues for Celery.

With this automation, the blog remains active and regularly updated with fresh content!

## Explore Celery Integration
If you're interested in how Celery is set up separately for task management, check out the `celery_seperate` branch: [Separate Celery Branch](https://github.com/Roshan4004/NepalTravelBlog/tree/celery_seperate)

Thank you for reading!