## Python Static Site Generation Tool

This is a tool I originally wrote to procedurally generate my own personal blog. 
I realized this could be a helpful tool for people who want to focus on their content
rather than the technicalities (while still being able to claim they wrote their own website).

As of right now this tool does **not** include styling, however that is something I am looking to add in the future. I've tried to keep the structure of the pages as simple as possible to make it easier to add your own styling.

### Instructions

1. Clone this repository on your local machine
```
git clone https://github.com/ethanzh/static-site-generator.git
```
2. Navigate to the ```content``` directory where you will find a ```hello_world.md``` file. This contains the template you will be using to write your content. Take note of the JSON-esque metadata stored at the top.
3. After writing your content, navigate back to the root folder and run ```python build.py``` (note, you may need to run ```pip install markdown``` in order for the script to run successfully).
4. Your files are now generated! ```index.html``` contains HTML for your home page which contains links to each blog post.

These generated files can be served from a web server of your choice. I recommend using [GitHub Pages](https://pages.github.com/) due to its sheer simplicity.