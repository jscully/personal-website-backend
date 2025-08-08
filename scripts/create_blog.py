import sys
import os
from datetime import datetime, timezone
from uuid import uuid4

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data.repositories.session import SessionLocal
from app.data.models.blog import Blog
from app.data.models.tag import Tag

def create_test_blog():
    db = SessionLocal()

    try:
        existing_blog = db.query(Blog).filter(Blog.slug == "my-first-blog-post").first()
        if existing_blog:
            print("Blog already exists!")
            return

        tag1 = db.query(Tag).filter(Tag.name == "Technology").first()
        if not tag1:
            tag1 = Tag(
                name="Technology",
                description="Posts about technology and programming",
                color_code="#007ACC"
            )
            db.add(tag1)

        tag2 = db.query(Tag).filter(Tag.name == "Python").first()
        if not tag2:
            tag2 = Tag(
                name="Python",
                description="Python programming language",
                color_code="#3776AB"
            )
            db.add(tag2)

        new_blog = Blog(
            title="My First Blog Post",
            slug="my-first-blog-post",
            content="""# Welcome to My Blog

This is my first blog post! I'm excited to share my thoughts and experiences with you.

## About This Post

This post covers:
- Getting started with blogging
- Setting up a personal website
- Best practices for content creation

## Content Section

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Conclusion

Thanks for reading my first blog post. More content coming soon!
            """.strip(),
            excerpt="This is my first blog post where I introduce myself and share my thoughts about starting a personal website.",
            publication_dt=datetime.now(timezone.utc),
            status="published",
            featured_image="https://via.placeholder.com/800x400?text=My+First+Blog+Post",
            seo_description="My first blog post about getting started with blogging and creating content",
            reading_time=5
        )

        new_blog.tags = [tag1, tag2]

        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)

        print(f"Blog created successfully!")
        print(f"Title: {new_blog.title}")
        print(f"Slug: {new_blog.slug}")
        print(f"Status: {new_blog.status}")
        print(f"Blog ID: {new_blog.id}")
        print(f"Tags: {', '.join([tag.name for tag in new_blog.tags])}")

    except Exception as e:
        print(f"Error creating blog: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def create_multiple_test_blogs():
    """Create multiple test blogs for better testing"""
    db = SessionLocal()

    try:
        # Create additional tags
        tags_data = [
            {"name": "Web Development", "description": "Frontend and backend development", "color_code": "#FF6B35"},
            {"name": "Tutorial", "description": "Step-by-step tutorials", "color_code": "#4ECDC4"},
            {"name": "Opinion", "description": "Personal thoughts and opinions", "color_code": "#45B7D1"},
        ]

        created_tags = []
        for tag_data in tags_data:
            existing_tag = db.query(Tag).filter(Tag.name == tag_data["name"]).first()
            if not existing_tag:
                tag = Tag(**tag_data)
                db.add(tag)
                created_tags.append(tag)
            else:
                created_tags.append(existing_tag)

        # Get existing tags
        tech_tag = db.query(Tag).filter(Tag.name == "Technology").first()
        python_tag = db.query(Tag).filter(Tag.name == "Python").first()

        # Create multiple blog posts
        blogs_data = [
            {
                "title": "Getting Started with FastAPI",
                "slug": "getting-started-with-fastapi",
                "content": """# FastAPI Tutorial

FastAPI is a modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints.

## Key Features
- Fast performance
- Easy to use
- Automatic documentation
- Type hints support

## Installation
```bash
pip install fastapi uvicorn
```

## Your First API
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

This creates a simple API that returns a JSON response.""",
                "excerpt": "Learn how to build modern APIs with FastAPI, a high-performance Python web framework.",
                "tags": [tech_tag, python_tag, created_tags[0]] if tech_tag and python_tag else [],
                "reading_time": 8
            },
            {
                "title": "Database Design Best Practices",
                "slug": "database-design-best-practices",
                "content": """# Database Design Best Practices

Good database design is crucial for application performance and maintainability.

## Key Principles
1. Normalize your data
2. Use appropriate data types
3. Create proper indexes
4. Plan for scalability

## Common Mistakes
- Over-normalization
- Poor indexing strategy
- Ignoring query patterns
- Not considering future growth

## Conclusion
Following these principles will help you build robust, scalable databases.""",
                "excerpt": "Essential principles and best practices for designing efficient and scalable databases.",
                "tags": [tech_tag, created_tags[1]] if tech_tag else [],
                "reading_time": 12
            },
            {
                "title": "Why I Switched to Python",
                "slug": "why-i-switched-to-python",
                "content": """# Why I Switched to Python

After years of working with various programming languages, I made the switch to Python. Here's why.

## Readability Matters
Python's syntax is clean and readable, making it easier to write and maintain code.

## Rich Ecosystem
The Python ecosystem is vast, with libraries for almost everything:
- Data science: pandas, numpy, scikit-learn
- Web development: Django, Flask, FastAPI
- Machine learning: TensorFlow, PyTorch

## Community Support
The Python community is welcoming and helpful, with excellent documentation and resources.

## Versatility
From web development to data science, Python handles it all.""",
                "excerpt": "My personal journey and reasons for choosing Python as my primary programming language.",
                "tags": [python_tag, created_tags[2]] if python_tag else [],
                "reading_time": 6
            }
        ]

        created_blogs = []
        for blog_data in blogs_data:
            # Check if blog already exists
            existing_blog = db.query(Blog).filter(Blog.slug == blog_data["slug"]).first()
            if existing_blog:
                print(f"Blog '{blog_data['title']}' already exists, skipping...")
                continue

            blog = Blog(
                title=blog_data["title"],
                slug=blog_data["slug"],
                content=blog_data["content"],
                excerpt=blog_data["excerpt"],
                publication_dt=datetime.now(timezone.utc),
                status="published",
                reading_time=blog_data["reading_time"],
                seo_description=blog_data["excerpt"]
            )

            if blog_data["tags"]:
                blog.tags = blog_data["tags"]

            db.add(blog)
            created_blogs.append(blog)

        db.commit()

        print(f"\nCreated {len(created_blogs)} additional blogs!")
        for blog in created_blogs:
            print(f"- {blog.title} (/{blog.slug})")

    except Exception as e:
        print(f"Error creating additional blogs: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating test data...")
    create_test_blog()

    create_multiple_test_blogs()

    print("\nAll test blogs created successfully!")