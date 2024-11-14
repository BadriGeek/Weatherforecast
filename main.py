import plotly.express as px
import streamlit as st
from Backend import get_data


st.title("Weather Forecast for the Next Days")
place = st.text_input("Place: ")
days = st.slider("Forecast Days",min_value=1,max_value=5,
                 help="Select the number of forecasted days")
option = st.selectbox("Select data to view",
                      ("Temperature","Sky"))
st.subheader(f"{option}for the next {days} days in {place}")

if place:
    try:

        filtered_data = get_data(place,days)
        

        if option == "Temperature":
            temperatures = [int(dict["main"]["temp"])/10 for dict in filtered_data]
            dates = [dict["dt_txt"] for dict in filtered_data]

            figure = px.line(x=dates,y=temperatures,labels={"x":"Date","y":"Temperature (C)"})
            st.plotly_chart(figure)

        if option == "Sky":
            images = {"Clear": "images/clear.png","Clouds": "images/cloud.png",
                      "Rain": "images/rain.png","Snow": "images/snow.png"}
            sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]

            image_paths = [images[condition] for condition in sky_conditions]

            # Create columns for a grid-like display
            # I use 8 columns because we have 8 observations per day
            columns_per_row = 4

            # Split the list of images into chunks of columns_per_row
            rows = [image_paths[i:i + columns_per_row] for i in
                    range(0, len(image_paths), columns_per_row)]

            # Display images row by row
            for row in rows:
                cols = st.columns(columns_per_row)
                for col, image in zip(cols, row):
                    col.image(image, width=115)
    except KeyError:
        st.write(f"That {place} place does not exist. ")
