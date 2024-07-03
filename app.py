import pickle
import streamlit as st
import pandas as pd
import requests
import base64

# Function to convert local image to base64 string
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64_str = base64.b64encode(image_file.read()).decode("utf-8")
    return base64_str

# Convert the local image to a base64 string
favicon_base64 = image_to_base64("movie-thumbnail.png")

bg_image_base64 = image_to_base64("backgrounds.jpeg")

# Set the page configuration with the base64 image string
st.set_page_config(page_title='movie recommender system',
                   page_icon=f"data:image/png;base64,{favicon_base64}",
                   )



# CSS to change the background to the image and style the text
st.markdown(
    f"""
    <style>
    .title-container {{
        background-image: url('data:image/png;base64,{bg_image_base64}');
        background-size: cover;
        color: white;
        padding: 0.5px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.3);
        margin-bottom: 4rem;
    }}
    .title-container h1 {{
        # padding: 0.4rem;
        # margin-bottom: 4rem;
        # border: groove 0.5rem #2818a3;
        # border-radius: 0.5rem;
        
        text-transform: uppercase;
        font-family: verdana;
        font-size: 5em;
        font-weight: 700;
        color: #f5f5f5;
        text-shadow: 1px 1px 1px #919191,
            1px 2px 1px #919191,
            1px 3px 1px #919191,
            1px 4px 1px #919191,
            1px 5px 1px #919191,
            1px 6px 1px #919191,
            1px 7px 1px #919191,
            1px 8px 1px #919191,
            1px 9px 1px #919191,
            1px 10px 1px #919191,
        1px 18px 6px rgba(16,16,16,0.4),
        1px 22px 10px rgba(16,16,16,0.2),
        1px 25px 35px rgba(16,16,16,0.2),
        1px 30px 60px rgba(16,16,16,0.4);
    }}
    </style>
    <div class="title-container">
        <h1>MOVIE RECOMMENDER SYSTEM</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# # Function to load HTML file
# def load_html(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         return file.read()

# # Load HTML content
# html_content = load_html('home.html')

# # Display HTML content in Streamlit
# st.markdown(html_content, unsafe_allow_html=True)



# Load custom CSS
st.markdown('<style>' + open('styles.css').read() + '</style>', unsafe_allow_html=True)


def fetch_poster_and_links(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=ab960f706b558bd0cfae45308d4c25da&language=en-US".format(movie_id)
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    links_path = data['imdb_id']
    full_poster_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    full_links_path = "https://www.imdb.com/title/" + links_path
    return full_poster_path,full_links_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_links = []
    for i in distances[1:6]:
        # fetch the movie poster
        current_movie_id = movies.iloc[i[0]].movie_id
        fetch_poster,fetch_links = fetch_poster_and_links(current_movie_id)

        recommended_movie_posters.append(fetch_poster)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_links.append(fetch_links)

    return recommended_movie_names,recommended_movie_posters,recommended_movie_links


# st.header('Movie Recommender System')
movie_dict = pickle.load(open('movie_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# Custom-styled label
st.markdown('<div class="custom-label">Type or select a movie from the dropdown</div>', unsafe_allow_html=True)

movies = pd.DataFrame(movie_dict)
selected_movie_name = st.selectbox(
    "",
    movies['title'].values
)


if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_links = recommend(selected_movie_name)
    
    # Display recommended movies in rows using custom HTML and CSS
    for i in range(5):
        st.markdown(
            f"""
            <div class="custom-text">
                <img src="{recommended_movie_posters[i]}" alt="Movie Poster">
                <div>
                    <p> {recommended_movie_names[i]} </p>
                    <a href="{recommended_movie_links[i]}" target="_blank" > Description or additional details about the movie. </a>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# if st.button('Show Recommendation'):
#     recommended_movie_names,recommended_movie_posters,recommended_movie_links = recommend(selected_movie_name)
#     col1, col2, col3, col4, col5 = st.columns(5)
#     with col1:
#         # Display the first recommended movie name with a link and custom styling
#         st.markdown(f"<div class='custom-text'><a href='{recommended_movie_links[0]}' >{recommended_movie_names[0]}</a></div>", unsafe_allow_html=True)
#         st.image(recommended_movie_posters[0], width=400)
#     with col2:
#         st.markdown(f"<div class='custom-text'><a href='{recommended_movie_links[1]}' target='_blank'>{recommended_movie_names[1]}</div>", unsafe_allow_html=True)
#         st.image(recommended_movie_posters[1], width=400)

#     with col3:
#         st.markdown(f"<div class='custom-text'><a href='{recommended_movie_links[2]}' target='_blank'>{recommended_movie_names[2]}</div>", unsafe_allow_html=True)
#         st.image(recommended_movie_posters[2], width=400)
#     with col4:
#         st.markdown(f"<div class='custom-text'><a href='{recommended_movie_links[3]}' target='_blank'>{recommended_movie_names[3]}</div>", unsafe_allow_html=True)
#         st.image(recommended_movie_posters[3], width=400)
#     with col5:
#         st.markdown(f"<div class='custom-text'><a href='{recommended_movie_links[4]}' target='_blank'>{recommended_movie_names[4]}</div>", unsafe_allow_html=True)
#         st.image(recommended_movie_posters[4], width=400)





