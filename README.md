# 🎬 Movie Reviewer Dashboard

An interactive movie analytics dashboard built with **Plotly Dash**. This application enables users to explore, analyze, and visualize movie data through a clean and intuitive interface.

## 🔍 Features

- 🔎 **Search Functionality**: Filter movies by title or genre  
- 🎭 **Genre-Based Filtering**: Dropdown menu to select specific genres  
- ⭐ **Rating Range Slider**: Dynamically filter movies by average rating  
- 📅 **Release Date Picker**: Filter movies by release date range  
- 📊 **Interactive Visualizations**:  
  - **Bar Chart**: Displays average rating by genre  
  - **Scatter Plot**: Compares movie ratings across genres  
  - **Line Chart**: Shows rating trends over time  
  - **Pie Chart**: Highlights genre distribution  
  - **Genre Count Bar Chart**: Displays frequency of each genre  
- 📋 **Interactive Data Table**: Click to view selected movie details  
- 🧠 **Genre Summary Panel**: Shows highest and lowest rated genres with insights  

## 📈 Example Insights

> - Highest rated genre: `Mystery` with average rating `8.6`  
> - Most frequent genre: `Drama`  
> - Movies from niche genres tend to receive higher ratings  
> - Line trend is flat due to all data being from 1995 (limitation of dataset)  

## 🛠️ Tech Stack

- Python 3  
- [Dash](https://plotly.com/dash/)  
- Plotly Express  
- Pandas  

## 🌐 Live Demo

👉 [Click here to try it out!](https://movie-reviewer-dashboard.onrender.com)

## 🚀 Installation

```bash
git clone https://github.com/BarisAI/movie-reviewer-dashboard.git
cd movie-reviewer-dashboard
pip install -r requirements.txt
python app.py
