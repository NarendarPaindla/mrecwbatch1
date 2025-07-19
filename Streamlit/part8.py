import streamlit as st


car_info = [{
  "CAR_MAKE": "Porsche",
  "CAR_MODEL": "911",
  "CAR_MODEL_YEAR": 1988,
  "CAR_PRICE": 3176
}, {
  "CAR_MAKE": "Chevrolet",
  "CAR_MODEL": "Corvette",
  "CAR_MODEL_YEAR": 1961,
  "CAR_PRICE": 23741
}, {
  "CAR_MAKE": "Audi",
  "CAR_MODEL": "S4",
  "CAR_MODEL_YEAR": 2011,
  "CAR_PRICE": 5533
}]

st.header('Choose your car.')
option = st.selectbox(
    "Which car did you like?",
    [
        car_info[0]['CAR_MAKE'] + " " + car_info[0]['CAR_MODEL'],
        car_info[1]['CAR_MAKE'] + " " + car_info[1]['CAR_MODEL'],
        car_info[2]['CAR_MAKE'] + " " + car_info[2]['CAR_MODEL']
    ]
)

st.write(option)